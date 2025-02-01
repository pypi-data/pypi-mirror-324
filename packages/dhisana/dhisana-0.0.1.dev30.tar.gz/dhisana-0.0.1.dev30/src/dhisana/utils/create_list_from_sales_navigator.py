import json
import logging
from typing import Any, Dict, List, Optional, Tuple


from dhisana.utils.generate_structured_output_internal import get_structured_output_with_o1, get_structured_output_with_o1
from dhisana.utils.workflow_code_model import WorkflowPythonCode

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_sales_nav_list_workflow_code(
    english_description: str,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[Dict[str, Any], str]:
    """
    Generate a workflow code (Python code) from an English description.

    Returns:
      A tuple of:
       - A dict containing {'workflow_python_code': '...'} 
       - A string representing status, e.g., 'SUCCESS' or 'ERROR'.
    """
    system_message = (
        "You are a helpful AI assistant who is an expert python coder. I want you to convert an English description of "
        "a requirement provided by user into an executable Python function called create_list_from_sales_navigator. "
        "Your output must be valid Python code. The provided example shows how the structure looks like and what methods you can use. "
        "Make sure the imports are present within the function definition itself. Make sure the logging library is imported and logger defined withing the function. "
        "Use the output function signature:\n"
        "    async def create_list_from_sales_navigator(tool_config)\n"
    )

    example_of_workflow_code = (
        '''
        async def create_list_from_sales_navigator(tool_config):
            """
            Example workflow demonstrating how to create a list from Sales Navigator.
            Returns ("SUCCESS", unique_leads) or ("ERROR", []).
            """
             # Make sure required imports are there within the function definition itself.
            import asyncio
            import logging
            from typing import Any, Dict, List, Optional, Tuple
            from dhisana.utils.agent_task import execute_task
            from dhisana.utils.compose_salesnav_query import generate_salesnav_people_search_url
            
            # Make sure the logger is present.
            logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)
        
            try:
                logger.info("Starting custom_workflow execution")

                english_request_for_salesnav_search = """Find me 2nd-degree connections who recently changed jobs, 
                    have a current job title of Chief Marketing Officer, 
                    and work in companies with 50-1000 employees."""
                
                # if user has provided a sales navigator url use that.
                user_input_salesnav_url = """ User provided sales nav query goes here """

                # Generate a Sales Navigator URL
                result = await generate_salesnav_people_search_url(
                    english_description=english_request_for_salesnav_search,
                    user_input_salesnav_url=user_input_salesnav_url,
                    tool_config=tool_config
                )
                if not result:
                    logger.error("generate_salesnav_people_search_url returned no result")
                    return "ERROR", []

                salesnav_url_list_leads = result.get('linkedin_salenav_url_with_query_parameters', None)
                logger.info("Sales Navigator URL obtained: %s", salesnav_url_list_leads)

                if not salesnav_url_list_leads:
                    logger.warning("No valid URL returned; cannot proceed.")
                    return "ERROR", []

                # Extract leads from the URL
                command_args = {
                    "salesnav_url_list_leads": salesnav_url_list_leads,
                    "max_pages": 1,
                    "enrich_detailed_lead_information": False,
                    "enrich_detailed_company_information": False,
                }
                try:
                    extraction_result = await execute_task("extract_leads_information", command_args, tool_config=tool_config)
                except Exception as exc:
                    logger.exception("Error while extracting leads: %s", exc)
                    return "ERROR", []

                leads = extraction_result.get('data', [])
                logger.info("Number of leads extracted: %d", len(leads))

                if not leads:
                    return "SUCCESS", []

                # Deduplicate leads
                unique_leads = {}
                for lead in leads:
                    salesnav_url = lead.get("user_linkedin_salesnav_url")
                    if salesnav_url:
                        unique_leads[salesnav_url] = lead

                deduped_leads = list(unique_leads.values())
                logger.info("Unique leads after deduplication: %d", len(deduped_leads))

                logger.info("Completed custom_workflow with success.")
                return "SUCCESS", deduped_leads

            except Exception as e:
                logger.exception("Exception in custom_workflow: %s", e)
                return "ERROR", []
        '''
    )

    supported_filters_explanation = """
        Sales Navigator filters include (not exhaustive):
            - PAST_COLLEAGUE
            - CURRENT_TITLE
            - PAST_TITLE
            - CURRENT_COMPANY
            - PAST_COMPANY
            - GEOGRAPHY (REGION)
            - INDUSTRY
            - SCHOOL
            - CONNECTION (RELATIONSHIP)
            - CONNECTIONS_OF
            - GROUP
            - COMPANY_HEADCOUNT
            - COMPANY_TYPE
            - SENIORITY_LEVEL
            - YEARS_IN_POSITION
            - YEARS_IN_COMPANY
            - FOLLOWING_YOUR_COMPANY (FOLLOWS_YOUR_COMPANY)
            - VIEWED_YOUR_PROFILE
            - CHANGED_JOBS (RECENTLY_CHANGED_JOBS)
            - POSTED_ON_LINKEDIN
            - MENTIONED_IN_NEWS
            - TECHNOLOGIES_USED
            - ANNUAL_REVENUE
            - LEAD_INTERACTIONS (e.g. Viewed Profile, Messaged)
            - SAVED_LEADS_AND_ACCOUNTS
            - WITH_SHARED_EXPERIENCES
            - FIRST_NAME
            - LAST_NAME
            - FUNCTION
            - YEARS_OF_EXPERIENCE
            - YEARS_AT_CURRENT_COMPANY
            - YEARS_IN_CURRENT_POSITION
            - COMPANY_HEADQUARTERS
    """

    user_prompt = f"""
    {system_message}
    Do the following step by step:
    1. Think about the leads the user wants to query and filters to use for the same. 
    2. If the user has provided a sales navigator url use that.
    3. Take a look at the examples provided to construct the URL if user has not provided one. 
    4. Think about the code example provided and see how you will fill the english_request_for_salesnav_search and user_input_salesnav_url correctly.
    5. Generate the correct python code which takes care of above requirements. 
    6. Make sure the code is valid and returns results in the format ("SUCCESS", leads_list) or ("ERROR", []).
    7. Return the result in valid JSON format filled in workflow_python_code.
    
    The user wants to generate code in python that performs the following:

    "{english_description}"

    Example of a workflow python code:
    {example_of_workflow_code}
    
    If user has provided a Sales Navigator URL set to to user_input_salesnav_url in the code and pass as input to generate_salesnav_people_search_url.

    Each lead returned has at least:
    full_name, first_name, last_name, email, user_linkedin_salesnav_url, organization_linkedin_salesnav_url ,
    user_linkedin_url, primary_domain_of_organization, job_title, phone, headline,
    lead_location, organization_name, organization_website, summary_about_lead, keywords,
    number_of_linkedin_connections

    Following are some common methods available:
    1. generate_salesnav_people_search_url - to generate Sales Navigator URL from plain English query.
       (Supported filters: {supported_filters_explanation})

    The output function signature MUST be:
      async def create_list_from_sales_navigator(tool_config)

    Double check to make sure the generated python code is valid and returns results in the format ("SUCCESS", leads_list) or ("ERROR", []).
    Output HAS to be valid JSON like:
    {{
        "workflow_python_code": "code that has been generated"
    }}
    """

    # Call the LLM
    response, status = await get_structured_output_with_o1(
        user_prompt, WorkflowPythonCode, tool_config=tool_config
    )
    return response.model_dump(), status


async def generate_sales_nav_list_workflow_and_execute(
    user_query: str, 
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Generate workflow from user query in natural language, then execute it.
    Returns:
      JSON string describing success or error, and includes leads if successful.
    """
    response, status = await generate_sales_nav_list_workflow_code(user_query, tool_config=tool_config)
    
    if status == "SUCCESS" and response and response.get("workflow_python_code"):
        code = response["workflow_python_code"]
        if not code:
            return json.dumps({"error": "No workflow code generated.", "status": status})
        
        logger.info("Generated workflow code:\n%s", code)
        local_vars = {}
        global_vars = {}

        try:
            # Execute the generated code; expect a function named `create_list_from_sales_navigator`
            exec(code, global_vars, local_vars)
            create_fn = local_vars.get("create_list_from_sales_navigator", None)
            if create_fn is None:
                raise RuntimeError("No 'create_list_from_sales_navigator' function found in generated code.")

            # Run the async function
            async def run_create_list(tool_cfg):
                return await create_fn(tool_cfg)

            try:
                result = await run_create_list(tool_config)
            except Exception as e:
                logger.exception("Error occurred while running create_list_from_sales_navigator.")
                return json.dumps({"status": "ERROR", "error": str(e)})

            # We expect a tuple like ("SUCCESS", leads) or ("ERROR", [])
            if not isinstance(result, tuple) or len(result) != 2:
                return json.dumps({
                    "status": "ERROR",
                    "error": "Workflow code did not return an expected (status, leads_list) tuple."
                })

            status_returned, leads_list = result
            if status_returned != "SUCCESS":
                return json.dumps({
                    "status": status_returned,
                    "error": "Workflow returned an error status.",
                    "leads": leads_list
                })

            # Return success plus leads
            return json.dumps({
                "status": status_returned,
                "leads": leads_list
            })

        except Exception as e:
            logger.exception("Exception occurred while executing workflow code.")
            return json.dumps({"status": "ERROR", "error": str(e)})

    # If code generation failed or we have no code snippet
    return json.dumps({"error": "No workflow code generated.", "status": status})
