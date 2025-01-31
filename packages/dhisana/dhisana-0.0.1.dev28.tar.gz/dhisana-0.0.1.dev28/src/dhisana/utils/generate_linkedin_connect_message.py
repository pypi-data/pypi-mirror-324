# Import necessary modules
from typing import Dict, List, Optional
from pydantic import BaseModel
from dhisana.schemas.sales import ContentGenerationContext
from dhisana.utils.generate_structured_output_internal import (
    get_structured_output_with_o1,
    get_structured_output_with_assistant_and_vector_store
)
from dhisana.utils.assistant_tool_tag import assistant_tool

# Define a model for the LinkedIn connection message
class LinkedInConnectMessage(BaseModel):
    subject: str
    body: str

def cleanup_linkedin_context(linkedin_context: ContentGenerationContext) -> ContentGenerationContext:
    """
    Removes or nullifies fields from the context that are not needed
    or may cause confusion in LinkedIn generation logic.
    """
    clone_context = linkedin_context.copy(deep=True)
    clone_context.external_source_fileIds = {}
    clone_context.external_openai_vector_store_id = None
    
    # Cleanup lead_info if needed
    clone_context.lead_info.task_ids = None
    clone_context.lead_info.email_validation_status = None
    clone_context.lead_info.linkedin_validation_status = None
    clone_context.lead_info.research_status = None
    clone_context.lead_info.enchrichment_status = None
    return clone_context

async def generate_personalized_linkedin_message_copy(
    linkedin_context: ContentGenerationContext,
    variation: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict:
    """
    Generate a personalized LinkedIn connection message using provided
    lead and campaign information with a template. Similar to the email approach.
    """
    cleaned_context = cleanup_linkedin_context(linkedin_context)

    prompt = f"""
    Hi AI Assistant,

    You’re an expert at crafting professional, concise, and compelling LinkedIn connection requests.
    Use the details below to ensure personalization, a clear value proposition,
    and adherence to the specified LinkedIn template. Avoid spam triggers or irrelevant info.

    **Important**: 
    1. The final answer must be a JSON object containing only 'subject' and 'body'.
    2. This is the final copy of the LinkedIn message to be sent directly to the lead. 
       DO NOT include any placeholders, comments, or instructions in the final output.
    3. If file_search is provided, check if there are relevant files to help 
       provide more context for the LinkedIn message.

    Steps:
    1. Summarize the user’s role and experience.
    2. Summarize the company and what it does.
    3. If file_search/tool is provided, incorporate any relevant case studies, testimonials, or industry use cases.
    4. Highlight how our product offering/campaign aligns with the user’s goals or challenges.
    5. Craft a concise LinkedIn connection request with a compelling reason to connect and a friendly sign-off.

    Pro Tips for LinkedIn Outreach:
    - Personalization: Reference the prospect’s role, recent activities, or industry vertical.
    - Keep it short: LinkedIn messages should be concise and value-driven.
    - Social Proof: Mention relevant success stories if applicable.
    - Clear CTA or Reason to Connect: Provide a single reason or next step.

    Lead Information & Campaign Details provided by user:
    {cleaned_context.model_dump()}

    Use the following info for this variation:
    {variation}

    Output Format (JSON):
    {{
        "subject": "Brief, personalized subject line for LinkedIn connection.",
        "body": "Concise LinkedIn connection message."
    }}

    After writing, review the content for relevance, clarity, and professionalism.
    DO NOT use irrelevant personal details (like city, school, or internal data).
    DO NOT include placeholders in the final message.
    """

    if linkedin_context.external_openai_vector_store_id:
        response, status = await get_structured_output_with_assistant_and_vector_store(
            prompt=prompt,
            response_format=LinkedInConnectMessage,
            vector_store_id=linkedin_context.external_openai_vector_store_id,
            tool_config=tool_config
        )
    else:
        response, status = await get_structured_output_with_o1(
            prompt,
            LinkedInConnectMessage,
            tool_config=tool_config
        )

    if status != "SUCCESS":
        raise Exception("Error in generating the personalized LinkedIn message.")
    
    return response.model_dump()

@assistant_tool
async def generate_personalized_linkedin_message(
    linkedin_context: ContentGenerationContext,
    number_of_variations: int = 3,
    tool_config: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    Generate multiple variations of a personalized LinkedIn connection message
    using provided lead/campaign information with a template.

    :param linkedin_context: Information about the lead, campaign, and template.
    :param number_of_variations: Number of LinkedIn message variations to generate.
    :param tool_config: Optional config for the tool or vector store usage.
    :return: A list of dictionaries, each containing 'subject' and 'body'.
    """
    # Example frameworks or variation prompts (You can adapt or expand as needed)
    variation_specs = [
        "Use a friendly introduction that references their role, then provide a quick reason for connecting.",
        "Use a social-proof approach referencing a relevant success story or industry insight.",
        "Use a concise 2-3 sentence approach highlighting a mutual interest or shared connection.",
        "Use a P-S-B (Pain, Solution, Benefit) style in under 60 words.",
        "Use the 3-Bullet Approach: 1) Industry/Pain, 2) Value Statement, 3) Simple Ask."
    ]

    linkedin_variations = []
    for i in range(number_of_variations):
        try:
            linkedin_copy = await generate_personalized_linkedin_message_copy(
                linkedin_context,
                variation_specs[i % len(variation_specs)],
                tool_config
            )
            linkedin_variations.append(linkedin_copy)
        except Exception as e:
            # You may want to log the error or handle it more gracefully.
            raise e
    return linkedin_variations
