# Import necessary modules
import os
from typing import Any, Dict, List, Optional
import aiohttp
from pydantic import BaseModel
from dhisana.schemas.sales import ContentGenerationContext, Lead, PromptEngineeringGuidance
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.generate_structured_output_internal import get_structured_output_with_o1, get_structured_output_with_assistant_and_vector_store    

# Define a model for email copy information
class EmailCopy(BaseModel):
    subject: str
    body: str

def cleanup_email_context(email_context: ContentGenerationContext) -> ContentGenerationContext:
    clone_context = email_context.copy(deep=True)
    clone_context.external_source_fileIds = {}
    clone_context.external_openai_vector_store_id = None
    clone_context.lead_info.task_ids = None
    clone_context.lead_info.email_validation_status = None
    clone_context.lead_info.linkedin_validation_status = None
    clone_context.lead_info.research_status = None
    clone_context.lead_info.enchrichment_status = None
    return clone_context

async def generate_personalized_email_copy(
    email_context: ContentGenerationContext,
    variation: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Generate a personalized email copy using provided lead and campaign information with a template.

    This function sends an asynchronous request to generate an email copy based on the provided lead information and template.
    
    Parameters:
    emailcontext: Information about the lead, campaign.
    tool_config (Optional[List[Dict]]): Configuration for the tool (default is None).

    Returns:
    dict: The JSON response containing the email subject and body.

    Raises:
    Exception: If there is an error in processing the request.
    """
    cleaned_context = cleanup_email_context(email_context)
    prompt = f"""
    Hi AI Assistant,

    You’re an expert at crafting professional, concise, and compelling emails.
    Use the details below to ensuring personalization, a clear value proposition,
    and adherence to the specified email template. Avoid spam triggers or irrelevant info.

    **Important**: 
    1. The final answer must be a JSON object containing only the fields 'subject' and 'body'.
    2. This is final copy of the email to be sent to the lead directly. DO NOT include any placeholders, comments or instructions in the final output.
    3. If file_search is provided check if there are any relevant files to help provide more context for email.

    
    The attached files have relevant information on case studies, product details, and customer testimonials.

    Steps:
    1. Summarize the user’s role and experience.
    2. Summarize the company and what it does.
    3. Check if the file_search tool is provided and has more context like case studies, customer testimonials, or industry use cases to help provide more context.
    4. Highlight how our product offering/campaign aligns with the user’s needs and company goals.
    5. Craft a personalized email with a compelling reason to reach out and a clear CTA.

    Pro Tips for B2B Enterprise Emails:
    - Personalization: Reference the prospect’s role, recent activities, relevant vertical solutions, or any mutual connections.
    - Brevity: Keep it concise.
    - Social Proof: Mention relevant success stories if applicable.
    - Clear CTA: End with a single call to action.

    Lead Information & Campaign Details provided by user below:
    {cleaned_context.model_dump()}

    Sender Info (Signature Use):
    - sender_first_name: str
    - sender_last_name: str

    Lead Info:
    - lead_info: Lead

    Output Format (JSON):
    {{
        "subject": "Personalized subject line.",
        "body": "Personalized email body content."
    }}

    Use the following info for this variation:
    {variation}

    After writing, review the content for relevance, clarity, and professionalism.
    Use personalization ONLY when relevant for the campaign and product; don’t add irrelevant details
    such as city or school information. DO NOT USE any user identifiers, PII, tracking IDs, internal
    information like deal size, or any other sensitive information in email body generated.
    """
    
    if  email_context.external_openai_vector_store_id:
        response, status = await get_structured_output_with_assistant_and_vector_store(prompt=prompt, 
                                                                                   response_format=EmailCopy, 
                                                                                   vector_store_id=email_context.external_openai_vector_store_id, 
                                                                                   tool_config=tool_config)
    else:
        response, status = await get_structured_output_with_o1(prompt, EmailCopy, tool_config=tool_config)

    if status != 'SUCCESS':
        raise Exception("Error in generating the personalized email.")
    return response.model_dump()

@assistant_tool
async def generate_personalized_email(
    email_context: ContentGenerationContext,
    number_of_variations: int = 3,
    tool_config: Optional[List[Dict]] = None
):
    """
    Generate a personalized email copy using provided lead and campaign information with a template.

    Parameters:
        email_context (EmailContentContext): Information about the lead, campaign.
        number_of_variations (int): Number of email variations to generate.
        tool_config (Optional[List[Dict]]): Configuration for the tool (default is None).

    Returns:
        List[dict]: The JSON response containing the email subject and body.

    Raises:
        Exception: If there is an error in processing the request.
    """
    variation_specs = [
        "Use PAS (Problem, Agitate, Solve) framework to write up email.",
        "Use VETO framework (Value, Evidence, Tie, Offer) to compose email.Explain how the product addresses the company’s current goals and requirements.",
        "Use AIDA framework (Attention, Interest, Desire, Action) to compose email.",
        "Use SPIN (Situation, Problem, Implication, Need-Payoff) framework to write up email.",
        "Use BANT (Budget, Authority, Need, Timeline) framework to write up email.",
        "Use P-S-B (Pain, Solution, Benefit) framework to write up email."
        "Use The 3-Bullet Approach (1. Industry Trend or Pain, 2. Value Statement 3. Simple Ask) framework to write up email. Keep it under 100 words."
        "Use Hook, Insight, Offer framework to write up email."
    ]
    email_variations = []
    for i in range(number_of_variations):
        try:
            email_copy = await generate_personalized_email_copy(
                email_context,
                variation_specs[i % 3],
                tool_config
            )
            email_variations.append(email_copy)
        except Exception as e:
            raise e
    return email_variations
