import asyncio
import hashlib
import json
import logging
import os
import aiohttp
import backoff
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from pydantic import BaseModel
from dhisana.schemas.sales import LeadsQueryFilters, SmartList, SmartListLead
from dhisana.utils.cache_output_tools import cache_output, retrieve_output
from dhisana.utils.assistant_tool_tag import assistant_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_apollo_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Retrieves the APOLLO_API_KEY access token from the provided tool configuration.

    Args:
        tool_config (list): A list of dictionaries containing the tool configuration. 
                            Each dictionary should have a "name" key and a "configuration" key,
                            where "configuration" is a list of dictionaries containing "name" and "value" keys.

    Returns:
        str: The APOLLO_API_KEY access token.

    Raises:
        ValueError: If the access token is not found in the tool configuration or environment variable.
    """
    logger.info("Entering get_apollo_access_token")
    APOLLO_API_KEY = None

    if tool_config:
        logger.debug(f"Tool config provided: {tool_config}")
        apollo_config = next(
            (item for item in tool_config if item.get("name") == "apollo"), None
        )
        if apollo_config:
            config_map = {
                item["name"]: item["value"]
                for item in apollo_config.get("configuration", [])
                if item
            }
            APOLLO_API_KEY = config_map.get("apiKey")
        else:
            logger.warning("No 'apollo' config item found in tool_config.")
    else:
        logger.debug("No tool_config provided or it's None.")

    # Check environment variable if no key found yet
    APOLLO_API_KEY = APOLLO_API_KEY or os.getenv("APOLLO_API_KEY")

    if not APOLLO_API_KEY:
        logger.error("APOLLO_API_KEY not found in configuration or environment.")
        raise ValueError("APOLLO_API_KEY access token not found in tool_config or environment variable")

    logger.info("Retrieved APOLLO_API_KEY successfully.")
    return APOLLO_API_KEY


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def enrich_person_info_from_apollo(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Fetch a person's details from Apollo using LinkedIn URL, email, or phone number.
    
    Parameters:
    - **linkedin_url** (*str*, optional): LinkedIn profile URL of the person.
    - **email** (*str*, optional): Email address of the person.
    - **phone** (*str*, optional): Phone number of the person.

    Returns:
    - **dict**: JSON response containing person information.
    """
    logger.info("Entering enrich_person_info_from_apollo")

    APOLLO_API_KEY = get_apollo_access_token(tool_config)

    if not linkedin_url and not email and not phone:
        logger.warning("No linkedin_url, email, or phone provided. At least one is required.")
        return {'error': "At least one of linkedin_url, email, or phone must be provided"}

    headers = {
        "X-Api-Key": f"{APOLLO_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {}
    if linkedin_url:
        logger.debug(f"LinkedIn URL provided: {linkedin_url}")
        data['linkedin_url'] = linkedin_url
        cached_response = retrieve_output("enrich_person_info_from_apollo", linkedin_url)
        if cached_response is not None:
            logger.info(f"Cache hit for LinkedIn URL: {linkedin_url}")
            return cached_response
    if email:
        logger.debug(f"Email provided: {email}")
        data['email'] = email
    if phone:
        logger.debug(f"Phone provided: {phone}")
        data['phone_numbers'] = [phone]  # Apollo expects a list for phone numbers

    url = 'https://api.apollo.io/api/v1/people/match'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                logger.debug(f"Received response status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    if linkedin_url:
                        cache_output("enrich_person_info_from_apollo", linkedin_url, result)
                    logger.info("Successfully retrieved person info from Apollo.")
                    return result
                elif response.status == 429:
                    msg = "Rate limit exceeded"
                    logger.warning(msg)
                    await asyncio.sleep(30)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=msg,
                        headers=response.headers
                    )
                else:
                    result = await response.json()
                    logger.warning(f"enrich_person_info_from_apollo error: {result}")
                    return {'error': result}
        except Exception as e:
            logger.exception("Exception occurred while fetching person info from Apollo.")
            return {'error': str(e)}


@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def lookup_person_in_apollo_by_name(
    full_name: str,
    company_name: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Fetch a person's details from Apollo using their full name and optionally company name.

    Parameters:
    - **full_name** (*str*): Full name of the person.
    - **company_name** (*str*, optional): Name of the company where the person works.
    - **tool_config** (*list*, optional): Tool configuration for API keys.

    Returns:
    - **dict**: JSON response containing person information.
    """
    logger.info("Entering lookup_person_in_apollo_by_name")

    if not full_name:
        logger.warning("No full_name provided.")
        return {'error': "Full name is required"}

    APOLLO_API_KEY = get_apollo_access_token(tool_config)
    headers = {
        "X-Api-Key": f"{APOLLO_API_KEY}",
        "Content-Type": "application/json"
    }

    # Construct the query payload
    data = {
        "q_keywords": f"{full_name} {company_name}" if company_name else full_name,
        "page": 1,
        "per_page": 10
    }

    url = 'https://api.apollo.io/api/v1/mixed_people/search'
    logger.debug(f"Making request to Apollo with payload: {data}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                logger.debug(f"Received response status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    logger.info("Successfully looked up person by name on Apollo.")
                    return result
                elif response.status == 429:
                    msg = "Rate limit exceeded"
                    logger.warning(msg)
                    await asyncio.sleep(30)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=msg,
                        headers=response.headers
                    )
                else:
                    result = await response.json()
                    logger.warning(f"lookup_person_in_apollo_by_name error: {result}")
                    return {'error': result}
        except Exception as e:
            logger.exception("Exception occurred while looking up person by name.")
            return {'error': str(e)}


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=30,
)
async def enrich_organization_info_from_apollo(
    organization_domain: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Fetch an organization's details from Apollo using the organization domain.
    
    Parameters:
    - **organization_domain** (*str*, optional): Domain of the organization.

    Returns:
    - **dict**: JSON response containing organization information.
    """
    logger.info("Entering enrich_organization_info_from_apollo")

    APOLLO_API_KEY = get_apollo_access_token(tool_config)

    if not organization_domain:
        logger.warning("No organization domain provided.")
        return {'error': "organization domain must be provided"}

    headers = {
        "X-Api-Key": f"{APOLLO_API_KEY}",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "accept": "application/json"
    }

    cached_response = retrieve_output("enrich_organization_info_from_apollo", organization_domain)
    if cached_response is not None:
        logger.info(f"Cache hit for organization domain: {organization_domain}")
        return cached_response

    url = f'https://api.apollo.io/api/v1/organizations/enrich?domain={organization_domain}'
    logger.debug(f"Making GET request to Apollo for organization domain: {organization_domain}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                logger.debug(f"Received response status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    cache_output("enrich_organization_info_from_apollo", organization_domain, result)
                    logger.info("Successfully retrieved organization info from Apollo.")
                    return result
                elif response.status == 429:
                    msg = "Rate limit exceeded"
                    logger.warning(msg)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=msg,
                        headers=response.headers
                    )
                else:
                    result = await response.json()
                    logger.warning(f"Error from Apollo while enriching org info: {result}")
                    return {'error': result}
        except Exception as e:
            logger.exception("Exception occurred while fetching organization info from Apollo.")
            return {'error': str(e)}


@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=5,
    giveup=lambda e: e.status != 429,
    factor=2,
)
async def fetch_apollo_data(session, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Helper function that fetches data from Apollo with caching and backoff on rate limits.
    """
    logger.info("Entering fetch_apollo_data")
    key_data = f"{url}_{json.dumps(payload, sort_keys=True)}"
    key_hash = hashlib.sha256(key_data.encode()).hexdigest()
    logger.debug(f"Cache key hash: {key_hash}")

    cached_response = retrieve_output("fetch_apollo_data", key_hash)
    if cached_response is not None:
        logger.info("Cache hit for fetch_apollo_data.")
        return cached_response

    logger.debug("No cache hit. Making POST request to Apollo.")
    async with session.post(url, headers=headers, json=payload) as response:
        logger.debug(f"Received response status: {response.status}")
        if response.status == 200:
            result = await response.json()
            cache_output("fetch_apollo_data", key_hash, result)
            logger.info("Successfully fetched data from Apollo and cached it.")
            return result
        elif response.status == 429:
            msg = "Rate limit exceeded"
            logger.warning(msg)
            raise aiohttp.ClientResponseError(
                request_info=response.request_info,
                history=response.history,
                status=response.status,
                message=msg,
                headers=response.headers
            )
        else:
            logger.error(f"Unexpected status code {response.status} from Apollo. Raising exception.")
            response.raise_for_status()


async def search_people_with_apollo(
    person_current_titles: List[str] = [],
    person_locations: List[str] = [],
    min_employees_in_organization: int = 1,
    max_employees_in_organization: int = 1000,
    filter_by_signals: List[str] = [],
    max_number_of_items_to_return: int = 100,
    industries: List[str] = [],
    search_keywords: Optional[str] = None,
    company_domains: Optional[List[str]] = None,
    company_hq_locations: Optional[List[str]] = None,
    contact_email_status: Optional[List[str]] = None,
    company_ids: Optional[List[str]] = None,
    person_seniorities: Optional[List[str]] = None,
    tool_config: Optional[List[Dict[str, Any]]] = None,

    job_openings_with_titles: Optional[List[str]] = None,

    min_revenue_of_the_company: Optional[int] = None,
    max_revenue_of_the_company: Optional[int] = None,
    latest_funding_stages: Optional[List[str]] = None,
    company_industry_tag_ids: Optional[List[str]] = None,
    q_organization_search_list_id: Optional[str] = None,
    q_not_organization_search_list_id: Optional[str] = None,
    currently_using_any_of_technology_uids: Optional[List[str]] = None,
    sort_by_field: Optional[str] = None,
    sort_ascending: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """
    Searches Apollo using the People Search endpoint and returns raw results (people + contacts).
    """
    logger.info("Entering search_people_with_apollo")

    # Validate min/max employees
    if min_employees_in_organization < 1:
        logger.warning("Minimum number of employees must be at least 1. Overriding to 1.")
        min_employees_in_organization = 1
    if max_employees_in_organization > 100000:
        logger.warning("Maximum number of employees must not exceed 100,000. Overriding to 100000.")
        max_employees_in_organization = 100000
    if min_employees_in_organization >= max_employees_in_organization:
        raise ValueError("Minimum employees must be less than maximum employees.")

    # Enforce search result limits
    if max_number_of_items_to_return <= 0:
        logger.warning("max_number_of_items_to_return <= 0, overriding to 10.")
        max_number_of_items_to_return = 10
    elif max_number_of_items_to_return > 5000:
        logger.warning("max_number_of_items_to_return > 5000, overriding to 5000.")
        max_number_of_items_to_return = 5000

    # Retrieve API key
    api_key = get_apollo_access_token(tool_config)
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }

    # Apollo People Search endpoint
    url = "https://api.apollo.io/api/v1/mixed_people/search"

    # Convert signals to Apollo-specific IDs (example mapping)
    signal_mapping = {
        "RECENT_JOB_CHANGE": "643daa349293c1cdaa4d00f8",
        "RAPID_EXPANSION":  "643daa3f9293c1cdaa4d00fa",
    }
    search_signal_ids = [signal_mapping[s] for s in filter_by_signals if s in signal_mapping]

    logger.debug(
        "Apollo Search:\n"
        f"  person_current_titles={person_current_titles}\n"
        f"  person_locations={person_locations}\n"
        f"  employees_in_organization=({min_employees_in_organization} to {max_employees_in_organization})\n"
        f"  filter_by_signals={filter_by_signals}\n"
        f"  industries={industries}\n"
        f"  search_keywords={search_keywords}\n"
        f"  company_domains={company_domains}\n"
        f"  company_hq_locations={company_hq_locations}\n"
        f"  contact_email_status={contact_email_status}\n"
        f"  company_ids={company_ids}\n"
        f"  person_seniorities={person_seniorities}\n"
        f"  job_openings_with_titles={job_openings_with_titles}\n"
        f"  min_revenue_of_the_company={min_revenue_of_the_company}\n"
        f"  max_revenue_of_the_company={max_revenue_of_the_company}\n"
        f"  latest_funding_stages={latest_funding_stages}\n"
        f"  company_industry_tag_ids={company_industry_tag_ids}\n"
        f"  q_organization_search_list_id={q_organization_search_list_id}\n"
        f"  q_not_organization_search_list_id={q_not_organization_search_list_id}\n"
        f"  technology_used={currently_using_any_of_technology_uids}\n"
        f"  sort_by_field={sort_by_field}\n"
        f"  sort_ascending={sort_ascending}\n"
        f"  max_items={max_number_of_items_to_return}"
    )

    async with aiohttp.ClientSession() as session:
        results: List[Dict[str, Any]] = []
        page = 1
        per_page = min(max_number_of_items_to_return, 100)  # 100 max per page

        while len(results) < max_number_of_items_to_return:
            employee_ranges = [f"{min_employees_in_organization},{max_employees_in_organization}"]

            # Decide how to handle person_locations vs company_hq_locations
            if not person_locations and company_hq_locations:
                person_locations = company_hq_locations
            elif person_locations and company_hq_locations:
                person_locations = list(set(person_locations + company_hq_locations))
            elif not person_locations:
                logger.debug("No person_locations provided, defaulting to ['United States'].")
                person_locations = ["United States"]

            payload = {
                "person_titles": person_current_titles,
                "person_locations": person_locations,
                "search_signal_ids": search_signal_ids,
                "organization_num_employees_ranges": employee_ranges,
                "page": page,
                "per_page": per_page,
            }

            if search_keywords:
                payload["q_keywords"] = search_keywords
            if company_domains:
                payload["q_organization_domains"] = company_domains
            # if company_hq_locations:
            #     payload["organization_locations"] = company_hq_locations
            # if contact_email_status:
            #     payload["contact_email_status"] = contact_email_status
            # if company_ids:
            #     payload["organization_ids"] = company_ids
            if person_seniorities:
                payload["person_seniorities"] = person_seniorities
            if industries:
                payload["organization_industries"] = industries

            # job_openings_with_titles
            if job_openings_with_titles:
                payload["q_organization_job_titles"] = job_openings_with_titles

            # revenue range
            if min_revenue_of_the_company is not None or max_revenue_of_the_company is not None:
                payload["revenue_range"] = {}
                if min_revenue_of_the_company is not None:
                    payload["revenue_range"]["min"] = min_revenue_of_the_company
                if max_revenue_of_the_company is not None:
                    payload["revenue_range"]["max"] = max_revenue_of_the_company

            # Sorting
            if sort_by_field is not None:
                payload["sort_by_field"] = sort_by_field
            if sort_ascending is not None:
                payload["sort_ascending"] = sort_ascending

            logger.debug(f"Payload for Apollo search on page {page}: {payload}")

            try:
                data = await fetch_apollo_data(session, url, headers, payload)
                if data is None:
                    logger.error("No data returned from Apollo API.")
                    break

                people = data.get("people", [])
                contacts = data.get("contacts", [])

                logger.info(f"Apollo returned {len(people)} people and {len(contacts)} contacts on page {page}.")

                if not people and not contacts:
                    logger.info("No more results found, ending pagination.")
                    break

                results.extend(people + contacts)

                pagination = data.get("pagination", {})
                current_page = pagination.get("page", 1)
                total_pages = pagination.get("total_pages", 1)

                if current_page >= total_pages:
                    logger.info("Reached the last page of results.")
                    break
                page += 1

            except aiohttp.ClientResponseError as e:
                if e.status == 429:
                    logger.warning("Rate limited by Apollo API, sleeping for 30 seconds...")
                    await asyncio.sleep(30)
                else:
                    logger.error(f"ClientResponseError from Apollo: status={e.status}, message={str(e)}")
                    error_details = {
                        "status": e.status,
                        "message": str(e),
                        "url": str(e.request_info.url) if e.request_info else "N/A",
                        "headers": dict(e.headers) if e.headers else {},
                    }
                    return [error_details]
            except Exception as e:
                logger.exception("Exception occurred while searching for people in Apollo.")
                break

        logger.info(f"Total results collected: {len(results)}")
        return results[:max_number_of_items_to_return]


async def search_leads_with_apollo(
    query: LeadsQueryFilters,
    request: SmartList,
    tool_config: Optional[List[Dict[str, Any]]] = None
) -> List[SmartListLead]:
    """
    Given a LeadsQueryFilters object, run the Apollo People Search.
    Format each result record as a SmartListLead.
    """
    logger.info("Entering search_leads_with_apollo")

    # 1) Apply defaults if any field is None
    person_current_titles = query.person_current_titles or []
    person_locations = query.person_locations or []
    min_employees = query.min_employees_in_organization or 1
    max_employees = query.max_employees_in_organization or 1000
    signals = query.filter_by_signals or []
    max_items = request.max_leads or 10
    if max_items > 2000:
        logger.warning("Requested max_leads > 2000, overriding to 2000.")
        max_items = 2000

    industries = query.industries or []

    # Additional filters
    search_keywords = query.search_keywords
    company_domains = query.company_domains or []
    company_hq_locations = query.company_hq_locations or []
    contact_email_status = query.contact_email_status or []
    company_ids = query.company_ids or []
    person_seniorities = query.person_seniorities or []

    # New field for job openings
    job_openings_with_titles = query.job_openings_with_titles

    # Additional fields
    min_revenue = query.min_revenue_of_the_company
    max_revenue = query.max_revenue_of_the_company
    latest_funding_stages = query.latest_funding_stages
    company_industry_tag_ids = query.company_industry_tag_ids
    q_organization_search_list_id = query.q_organization_search_list_id
    q_not_organization_search_list_id = query.q_not_organization_search_list_id
    currently_using_any_of_technology_uids = query.currently_using_any_of_technology_uids
    sort_by_field = query.sort_by_field
    sort_ascending = query.sort_ascending

    logger.debug(f"SmartList request => agent_instance_id={request.agent_instance_id}, organization_id={request.organization_id}")

    # 2) Fetch raw results (list of dict) from Apollo
    results = await search_people_with_apollo(
        person_current_titles=person_current_titles,
        person_locations=person_locations,
        min_employees_in_organization=min_employees,
        max_employees_in_organization=max_employees,
        filter_by_signals=signals,
        max_number_of_items_to_return=max_items,
        industries=industries,
        search_keywords=search_keywords,
        company_domains=company_domains,
        company_hq_locations=company_hq_locations,
        contact_email_status=contact_email_status,
        company_ids=company_ids,
        person_seniorities=person_seniorities,
        tool_config=tool_config,
        job_openings_with_titles=job_openings_with_titles,
        min_revenue_of_the_company=min_revenue,
        max_revenue_of_the_company=max_revenue,
        latest_funding_stages=latest_funding_stages,
        company_industry_tag_ids=company_industry_tag_ids,
        q_organization_search_list_id=q_organization_search_list_id,
        q_not_organization_search_list_id=q_not_organization_search_list_id,
        currently_using_any_of_technology_uids=currently_using_any_of_technology_uids,
        sort_by_field=sort_by_field,
        sort_ascending=sort_ascending
    )

    # 3) Convert raw results into SmartListLead objects
    leads_list: List[SmartListLead] = []
    for apollo_person in results:
        org_data = apollo_person.get("organization", {}) or {}

        lead = SmartListLead(
            full_name=apollo_person.get("name"),
            first_name=apollo_person.get("first_name"),
            last_name=apollo_person.get("last_name"),
            email=apollo_person.get("email"),
            user_linkedin_url=apollo_person.get("linkedin_url"),
            phone=apollo_person.get("contact", {}).get("sanitized_phone"),
            job_title=apollo_person.get("title"),
            headline=apollo_person.get("headline"),

            organization_name=org_data.get("name"),
            organization_linkedin_url=org_data.get("linkedin_url"),
            organization_website=org_data.get("website_url"),
            primary_domain_of_organization=org_data.get("primary_domain"),

            lead_location=", ".join(
                filter(None, [apollo_person.get("city", ""), apollo_person.get("state", "")])
            ) or None,

            agent_instance_id=request.agent_instance_id,
            organization_id=request.organization_id,
            created_by=None,
        )

        # Example email masking or cleaning
        if lead.email and "domain.com" in lead.email.lower():
            logger.debug(f"Masking an email that contains 'domain.com': {lead.email}")
            lead.email = ""

        additional_props = {}
        additional_props["raw_apollo_data"] = json.dumps(apollo_person)
        lead.additional_properties = additional_props

        leads_list.append(lead)

    logger.info(f"Converted {len(leads_list)} Apollo records into SmartListLead objects.")
    return leads_list


@assistant_tool
async def get_organization_domain_from_apollo(
    organization_id: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Fetch an organization's domain from Apollo using the organization ID.

    Parameters:
    - organization_id (str): ID of the organization.

    Returns:
    - dict: Contains the organization's ID and domain, or an error message.
    """
    logger.info("Entering get_organization_domain_from_apollo")

    if not organization_id:
        logger.warning("No organization_id provided.")
        return {'error': 'organization_id must be provided'}

    try:
        result = await get_organization_details_from_apollo(organization_id, tool_config=tool_config)
        if 'error' in result:
            return result
        domain = result.get('primary_domain')
        if domain:
            logger.info("Successfully retrieved domain from Apollo organization details.")
            return {'organization_id': organization_id, 'domain': domain}
        else:
            logger.warning("Domain not found in the organization details.")
            return {'error': 'Domain not found in the organization details'}
    except Exception as e:
        logger.exception("Exception occurred in get_organization_domain_from_apollo.")
        return {'error': str(e)}


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=3,
    giveup=lambda e: e.status != 429,
    factor=60,
)
async def get_organization_details_from_apollo(
    organization_id: str,
    tool_config: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Fetch an organization's details from Apollo using the organization ID.

    Parameters:
    - organization_id (str): ID of the organization.

    Returns:
    - dict: Organization details or an error message.
    """
    logger.info("Entering get_organization_details_from_apollo")

    APOLLO_API_KEY = get_apollo_access_token(tool_config)
    if not organization_id:
        logger.warning("No organization_id provided.")
        return {'error': "Organization ID must be provided"}

    headers = {
        "X-Api-Key": APOLLO_API_KEY,
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Accept": "application/json"
    }

    cached_response = retrieve_output("get_organization_details_from_apollo", organization_id)
    if cached_response is not None:
        logger.info(f"Cache hit for organization ID: {organization_id}")
        return cached_response

    url = f'https://api.apollo.io/api/v1/organizations/{organization_id}'
    logger.debug(f"Making GET request to Apollo for organization ID: {organization_id}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                logger.debug(f"Received response status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    org_details = result.get('organization', {})
                    if org_details:
                        cache_output("get_organization_details_from_apollo", organization_id, org_details)
                        logger.info("Successfully retrieved organization details from Apollo.")
                        return org_details
                    else:
                        logger.warning("Organization details not found in the response.")
                        return {'error': 'Organization details not found in the response'}
                elif response.status == 429:
                    msg = "Rate limit exceeded"
                    limit_minute = response.headers.get('x-rate-limit-minute')
                    limit_hourly = response.headers.get('x-rate-limit-hourly')
                    limit_daily = response.headers.get('x-rate-limit-daily')
                    logger.info(f"get_organization_details_from_apollo x-rate-limit-minute: {limit_minute}")
                    logger.info(f"get_organization_details_from_apollo x-rate-limit-hourly: {limit_hourly}")
                    logger.info(f"get_organization_details_from_apollo x-rate-limit-daily: {limit_daily}")
                    logger.warning(msg)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=msg,
                        headers=response.headers
                    )
                else:
                    result = await response.json()
                    logger.warning(f"get_organization_details_from_apollo error: {result}")
                    return {'error': result}
        except Exception as e:
            logger.exception("Exception occurred while fetching organization details from Apollo.")
            return {'error': str(e)}


async def enrich_user_info_with_apollo(
    input_user_properties: Dict[str, Any],
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Enriches the user info (input_user_properties) with data from Apollo.
    Attempts direct enrichment if LinkedIn URL or email is provided; otherwise,
    performs a name-based search. Updates the user_properties dictionary in place.

    Parameters:
    - input_user_properties (Dict[str, Any]): A dictionary with user details.
    - tool_config (List[Dict], optional): Apollo tool configuration.

    Returns:
    - Dict[str, Any]: Updated input_user_properties with enriched data from Apollo.
    """
    logger.info("Entering enrich_user_info_with_apollo")

    if not input_user_properties:
        logger.warning("No input_user_properties provided; returning empty dict.")
        return {}

    linkedin_url = input_user_properties.get("user_linkedin_url", "")
    email = input_user_properties.get("email", "")
    user_data_from_apollo = None

    logger.debug(f"Properties => LinkedIn URL: {linkedin_url}, Email: {email}")

    # If LinkedIn url or email is present, attempt direct enrichment
    if linkedin_url or email:
        try:
            user_data_from_apollo = await enrich_person_info_from_apollo(
                linkedin_url=linkedin_url,
                email=email,
                tool_config=tool_config
            )
        except Exception as e:
            logger.exception("Exception occurred while enriching person info from Apollo by LinkedIn or email.")
    else:
        # Fallback to name-based lookup
        first_name = input_user_properties.get("first_name", "")
        last_name = input_user_properties.get("last_name", "")
        full_name = input_user_properties.get("full_name", f"{first_name} {last_name}").strip()
        company = input_user_properties.get("organization_name", "")

        if not full_name:
            logger.warning("No full_name or (first_name + last_name) provided.")
            input_user_properties["found_user_in_apollo"] = False
            return input_user_properties

        logger.debug(f"Looking up Apollo by name: {full_name}, company: {company}")
        try:
            search_result = await lookup_person_in_apollo_by_name(
                full_name=full_name,
                company_name=company,
                tool_config=tool_config
            )

            # Extract people and contacts from the search result
            people = search_result.get("people", [])
            contacts = search_result.get("contacts", [])
            results = people + contacts
            logger.info(f"Name-based lookup returned {len(results)} results from Apollo.")

            for person in results:
                person_name = person.get("name", "").lower()
                person_first_name = person.get("first_name", "").lower()
                person_last_name = person.get("last_name", "").lower()
                person_company = (person.get("organization", {}) or {}).get("name", "").lower()

                # Match the full name or first/last name and company
                if (
                    (person_name == full_name.lower() or
                     (person_first_name == first_name.lower() and person_last_name == last_name.lower()))
                    and (not company or person_company == company.lower())
                ):
                    logger.info(f"Found matching person {person.get('name')} in Apollo. Enriching data.")
                    linkedin_url = person.get("linkedin_url", "")
                    if linkedin_url:
                        try:
                            user_data_from_apollo = await enrich_person_info_from_apollo(
                                linkedin_url=linkedin_url,
                                tool_config=tool_config
                            )
                        except Exception as e:
                            logger.exception("Exception occurred during second stage Apollo enrichment.")
                    if user_data_from_apollo:
                        break
        except Exception as e:
            logger.exception("Exception occurred while performing name-based lookup in Apollo.")

    if not user_data_from_apollo:
        logger.debug("No user data returned from Apollo.")
        input_user_properties["found_user_in_apollo"] = False
        return input_user_properties

    # At this point, user_data_from_apollo likely has "person" key
    person_data = user_data_from_apollo.get("person", {})
    additional_props = input_user_properties.get("additional_properties") or {}
    additional_props["apollo_person_data"] = json.dumps(person_data)
    input_user_properties["additional_properties"] = additional_props

    # Fill missing contact info if not already present
    if not input_user_properties.get("email"):
        input_user_properties["email"] = person_data.get("email", "")
    if not input_user_properties.get("phone"):
        input_user_properties["phone"] = (person_data.get("contact", {}) or {}).get("sanitized_phone", "")

    # Map fields
    if person_data.get("name"):
        input_user_properties["full_name"] = person_data["name"]
    if person_data.get("first_name"):
        input_user_properties["first_name"] = person_data["first_name"]
    if person_data.get("last_name"):
        input_user_properties["last_name"] = person_data["last_name"]
    if person_data.get("linkedin_url"):
        input_user_properties["user_linkedin_url"] = person_data["linkedin_url"]

    if person_data.get("organization"):
        org_data = person_data["organization"] or {}
        if org_data.get("primary_domain"):
            input_user_properties["primary_domain_of_organization"] = org_data["primary_domain"]
        if org_data.get("name"):
            input_user_properties["organization_name"] = org_data["name"]
        if org_data.get("linkedin_url"):
            input_user_properties["organization_linkedin_url "] = org_data["linkedin_url"]
        if org_data.get("website_url"):
            input_user_properties["organization_website"] = org_data["website_url"]
        if org_data.get("keywords"):
            input_user_properties["keywords"] = ", ".join(org_data["keywords"])

    if person_data.get("title"):
        input_user_properties["job_title"] = person_data["title"]
    if person_data.get("headline"):
        input_user_properties["headline"] = person_data["headline"]
        # If there's no summary_about_lead, reuse the person's headline
        if not input_user_properties.get("summary_about_lead"):
            input_user_properties["summary_about_lead"] = person_data["headline"]

    # Derive location
    city = person_data.get("city", "")
    state = person_data.get("state", "")
    if city or state:
        input_user_properties["lead_location"] = f"{city}, {state}".strip(", ")

    # Verify name match
    first_matched = bool(
        input_user_properties.get("first_name")
        and person_data.get("first_name") == input_user_properties["first_name"]
    )
    last_matched = bool(
        input_user_properties.get("last_name")
        and person_data.get("last_name") == input_user_properties["last_name"]
    )
    if first_matched and last_matched:
        logger.info("Matching user found and data enriched from Apollo.")
        input_user_properties["found_user_in_apollo"] = True

    return input_user_properties
