import datetime
import logging
import os
import json
from typing import Any, Dict, List, Optional

import aiohttp
from pydantic import BaseModel

from dhisana.utils.generate_structured_output_internal import get_structured_output_internal
from dhisana.utils.cache_output_tools import cache_output, retrieve_output
import asyncio

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
    Generate three Google search queries based on a plain-English description,
    incorporating the following logic:
      1. First consider searching LinkedIn and the organization's own website for relevant info.
      2. Then consider searching Instagram, Twitter, Github, Yelp, Crunchbase, Bloomberg,
         or reputable news/financial sites for relevant qualification info.
      3. If lead["primary_domain_of_organization"] is not empty, ALWAYS include one query
         that searches the domain with something like:
            site:<primary_domain_of_organization> "about this company"
      4. Make sure lead["organization_name"] is part of every query.

    Args:
        lead: Dictionary containing information about the lead, including 'organization_name'.
        english_description: The user's plain-English description.
        intent_signal_type: A string indicating the intent signal type.
        example_query: Optional user-provided example.
        tool_config: Optional list of dictionaries containing tool configuration.

    Returns:
        A dictionary with a single key: "google_search_queries", mapping to a list of
        exactly three search query strings.
    """
    # Pull out relevant values
    org_name = ""
    primary_domain = ""
    if lead and lead.get("organization_name", ""):
        org_name = lead["organization_name"].strip()
    if lead and lead.get("primary_domain_of_organization", ""):
        primary_domain = lead.get("primary_domain_of_organization", "").strip()

    # System message to guide the LLM
    system_message = (
        "You are a helpful AI Assistant that converts an English description of search requirements "
        "into valid Google search queries. \n\n"
        "Important instructions:\n"
        "1. Always include the organization name in every query. The organization name is:\n"
        f"   {org_name}\n"
        "2. First consider ways to use LinkedIn or the company's own website to gather info.\n"
        "3. Then consider how Google can leverage Instagram, Twitter, Github, Yelp, Crunchbase, Bloomberg, "
        "   or reputable news/financial sites to figure out relevant info for qualification.\n"
        "4. You MUST generate exactly three Google search queries. No extra commentary or text.\n"
        "5. If you're unsure about some filter, make your best guess or omit it.\n"
        "6. Primary domain of organization is: {primary_domain}. Use if present.\n\n"
        "7. Think like a salesperson trying to qualify a lead.\n\n"
        f"8. In any any site:linkedin.com search make sure intitle:{org_name} is present\n\n"
        "Output must be valid JSON with the structure:\n"
        "{\n"
        "   \"google_search_queries\": [\"search query1\", \"search query2\", \"search query3\"]\n"
        "}"
    )

    # Example queries for the LLM
    # We place placeholders to show how one might incorporate {org_name}.
    # In actual generation, the LLM will produce queries substituting org_name.
    few_shot_example_queries_lines = [
        'Examples:',
        '- Check for technology used by the organization on LinkedIn by searching /in and /posts:',
        f'- site:linkedin.com/in "{org_name}" "techonology_used check Eg Neo4j" intitle:"{org_name}"',
        f'- site:linkedin.com/posts "{org_name}" "techonology_used check Eg Neo4j" intitle:"{org_name}"',
        '- Check for Data Engineer at the organization:',
        f'- site:linkedin.com/in "{org_name}" "Data Engineer" intitle:"{org_name}"',
        '- Check for hiring Angular Developer at the organization:',
        f'- site:linkedin.com/jobs/view/ "{org_name}" "hiring" "angular developer" intitle:"{org_name}"',
        '- Check for funding, acquisition, or partnership news:',
        f'- site:news.google.com "{org_name}" "funding" OR "acquisition" OR "partnership"',
        f'- site:crunchbase.com "{org_name}" "funding"',
    ]

    if primary_domain:
        few_shot_example_queries_lines.append(f'- site:{primary_domain} Job Openings')
        few_shot_example_queries_lines.append(f'- site:{primary_domain} Case Studies')

    few_shot_example_queries_lines.append(f'- "{org_name}" "competitors" OR "versus" OR "vs" "market share" "compare"')

    few_shot_example_queries = "\n".join(few_shot_example_queries_lines)
    current_date_iso = datetime.datetime.now().isoformat()

    user_prompt = f"""
        {system_message}

        The user wants to build Google search queries for:
        "{english_description}"

        Some example queries (using placeholders like {{organization_name}}):
        {few_shot_example_queries}

        Some info about the lead (including organization_name):
        {json.dumps(lead, indent=2)}

        Additional example/context (if provided):
        {example_query}

        Intent signal type:
        {intent_signal_type}
        

        Please generate exactly three queries in JSON format as:
        {{
            "google_search_queries": ["query1", "query2", "query3"]
        }}
        Remember to include "{org_name}" in each query.
    """

    logger.info("Generating Google search queries from description: %s", english_description)

    # Call your structured-output helper
    response, status = await get_structured_output_internal(
        user_prompt,
        GoogleSearchQuery,
        tool_config=tool_config
    )

    if status != "SUCCESS" or not response:
        raise Exception("Error generating the Google search queries.")

    queries_dict = response.model_dump()
    
    # Also ensure that each query includes org_name
    fixed_queries = []
    for q in queries_dict["google_search_queries"]:
        # If org_name is missing in the query, we can insert it only if it's not a site:primary_domain query
        if org_name and org_name.lower() not in q.lower() and not q.lower().startswith(f'site:{primary_domain}'):
            q = f'{q} "{org_name}"'
        fixed_queries.append(q.strip())
    queries_dict["google_search_queries"] = fixed_queries
    
    # Ensure the domain-based query is included if primary_domain is present.
    # Force it into the last query if it's missing.
    if primary_domain:
        domain_query = f'site:{primary_domain}'
        queries = queries_dict["google_search_queries"]
        queries.append(domain_query)
        queries_dict["google_search_queries"] = queries

    logger.info("Search queries to be returned: %s", queries_dict["google_search_queries"])
    return queries_dict



async def get_search_results_for_insights(
    lead: Dict[str, Any],
    english_description: str,
    intent_signal_type: str,
    example_query: str = "",
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Uses generate_google_search_queries() to get up to four Google queries,
    then calls search_google() for each query in parallel to fetch results.
    
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
    
    # Extract and limit the queries to a maximum of four
    queries = response_dict.get("google_search_queries", [])
    queries = queries[:4]

    # Create a list of coroutines
    coroutines = [
        search_google(query, number_of_results=3, tool_config=tool_config) 
        for query in queries
    ]

    # Execute searches in parallel
    results = await asyncio.gather(*coroutines)

    # Build the response
    results_of_queries = []
    for query, query_results in zip(queries, results):
        results_of_queries.append({
            "query": query,
            "results": json.dumps(query_results)
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
