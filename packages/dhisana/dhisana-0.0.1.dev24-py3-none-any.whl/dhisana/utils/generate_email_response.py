# Import necessary modules
import base64
from typing import Any, Dict, List, Optional
import aiohttp
from pydantic import BaseModel
from dhisana.schemas.sales import EmailContentContext
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.generate_structured_output_internal import get_structured_output_with_assistant_and_vector_store, get_structured_output_with_o1

class InboundEmailTriageResponse(BaseModel):
    """
    Model representing the structured response for an inbound email triage.
    - triage_status: "AUTOMATIC" or "REQUIRES_APPROVAL"
    - triage_reason: Reason text if triage_status == "REQUIRES_APPROVAL"
    - response_action_to_take: The recommended next action (e.g. SCHEDULE_MEETING, SEND_REPLY, etc.)
    - response_message: The actual body of the email response that can be sent to the user or used for approval.
    """
    triage_status: str  # "AUTOMATIC" or "REQUIRES_APPROVAL"
    triage_reason: Optional[str]
    response_action_to_take: str
    response_message: str
    
def cleanup_reply_email_context(email_context: EmailContentContext) -> EmailContentContext:
    clone_context = email_context.copy(deep=True)
    clone_context.external_source_fileIds = {}
    clone_context.external_openai_vector_store_id = None
    clone_context.lead_info.task_ids = None
    clone_context.lead_info.email_validation_status = None
    clone_context.lead_info.linkedin_validation_status = None
    clone_context.lead_info.research_status = None
    clone_context.lead_info.enchrichment_status = None
    return clone_context

@assistant_tool
async def generate_inbound_email_response(
    email_context: EmailContentContext,
    email_thread: str,
    triage_guidelines: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Generate an inbound email response, including a triage section to determine if the reply
    can be sent automatically or requires human approval.

    Parameters:
    -----------
    user_info : Dict[str, Any]
        Information about the user who sent the email.
    email_thread : str
        The conversation or email thread text so far.
    company_info : Dict[str, Any]
        Information about the sender's company (or the recipient's company context).
    triage_guidelines : str
        Additional instructions or guidelines on how to triage or handle the response.
    tool_config : Optional[List[Dict]]
        Configuration for the tool (e.g., model settings, etc.). Defaults to None.

    Returns:
    --------
    Dict[str, Any]
        A dictionary with the following keys:
        {
          "triage_status": str,  # "AUTOMATIC" or "REQUIRES_APPROVAL"
          "triage_reason": Optional[str],
          "response_action_to_take": str,
          "response_message": str
        }

    Raises:
    -------
    Exception
        If there's an error in generating a structured LLM response.
    """
    # You can adjust the action list to match your application's needs
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

    # Construct a prompt instructing the LLM to:
    # 1) Understand the user email context and conversation thread
    # 2) Use triage guidelines to decide if the response is automatic or requires approval
    # 3) Provide a reason if approval is required
    # 4) Suggest the appropriate action to take from the allowed list
    # 5) Propose a response message that can be sent to the user or used for approval
    prompt = f"""
    You are a specialized email assistant. 
    Your task is to analyze the user's email thread, the user and company information, 
    and the provided triage guidelines to craft a response.

    1. Understand the email thread:
       {email_thread}

    2. Know about the user and their company:
       Lead Information & Campaign Details provided by user below:
       {cleaned_context.model_dump()}

    3. Follow these triage guidelines to decide if we can reply automatically or need approval:
       {triage_guidelines}

       - If the request is standard, simple, or obviously handled by our standard processes, 
         set triage_status to "AUTOMATIC".
       - If the request is complex, sensitive, or needs managerial/legal input, 
         set triage_status to "REQUIRES_APPROVAL" and provide a triage_reason.

    4. Decide an appropriate action from this list: {allowed_actions}

    5. Provide your recommended email body that best addresses the user's message.

    DO NOT reply on any PII information request of financial information and move such requests to REQUIRES_APPROVAL.
    
    Your final output must be valid JSON with the structure:
    {{
      "triage_status": "AUTOMATIC" or "REQUIRES_APPROVAL",
      "triage_reason": "<reason if requires approval; otherwise null>",
      "response_action_to_take": "<chosen action>",
      "response_message": "<the email body to respond with>"
    }}
    """

    if email_context.external_openai_vector_store_id:
        # Use the utility that ensures we get a structured JSON fitting our Pydantic model
        response, status = await get_structured_output_with_assistant_and_vector_store(prompt=prompt, 
                                                                                    response_format=InboundEmailTriageResponse, 
                                                                                    vector_store_id=email_context.external_openai_vector_store_id, 
                                                                                    tool_config=tool_config)
    else:
        response, status = await get_structured_output_with_o1(prompt, InboundEmailTriageResponse, tool_config=tool_config)

    # Raise an error if the LLM processing fails
    if status != "SUCCESS":
        raise Exception("Error in generating the inbound email triage response.")

    # Return the structured result as a dictionary
    return response.model_dump()