import base64
from typing import Any, Dict, List, Optional
import aiohttp
from pydantic import BaseModel
from dhisana.schemas.sales import ContentGenerationContext
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.generate_structured_output_internal import (
    get_structured_output_with_assistant_and_vector_store,
    get_structured_output_with_o1
)

# ---------------------------------------------------------------------------------------
# MODEL
# ---------------------------------------------------------------------------------------
class InboundEmailTriageResponse(BaseModel):
    """
    Model representing the structured response for an inbound email triage.
    - triage_status: "AUTOMATIC" or "REQUIRES_APPROVAL"
    - triage_reason: Reason text if triage_status == "REQUIRES_APPROVAL"
    - response_action_to_take: The recommended next action (e.g. SCHEDULE_MEETING, SEND_REPLY, etc.)
    - response_message: The actual body of the email response to be sent or used for approval.
    """
    triage_status: str  # "AUTOMATIC" or "REQUIRES_APPROVAL"
    triage_reason: Optional[str]
    response_action_to_take: str
    response_message: str

# ---------------------------------------------------------------------------------------
# HELPER FUNCTION TO CLEAN CONTEXT
# ---------------------------------------------------------------------------------------
def cleanup_reply_email_context(email_context: ContentGenerationContext) -> ContentGenerationContext:
    clone_context = email_context.copy(deep=True)
    clone_context.external_source_fileIds = {}
    # If you do NOT want to use vector store for triage, you can unset it here:
    # clone_context.external_openai_vector_store_id = None

    clone_context.lead_info.task_ids = None
    clone_context.lead_info.email_validation_status = None
    clone_context.lead_info.linkedin_validation_status = None
    clone_context.lead_info.research_status = None
    clone_context.lead_info.enchrichment_status = None
    return clone_context

# ---------------------------------------------------------------------------------------
# CORE FUNCTION TO GENERATE SINGLE RESPONSE (ONE VARIATION)
# ---------------------------------------------------------------------------------------
async def generate_inbound_email_response_copy(
    email_context: ContentGenerationContext,
    variation: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Generate a single inbound email triage response based on the provided context and
    a specific variation prompt.
    """
    allowed_actions = [
        "SCHEDULE_MEETING",
        "SEND_REPLY",
        "UNSUBSCRIBE",
        "OOF_MESSAGE",
        "NOT_INTERESTED",
        "NEED_MORE_INFO",
        "FORWARD_TO_OTHER_USER",
        "NO_MORE_IN_ORGANIZATION",
        "OBJECTION_RAISED",
        "OTHER"
    ]
    
    cleaned_context = cleanup_reply_email_context(email_context)

    # Build the prompt, adding the variation text for stylistic or structural changes.
    prompt = f"""
    You are a specialized email assistant. 
    Your task is to analyze the user's email thread, the user/company info,
    and the provided triage guidelines to craft a response.

    Variation Style or Focus: {variation}

    1. Understand the email thread:
       {cleaned_context.current_email_thread}

    2. User & Company (Lead) Info:
       {cleaned_context.model_dump()}

    3. Triage Guidelines:
       {cleaned_context.email_triage_guidelines}

       - If the request is standard, simple, or obviously handled by standard processes,
         set triage_status to "AUTOMATIC".
       - If the request is complex, sensitive, or needs special input,
         set triage_status to "REQUIRES_APPROVAL" and provide triage_reason.

    4. Choose one action from this list: {allowed_actions}

    5. Provide your recommended email body that best addresses the user's message.

    DO NOT reply to any PII or financial information requests; triage them as "REQUIRES_APPROVAL".

    Your final output must be valid JSON with the structure:
    {{
      "triage_status": "AUTOMATIC" or "REQUIRES_APPROVAL",
      "triage_reason": "<reason if requires approval; otherwise null>",
      "response_action_to_take": "<chosen action>",
      "response_message": "<the email body to respond with>"
    }}
    """

    # If there's a vector store ID, use that approach
    if cleaned_context.external_openai_vector_store_id:
        response, status = await get_structured_output_with_assistant_and_vector_store(
            prompt=prompt,
            response_format=InboundEmailTriageResponse,
            vector_store_id=cleaned_context.external_openai_vector_store_id,
            tool_config=tool_config
        )
    else:
        response, status = await get_structured_output_with_o1(
            prompt=prompt,
            response_format=InboundEmailTriageResponse,
            tool_config=tool_config
        )

    if status != "SUCCESS":
        raise Exception("Error in generating the inbound email triage response.")

    return response.model_dump()

# ---------------------------------------------------------------------------------------
# MAIN ENTRY POINT - GENERATE MULTIPLE VARIATIONS
# ---------------------------------------------------------------------------------------
@assistant_tool
async def generate_inbound_email_response_variations(
    email_context: ContentGenerationContext,
    number_of_variations: int = 3,
    tool_config: Optional[List[Dict]] = None
) -> List[Dict[str, Any]]:
    """
    Generate multiple inbound email triage responses, each with a different 'variation'.
    Returns a list of dictionaries conforming to InboundEmailTriageResponse.
    """
    # Example variation frameworks or prompts
    variation_specs = [
        "Short and friendly response focusing on quick resolution.",
        "More formal tone referencing user’s key points in the thread.",
        "Meeting-based approach if user needs further discussion or demo.",
        "Lean approach focusing on clarifying user’s questions or concerns.",
        "Solution-driven approach referencing a relevant product or case study."
    ]
    
    all_variations = []
    for i in range(number_of_variations):
        variation_text = variation_specs[i % len(variation_specs)]
        
        try:
            triaged_response = await generate_inbound_email_response_copy(
                email_context,
                variation_text,
                tool_config=tool_config
            )
            all_variations.append(triaged_response)
        except Exception as e:
            raise e

    return all_variations
