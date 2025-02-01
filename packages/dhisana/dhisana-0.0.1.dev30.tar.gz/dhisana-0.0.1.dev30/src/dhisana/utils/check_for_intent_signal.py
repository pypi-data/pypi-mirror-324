import logging
from typing import Any, Dict, List, Optional, cast

from pydantic import BaseModel
from dhisana.utils.generate_structured_output_internal import get_structured_output_with_o1
from dhisana.utils.compose_search_query import (
    generate_google_search_queries,
    get_search_results_for_insights
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class IntentSignalScoring(BaseModel):
    score_based_on_intent_signal: int


async def check_for_intent_signal(
    lead: Dict[str, Any],
    signal_to_look_for_in_plan_english: str,
    intent_signal_type: str,
    add_search_results: Optional[bool] = False,
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> int:
    """
    Evaluate a 'lead' for a specific intent signal and return an integer score from 0–5.
    """

    search_results_text = ""
    if add_search_results:
        # Correctly call get_search_results_for_insights with intent_signal_type
        search_results = await get_search_results_for_insights(
            lead=lead,
            english_description=signal_to_look_for_in_plan_english,
            intent_signal_type=intent_signal_type,
            tool_config=tool_config
        )

        # Build a readable string from returned queries and results
        # Each item in 'search_results' is a dict: {"query": str, "results": <json-encoded list of SERP results>}
        for item in search_results:
            query_str = item.get("query", "")
            results_str = item.get("results", "")
            search_results_text += f"Query: {query_str}\nResults: {results_str}\n\n"

    user_prompt = f"""
    Hi AI Assistant,
    You are an expert in scoring leads based on intent signals.
    You have the following lead and user requirements to provide a  qulifying lead score score between 0 and 5 
    based on the intent signal the user is looking for.
    Do the following step by step:
    1. This about the summary of the lead and the company lead is working for.
    2. Create a summary of the search results obtained.     
    3. Think about the signal user is looking for to qualify and score the lead. 
    4. Use the lead information, summary of search results and signal user is looking for to score the lead.
    5. Go back and check if the score makes sense. Score between 0-5 based on the confidence of the signal.
    
    Lead Data:
    {lead}

    Description of the signal user is looking for:
    {signal_to_look_for_in_plan_english}
    
    Following is some search results I found online. Use them if they are relevant for scoring:
    {search_results_text}

    Return your answer in valid JSON with the key 'score_based_on_intent_signal'.
    Make sure it is an integer between 0 and 5.
    """

    logger.info("Scoring intent signal '%s' for lead: %s", intent_signal_type, lead.get("full_name", "Unknown"))

    # The helper returns (model_instance or None, status_str)
    response_any, status = await get_structured_output_with_o1(
        user_prompt,
        IntentSignalScoring,
        tool_config=tool_config
    )

    if status != "SUCCESS" or response_any is None:
        raise Exception("Failed to generate an intent signal score from the LLM.")

    # Cast to your specific model so the type checker is satisfied
    response = cast(IntentSignalScoring, response_any)
    score = response.score_based_on_intent_signal

    logger.info(
        "Lead '%s' scored %d for intent signal '%s'.",
        lead.get("full_name", "Unknown"),
        score,
        intent_signal_type
    )
    return score
