from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from dhisana.schemas.sales import ContentGenerationContext
from dhisana.utils.generate_structured_output_internal import (
    get_structured_output_with_o1,
    get_structured_output_with_assistant_and_vector_store
)
from dhisana.utils.assistant_tool_tag import assistant_tool

# ---------------------------------------------------------------------------------------
# MODEL
# ---------------------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------------------
def cleanup_reply_linkedin_context(linkedin_context: ContentGenerationContext) -> ContentGenerationContext:
    """
    Create a copy of the context and remove unneeded or sensitive fields.
    """
    clone_context = linkedin_context.copy(deep=True)
    
    # Remove or nullify external file references / IDs if not needed
    clone_context.external_source_fileIds = {}
    # If you do NOT want to use the vector store for triage, set it to None:
    # clone_context.external_openai_vector_store_id = None

    # Example: removing tasks or statuses that are not needed for triage
    clone_context.lead_info.task_ids = None
    clone_context.lead_info.research_status = None
    clone_context.lead_info.email_validation_status = None
    clone_context.lead_info.linkedin_validation_status = None
    clone_context.lead_info.enchrichment_status = None
    
    return clone_context


async def generate_linkedin_response_message_copy(
    linkedin_context: ContentGenerationContext,
    variation: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Generates a single variation of a triaged LinkedIn response using the provided context.
    Returns a structured result conforming to LinkedInTriageResponse.
    """
    allowed_actions = [
        "SEND_REPLY",        # Normal: send reply
        "WAIT_TO_SEND",      # Wait because user was recently messaged
        "STOP_SENDING",      # No more messages to user
        "SCHEDULE_MEETING",  # If user requests a meeting
        "FOLLOW_UP_LATER",
        "NEED_MORE_INFO",
        "OTHER"
    ]
    
    cleaned_context = cleanup_reply_linkedin_context(linkedin_context)

    # For demonstration, assume your context has these attributes:
    #   linkedin_context.outreach_context
    #   linkedin_context.connect_template
    #   linkedin_context.current_conversations
    #   linkedin_context.additional_instructions
    #   linkedin_context.lead_info (dict-like with user data)
    # Adjust as needed based on your actual ContentGenerationContext definition.
    prompt = f"""
    You are a specialized LinkedIn assistant.

    Your task:
      1. Analyze the current LinkedIn conversation.
      2. Inspect the user (lead) info, outreach campaign context, and any additional instructions.
      3. Decide whether to automatically send a reply or if human approval is needed (triage).
      4. If approval is needed, provide the reason.
      5. Choose one recommended next action from: {allowed_actions}.
      6. Provide a short LinkedIn message body that addresses the lead's conversation.

    Variation / Style: {variation}

    Current linkedin thread:
    {cleaned_context.current_linkedin_thread}

    Lead & Outreach (Campaign) Context:
    {cleaned_context.model_dump()}

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

    # Decide if we use a vector store
    if cleaned_context.external_openai_vector_store_id:
        response, status = await get_structured_output_with_assistant_and_vector_store(
            prompt=prompt,
            response_format=LinkedInTriageResponse,
            vector_store_id=cleaned_context.external_openai_vector_store_id,
            tool_config=tool_config
        )
    else:
        response, status = await get_structured_output_with_o1(
            prompt=prompt,
            response_format=LinkedInTriageResponse,
            tool_config=tool_config
        )

    if status != 'SUCCESS':
        raise Exception("Error in generating the triaged LinkedIn message.")
    
    return response.model_dump()


# ---------------------------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------------------------
@assistant_tool
async def get_linkedin_response_message_variations(
    linkedin_context: ContentGenerationContext,
    number_of_variations: int = 3,
    tool_config: Optional[List[Dict]] = None
) -> List[Dict[str, Any]]:
    """
    Generates multiple variations of a triaged LinkedIn message and returns them all.
    Each variation is a dict conforming to LinkedInTriageResponse with keys:
        - triage_status
        - triage_reason
        - response_action_to_take
        - response_message
    """
    # Example set of variation specs – feel free to tailor them
    variation_specs = [
        "Friendly, short response with empathetic tone.",
        "Direct response referencing user’s last message or question.",
        "Meeting-oriented approach if the user seems interested in a deeper discussion.",
        "Longer, more detailed approach – reference relevant success stories or context.",
        "Minimalistic approach focusing on primary CTA only."
    ]

    triaged_responses = []
    for i in range(number_of_variations):
        try:
            variation_style = variation_specs[i % len(variation_specs)]
            triaged_response = await generate_linkedin_response_message_copy(
                linkedin_context=linkedin_context,
                variation=variation_style,
                tool_config=tool_config
            )
            triaged_responses.append(triaged_response)
        except Exception as e:
            # You may want to log or handle the error
            raise e

    return triaged_responses
