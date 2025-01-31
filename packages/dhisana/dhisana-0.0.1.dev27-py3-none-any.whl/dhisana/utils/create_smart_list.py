import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from dhisana.utils.generate_structured_output_internal import get_structured_output_with_o1
from dhisana.utils.workflow_code_model import WorkflowPythonCode

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_smart_list_creation_code(
    english_description: str,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[Dict[str, Any], str]:
    """
    Generate a workflow code (Python code) from an English description.
    
    Returns:
        A tuple of:
         - A dict containing {'workflow_python_code': '...'}.
         - A string representing status, e.g., 'SUCCESS' or 'ERROR'.
    """
    system_message = (
        "You are a helpful AI assistant who is expert python coder. I want you to convert an English description "
        "of a requirement provided by user into an executable Python function called create_smart_list. "
        "Your output must be valid Python code. The provided example shows how the structure looks like and "
        "what methods you can use.\n"
        "Your output must be valid Python code. The provided example shows how the structure looks like and what methods you can use. "
        "Make sure required imports and logger is defined within the function. "
        "Use the output function signature:\n"
        "    async def create_smart_list(input_leads_list, tool_config)\n"
    )

    # UPDATED EXAMPLE OF WORKFLOW CODE BELOW
    example_of_workflow_code = (
        '''
        async def create_smart_list(input_leads_list, tool_config):
            """
            Example skeleton. Deduplicate leads, perform checks for signals, add the intent_score to each lead,
            then sort by intent_score (descending) and return qualified leads.
            Returns ("SUCCESS", sorted_qualified_leads) or ("ERROR", []).
            """
            
            # Make sure the imports are there withing this function defined.
            import asyncio
            import logging
            from typing import Any, Dict, List, Optional, Tuple
            from dhisana.utils.check_for_intent_signal import check_for_intent_signal

            # Make sure logger is defined withing the function.
            logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)
            
            try:
                logger.info("Starting custom_workflow execution")

                # Step 1 : Deduplicate leads by user_linkedin_url or user_linkedin_salesnav_url
                leads_with_linkedin = {}
                leads_with_salesnav = {}

                for lead in input_leads_list:
                    user_linkedin_url = lead.get("user_linkedin_url")
                    user_linkedin_salesnav_url = lead.get("user_linkedin_salesnav_url")
                    if user_linkedin_url:
                        leads_with_linkedin[user_linkedin_url] = lead
                    elif user_linkedin_salesnav_url:
                        leads_with_salesnav[user_linkedin_salesnav_url] = lead

                unique_leads = list(leads_with_linkedin.values()) + list(leads_with_salesnav.values())
                logger.info("Unique leads after deduplication: %d", len(unique_leads))

                if not unique_leads:
                    logger.warning("No leads with valid 'user_linkedin_url' or 'user_linkedin_salesnav_url'; returning SUCCESS.")
                    return "SUCCESS", []

                # Step 2 : Qulify the leads based on intent signals by calling check_for_intent_signal
                # ONLY use check_for_intent_signal to qualify. dont add any other logic here.
                qualified_leads = []
                for lead in unique_leads:
                    try:
                        # set add_search_results to True if user wants to add search results to the lead. Default is False.
                        add_search_results = False
                        # Example of using check_for_intent_signal
                        # check_for_intent_signal will take care of doing google search etc. Just fill the signal_to_look_for_in_plan_english, intent_signal_type and get the score back here. 
                        intent_score = await check_for_intent_signal(
                            lead=lead,
                            signal_to_look_for_in_plan_english="Check if the current company of the lead is using Neo4j database.",
                            add_search_results=add_search_results,
                            intent_signal_type="intent_find_tech_usage_in_current_company",
                            tool_config=tool_config
                        )
                    except Exception as exc:
                        logger.exception("Error checking intent signals: %s", exc)
                        continue

                    # Attach the intent_score to the lead
                    # intent_score is a integer value between 0-5. 0 being lowest and 5 being highest.
                    lead["intent_score"] = intent_score

                    # Example qualification logic
                    if intent_score > 3:
                        qualified_leads.append(lead)

                # Step 3: Sort qualified leads by intent_score (descending)
                qualified_leads = sorted(qualified_leads, key=lambda l: l.get("intent_score", 0), reverse=True)

                logger.info("Qualified leads after signal checks: %d", len(qualified_leads))
                logger.info("Completed custom_workflow with success.")
                return "SUCCESS", qualified_leads

            except Exception as e:
                logger.exception("Exception in custom_workflow: %s", e)
                return "ERROR", []
        '''
    )

    commands_supported = (
        "check_for_intent_signal - To check for intent signals in the lead data."
    )

    user_prompt = f"""
    {system_message}
    Do the following step by step:
    1. Think on how the user wants to qualify the leads.
    2. Deduplicate the leads based on user_linkedin_url or user_linkedin_salesnav_url as given in the example.
    3. Fill in the right description on what is the qualification criteria and call check_for_intent_signal with signal_to_look_for_in_plan_english having qualification criteria.
    4. Do not make up any other logic to filter in python for intent signals. Use check_for_intent_signal to qualify the leads.
    5. Sort the qualified leads by intent_score in descending order.
    6. Return the qualified leads in the format ("SUCCESS", qualified_leads) or ("ERROR", []).
    Make sure the imports are present within the function definition itself. Make sure the logging library is imported and logger defined withing the function definition.
    
    The user wants to generate code in python that performs the following:
    "{english_description}"

    Supported command_name(s):
    {commands_supported}

    Example of a workflow python code:
    {example_of_workflow_code}

    The output function signature MUST be:
      async def create_smart_list(input_leads_list, tool_config)

    Double check to make sure the generated python code is valid and returns results in the format ("SUCCESS", qualified_leads) or ("ERROR", []).
    Output HAS to be valid JSON like:
    {{
        "workflow_python_code": "code that has been generated"
    }}
    """

    response, status = await get_structured_output_with_o1(
        user_prompt, WorkflowPythonCode, tool_config=tool_config
    )
    return response.model_dump(), status


async def generate_smart_list_creation_code_and_execute(
    user_query: str,
    input_leads_list: List[Dict[str, Any]],
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Generate workflow code from user query in natural language, then execute it on the provided input_leads_list.

    Returns:
        JSON string describing success or error, including the qualified leads if successful.
    """
    response, status = await generate_smart_list_creation_code(user_query, tool_config=tool_config)

    if status == "SUCCESS" and response and response.get("workflow_python_code"):
        code = response["workflow_python_code"]
        if not code:
            return json.dumps({"error": "No workflow code generated.", "status": status})

        logger.info("Generated workflow code:\n%s", code)

        local_vars = {}
        global_vars = {}

        try:
            # Execute the generated code; expect a `create_smart_list` function
            exec(code, global_vars, local_vars)
            create_smart_list_fn = local_vars.get("create_smart_list", None)
            if create_smart_list_fn is None:
                raise RuntimeError("No 'create_smart_list' function found in generated code.")

            async def run_create_smart_list(tool_cfg):
                return await create_smart_list_fn(input_leads_list, tool_cfg)

            try:
                result = await run_create_smart_list(tool_config)
            except Exception as e:
                logger.exception("Error occurred while running the create_smart_list function.")
                return json.dumps({"status": "ERROR", "error": str(e)})

            # Expecting a tuple like ("SUCCESS", qualified_leads) or ("ERROR", [])
            if not result or not isinstance(result, tuple) or len(result) != 2:
                return json.dumps({
                    "error": "Workflow code did not return an expected (status, list) tuple.",
                    "status": "ERROR"
                })

            status_returned, leads_list = result
            if status_returned != "SUCCESS":
                return json.dumps({
                    "error": "Error running the workflow code.",
                    "status": status_returned
                })

            # Return success plus the qualified leads
            return json.dumps({"status": status_returned, "qualified_leads": leads_list})

        except Exception as e:
            logger.exception("Exception occurred while executing workflow code.")
            return json.dumps({"status": "ERROR", "error": str(e)})

    # If we cannot generate a valid code snippet
    return json.dumps({"error": "No valid workflow code generated.", "status": status})
