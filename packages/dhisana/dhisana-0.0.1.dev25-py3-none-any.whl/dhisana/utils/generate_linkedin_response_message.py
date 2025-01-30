from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from dhisana.utils.generate_structured_output_internal import (
    get_structured_output_with_o1
)

class LinkedInTriageResponse(BaseModel):
    """
    Model representing the structured response for a LinkedIn conversation triage.
    - triage_status: "AUTOMATIC" or "REQUIRES_APPROVAL"
    - triage_reason: Optional reason text if triage_status == "REQUIRES_APPROVAL"
    - response_action_to_take: The recommended next action (e.g., SEND_REPLY, WAIT_TO_SEND, STOP_SENDING, etc.)
    - response_message: The actual message (body) to be sent or used for approval.
    """
    triage_status: str  # "AUTOMATIC" or "REQUIRES_APPROVAL"
    triage_reason: Optional[str]
    response_action_to_take: str
    response_message: str


def cleanup_reply_linkedin_context(lead_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clone or sanitize the lead info to remove unneeded or sensitive fields.
    """
    cleaned_lead_info = dict(lead_info)  # Shallow copy

    # Example of removing or masking unwanted fields
    cleaned_lead_info.pop("task_ids", None)
    cleaned_lead_info.pop("research_status", None)
    # Add more fields you want to remove as needed

    return cleaned_lead_info


async def generate_linkedin_response_message(
    lead_info: Dict[str, Any],
    outreach_context: str,
    connect_template: str,
    current_conversations: str,
    additional_instructions: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Generate a triaged LinkedIn message, deciding if it can be sent automatically
    or requires human approval. The final JSON structure must conform to
    LinkedInTriageResponse (triage_status, triage_reason, response_action_to_take, response_message).

    The content should be genuine, authentic, and professional, avoiding clichés
    and heavy sales pushes. It should be respectful of user preferences (e.g., not
    spamming a user who has shown disinterest).
    """

    # Possible actions for spam-avoidance, scheduling, and response
    allowed_actions = [
        "SEND_REPLY",        # Normal: send reply
        "WAIT_TO_SEND",      # Wait because user was recently messaged
        "STOP_SENDING",      # No more messages to user
        "SCHEDULE_MEETING",  # If user requests a meeting
        "FOLLOW_UP_LATER",
        "NEED_MORE_INFO",
        "OTHER"
    ]

    cleaned_lead_info = cleanup_reply_linkedin_context(lead_info)

    # Incorporate the outreach context and guidelines directly in the prompt
    prompt = f"""
    You are a specialized LinkedIn assistant.

    Your task:
      1. Analyze the current LinkedIn conversation.
      2. Inspect the user (lead) info, outreach campaign context, and any additional instructions.
      3. Decide whether to automatically send a reply or if human approval is needed (triage).
      4. If approval is needed, provide the reason.
      5. Choose one recommended next action from: {allowed_actions}.
      6. Provide a short LinkedIn message body that addresses the lead's conversation.

    Connect Template (for reference):
    {connect_template}

    Outreach (Campaign) Context:
    {outreach_context}

    Additional Instructions (Triage Guidelines):
    {additional_instructions}

    Current Conversations:
    {current_conversations}

    Lead Info:
    {cleaned_lead_info}

    === IMPORTANT ANTI-SPAM AND RESPECT RULES ===
    1. If we have sent a message to the user within the past 24 hours and the user has not responded,
       do NOT send another message right now. Instead, triage with "WAIT_TO_SEND".
    2. If we have sent more than 3 messages in total without any user response, do NOT send another message.
       Instead, triage with "STOP_SENDING".
    3. If the user explicitly says "don't reply", "not interested", or any equivalent,
       do NOT continue the thread. Triage with "STOP_SENDING".
    4. If the user has requested a meeting, triage as "AUTOMATIC" or "REQUIRES_APPROVAL" 
       (depending on complexity), and set response_action_to_take to "SCHEDULE_MEETING".
       Craft a helpful response for scheduling.

    === TONE AND STYLE RULES ===
    - Your message must be genuine, authentic, and professional.
    - Avoid clichés and spammy or overly aggressive sales pitches.
    - Do not push sales in an unnatural way.

    === OUTPUT FORMAT ===
    Your final output must be valid JSON in this exact format:
    {{
      "triage_status": "AUTOMATIC" or "REQUIRES_APPROVAL",
      "triage_reason": "<reason if REQUIRES_APPROVAL; else empty or null>",
      "response_action_to_take": "<one of {allowed_actions}>",
      "response_message": "<the new or reply message>"
    }}
    """

    # Decide how to call your structured output function (based on vector store or not).
    # We'll assume there's no vector store ID for LinkedIn. If you do have one, adapt similarly.
    response, status = await get_structured_output_with_o1(
        prompt=prompt,
        response_format=LinkedInTriageResponse,
        tool_config=tool_config
    )

    if status != 'SUCCESS':
        raise Exception("Error in generating the triaged LinkedIn message.")
    
    return response.model_dump()


async def get_linkedin_response_message(
    lead_info: Dict[str, Any],
    outreach_context: str,
    current_conversations: str,
    additional_instructions: str,
    tool_config: Optional[List[Dict]] = None
) -> str:
    """
    Returns only the 'response_message' from the triaged LinkedIn response.
    This includes usage of the outreach (campaign) context to better tailor
    the message to the lead.
    """
    connect_template = """
    Hi <<first_name>>,
    << message >>
    Thanks,
    << sender_name >>
    """

    triaged_response = await generate_linkedin_response_message(
        lead_info=lead_info,
        outreach_context=outreach_context,
        connect_template=connect_template,
        current_conversations=current_conversations,
        additional_instructions=additional_instructions,
        tool_config=tool_config
    )
    return triaged_response.get("response_message", "")
