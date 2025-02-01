import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

from dhisana.utils.generate_structured_output_internal import get_structured_output_with_o1
from dhisana.utils.workflow_code_model import WorkflowPythonCode

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_code_for_campaign_cadence(
    english_description: str,
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> Tuple[Dict[str, Any], str]:
    """
    Generate a workflow code (Python code) from an English description.
    
    The function produced will be named:
        async def run_campaing_cadence(input_leads, campaign_context, tool_config) -> str
    Returns: (response_dict, status_string)
    """
    system_message = (
        "You are a helpful AI assistant and an expert Python coder. "
        "Convert the English description provided by the user into an executable Python function named "
        "'run_campaing_cadence', with the signature:\n"
        "    async def run_campaing_cadence(input_leads, campaign_context, tool_config) -> str\n"
        "The function should iterate over 'input_leads' and perform the required LinkedIn actions via execute_task. "
        "Valid commands include: "
        "    view_linkedin_profile, send_connection_request, like_recent_post, send_linkedin_message, get_current_messages, save_lead.\n"
        "Return 'SUCCESS' or 'ERROR' as a string."
    )

    example_of_workflow_code = (
        '''
        async def run_campaing_cadence(input_leads, campaign_context, tool_config):
            """
            Example skeleton. Run a linkedin campaign cadence with actions like view_profile, send_linkedin_message etc.
            Returns "SUCCESS" or "ERROR".
            """
            
            # Make sure required imports are there within the function definition itself.
            import asyncio
            import logging
            from typing import Any, Dict, List, Optional, Tuple
            from dhisana.utils.agent_task import execute_task
            from dhisana.utils.generate_linkedin_connect_message import get_personalized_linkedin_message
            
            # Make sure logger is defined and the logging library is imported within the function.
            logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)
        
            try:
                MAX_ACTIONS = {
                    "view_profile": 30,
                    "send_connection_request": 10,
                    "send_linkedin_message": 10,
                    "like_post": 10
                }

                # View profiles
                for lead in input_leads[:MAX_ACTIONS["view_profile"]]:
                    await execute_task(
                        command_name="view_linkedin_profile",
                        command_args={"user_linkedin_salesnav_url": lead.get("user_linkedin_salesnav_url")},
                        tool_config=tool_config
                    )
                    logger.debug("Viewed profile: %s", lead.get("full_name"))

                # Send connection requests
                for lead in input_leads[:MAX_ACTIONS["send_connection_request"]]:
                    await execute_task(
                        command_name="send_connection_request",
                        command_args={
                            "user_linkedin_salesnav_url": lead.get("user_linkedin_salesnav_url"),
                            "lead_info": lead,
                            "context": campaign_context
                        },
                        tool_config=tool_config
                    )
                    logger.debug("Sent connection request: %s", lead.get("full_name"))

                # Send messages
                for lead in input_leads[:MAX_ACTIONS["send_linkedin_message"]]:
                    await execute_task(
                        command_name="send_linkedin_message",
                        command_args={
                            "user_linkedin_salesnav_url": lead.get("user_linkedin_salesnav_url"),
                            "lead_info": lead,
                            "context": campaign_context
                        },
                        tool_config=tool_config
                    )
                    logger.debug("Sent message to: %s", lead.get("full_name"))

                # Like recent posts
                for lead in input_leads[:MAX_ACTIONS["like_post"]]:
                    await execute_task(
                        command_name="like_recent_post",
                        command_args={"user_linkedin_salesnav_url": lead.get("user_linkedin_salesnav_url")},
                        tool_config=tool_config
                    )
                    logger.debug("Liked recent post for lead: %s", lead.get("full_name"))

                logger.info("Completed run_campaing_cadence successfully.")
                return "SUCCESS"

            except Exception as e:
                logger.exception("Exception in run_campaing_cadence: %s", e)
                return "ERROR"
        '''
    )

    user_prompt = f"""
    {system_message}
    "Make sure the imports are present within the function definition itself. Make sure the logging library is imported and logger defined within the function. "
    The user wants to generate Python code that does this:

    \"{english_description}\"

    Here is an example workflow code:
    {example_of_workflow_code}

    The final code must be valid Python, and must produce:
      async def run_campaing_cadence(input_leads, campaign_context, tool_config) -> str

    Return your final output as valid JSON with:
    {{
      "workflow_python_code": "<the python code here>"
    }}
    """
    response, status = await get_structured_output_with_o1(
        user_prompt, WorkflowPythonCode, tool_config=tool_config
    )
    return response.model_dump(), status


class CampaignContext(BaseModel):
    instructions: str


async def generate_campaign_cadence_workflow_and_execute(
    instructions: str,
    input_leads: List[Dict[str, Any]],
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Generate the campaign cadence workflow code from the user query, 
    then execute it on the provided input_leads.

    Returns:
        JSON string describing success or error.
    """
    response, status = await generate_code_for_campaign_cadence(
        instructions, tool_config=tool_config
    )

    # Check if we have a successful code generation
    if status == "SUCCESS" and response and response.get("workflow_python_code"):
        code = response["workflow_python_code"]
        if not code:
            return json.dumps({"error": "No workflow code generated.", "status": status})

        logger.info("Generated workflow code:\n%s", code)

        local_vars = {}
        global_vars = {}

        try:
            # Execute the generated code; expect a function named `run_campaing_cadence`
            exec(code, global_vars, local_vars)
            campaign_fn = local_vars.get("run_campaing_cadence", None)
            if campaign_fn is None:
                raise RuntimeError("No 'run_campaing_cadence' function found in generated code.")

            # Helper to call the newly generated async function
            async def run_campaign(leads, campaign_context, cfg):
                return await campaign_fn(leads, campaign_context, cfg)

            try:
                campaign_context = CampaignContext(instructions=instructions)
                result = await run_campaign(input_leads, campaign_context, tool_config)
            except Exception as e:
                logger.exception("Error occurred while running run_campaing_cadence.")
                return json.dumps({"status": "ERROR", "error": str(e)})

            # If it's not "SUCCESS", treat it as an error
            if not result or result != "SUCCESS":
                return json.dumps({"error": "Error running the workflow code.", "status": "ERROR"})

            return json.dumps({"status": "SUCCESS"})

        except Exception as e:
            logger.exception("Exception occurred while executing generated code.")
            return json.dumps({"status": "ERROR", "error": str(e)})

    # If code generation failed or no code snippet was returned
    return json.dumps({"error": "No valid workflow code generated.", "status": status})
