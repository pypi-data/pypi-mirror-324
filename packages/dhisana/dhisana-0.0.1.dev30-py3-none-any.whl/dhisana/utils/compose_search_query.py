import logging
import os
import json
from typing import Any, Dict, List, Optional

import aiohttp
from pydantic import BaseModel

from dhisana.utils.generate_structured_output_internal import get_structured_output_with_o1
from dhisana.utils.cache_output_tools import cache_output, retrieve_output

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GoogleSearchQuery(BaseModel):
    """
    Pydantic model representing the three Google search queries generated.
    google_search_queries has list of 3 search query strings.
    """
    google_search_queries: List[str]


async def generate_google_search_queries(
    lead: Dict[str, Any],
    english_description: str,
    intent_signal_type: str,
    example_query: str = "",
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Generate three Google search queries based on a plain-English description.
    
    Args:
        lead: Dictionary containing information about the lead.
        english_description: The user's plain-English description.
        intent_signal_type: A string indicating the intent signal type.
        example_query: Optional user-provided example.
        tool_config: Optional list of dictionaries containing tool configuration.

    Returns:
        A dictionary with a single key: "google_search_query", which maps to
        a list of three search queries.
    """

    # System message to guide the LLM
    system_message = (
        "You are a helpful AI Assistant that converts an English description "
        "of search requirements into valid Google search queries. "
        "Your output MUST generate exactly three search queries. "
        "No extra commentary or text is allowed. If you are unsure about a filter, "
        "make your best guess or omit it."
    )

    few_shot_example_queries = (
        'To find if the company uses a technology you can use queries like below:\n',
        'site:linkedin.com/in "{organization_name}" "{technology_to_look_for}" {location like US, UK etc} intitle:"{company_name}"\n'         
        'site:linkedin.com/jobs/view/ "{organization_name}" "{technology_to_look_for}"\n\n'
        'To find user with specific title in the company, you can use queries like below:\n',
        'site:linkedin.com/in "{organization_name}" "{title looking for like CEO, CTO}" \n\n',
        'To search for funding or acquisition information, you can use queries like below:\n',
        'site:news.google.com "{organization_name}" "funding" OR "acquisition" OR "partnership" after:2022-01-01 \n',
        'site:crunchbase.com "{organization_name}" "funding" \n\n',
        'To search for competitors and market share, you can use queries like below:\n',
        '"{organization_name}" "competitors" OR "versus" OR "vs" "market share" "compare" \n',
    )

    user_prompt = f"""
        {system_message}
        Think and do the following step by step:
        1. Think about the summary of the lead and the company the lead is working for.
        2. Think about the signal the user is looking for to qualify and score the lead.
        3. Use the lead information and the signal the user is looking for to generate three search queries to search in google.
        4. Go back and check if the queries make sense to search for signals that user is looking for about lead and his company.
        lead["organization_name"] has name of current company lead is working for.
        lead["lead_location"] has location of the lead. 
        Do Not use lead name in the query when searching for company information like technology used, funding, compete search etc.
        The user wants to build Google search queries for the following requirements:
        "{english_description}"

        Some example queries:
        {few_shot_example_queries}

        Some info about the lead:
        {lead}

        Additional example/context (if provided):
        {example_query}

        Intent signal type looking for:
        {intent_signal_type}

        Output MUST be valid JSON. 
        google_search_queries is a list of 3 search query strings.

        {{
            "google_search_queries": ["search query1", "search query2", "search query3"]
        }}
        """

    logger.info("Generating Google search queries from description: %s", english_description)

    # Call your structured-output helper
    response, status = await get_structured_output_with_o1(
        user_prompt,
        GoogleSearchQuery,
        tool_config=tool_config
    )

    if status != "SUCCESS" or not response:
        raise Exception("Error generating the Google search queries.")

    logger.info("Successfully generated Google search queries.")
    return response.model_dump()


async def get_search_results_for_insights(
    lead: Dict[str, Any],
    english_description: str,
    intent_signal_type: str,
    example_query: str = "",
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Uses generate_google_search_queries() to get three Google queries, 
    then calls search_google() for each query to fetch results.
    
    Args:
        lead: Dictionary containing information about the lead.
        english_description: The user's plain-English description.
        intent_signal_type: A string indicating the intent signal type.
        example_query: Optional user-provided example.
        tool_config: Optional list of dictionaries containing tool configuration.

    Returns:
        A list of dictionaries, where each dictionary contains:
        {
            "query": <the google query used>,
            "results": <a JSON string of search results array>
        }
    """
    response_dict = await generate_google_search_queries(
        lead=lead,
        english_description=english_description,
        intent_signal_type=intent_signal_type,
        example_query=example_query,
        tool_config=tool_config
    )
    
    # Extract the actual queries from the returned dictionary
    queries = response_dict.get("google_search_queries", [])
    results_of_queries = []

    for query in queries:
        results = await search_google(query, number_of_results=3, tool_config=tool_config)
        results_of_queries.append({
            "query": query,
            "results": json.dumps(results)
        })

    return results_of_queries


def get_serp_api_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Retrieves the SERPAPI_KEY access token from the provided tool configuration 
    or from the environment variable SERPAPI_KEY.
    """
    if tool_config:
        serpapi_config = next(
            (item for item in tool_config if item.get("name") == "serpapi"), 
            None
        )
        if serpapi_config:
            config_map = {
                item["name"]: item["value"]
                for item in serpapi_config.get("configuration", [])
                if item
            }
            serpapi_key = config_map.get("apiKey")
        else:
            serpapi_key = None
    else:
        serpapi_key = None

    serpapi_key = serpapi_key or os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        raise ValueError(
            "SERPAPI_KEY access token not found in tool_config or environment variable"
        )
    return serpapi_key


async def search_google(
    query: str,
    number_of_results: int = 3,
    tool_config: Optional[List[Dict]] = None
) -> List[str]:
    """
    Search Google using SERP API and return the results as a list of JSON strings.

    Args:
        query: The search query.
        number_of_results: Number of organic results to return.
        tool_config: Optional list of dictionaries containing tool configuration.

    Returns:
        A list of JSON strings, each string representing one search result.
        If any error occurs, returns a list with a single JSON-encoded error dict.
    """
    serpapi_key = get_serp_api_access_token(tool_config)

    # Check cache first
    cached_response = retrieve_output("search_google_serp", query)
    if cached_response is not None:
        return cached_response

    params = {
        "q": query,
        "num": number_of_results,
        "api_key": serpapi_key
    }

    url = "https://serpapi.com/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    error_data = await response.text()
                    return [json.dumps({"error": error_data})]

                result = await response.json()
                # Serialize each result to a JSON string
                serialized_results = [
                    json.dumps(item) for item in result.get('organic_results', [])
                ]
                # Cache results
                cache_output("search_google_serp", query, serialized_results)
                return serialized_results
    except Exception as exc:
        return [json.dumps({"error": str(exc)})]
