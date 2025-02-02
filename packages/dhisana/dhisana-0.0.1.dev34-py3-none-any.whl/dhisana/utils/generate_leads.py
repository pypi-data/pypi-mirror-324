import json
import logging
import asyncio
from typing import Any, Dict, List, Optional

import aiohttp
from pydantic import BaseModel, Field

from dhisana.schemas.sales import LeadsQueryFilters, SmartList
from dhisana.utils.apollo_tools import search_leads_with_apollo
from dhisana.utils.generate_structured_output_internal import get_structured_output_internal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_leads(
    user_query: str,
    request: SmartList,
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> str:
    logger.info("Starting generate_leads with user_query=%s", user_query)

    """
    1) Generate a LeadsQueryFilters object by parsing a user query with an LLM.
    2) Search Apollo with those filters.
    3) Return JSON containing a list of SmartListLead objects.
    """
    prompt_msg = f"""
    Hi AI Assistant, User has provided following query User query: {user_query}
    \nConvert to valid JSON for LeadsQueryFilters."""
    logger.info("Prompt message: %s", prompt_msg)

    filters_obj, status = await get_structured_output_internal(
        prompt=prompt_msg,
        response_format=LeadsQueryFilters,
        tool_config=tool_config
    )
    if status != "SUCCESS":
        logger.error("Failed to parse user query into LeadsQueryFilters.")
        return json.dumps({
            "status": "FAIL",
            "message": "Failed to parse user query into LeadsQueryFilters."
        })

    try:
        logger.info("Starting search_leads_with_apollo with filters: %s", filters_obj.dict())
        smart_leads = await search_leads_with_apollo(filters_obj, request, tool_config)
        leads_data = [lead.dict() for lead in smart_leads]
        return json.dumps({
            "status": "SUCCESS",
            "leads": leads_data
        }, default=str)
    except Exception as ex:
        logger.error("Error during Apollo search: %s", str(ex))
        return json.dumps({
            "status": "FAIL",
            "message": f"Error during Apollo search: {str(ex)}"
        })