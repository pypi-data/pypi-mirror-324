import os
import json
import logging
from typing import Dict, List, Optional, Any
import aiohttp

logger = logging.getLogger(__name__)
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.cache_output_tools import cache_output, retrieve_output

# --------------------------------------------------------------------------------
# 1. Access Token Helpers
# --------------------------------------------------------------------------------

def get_zero_bounce_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Retrieves the ZeroBounce access token from the provided tool configuration or environment.

    Raises:
        ValueError: If the token is not found.
    """
    logger.info("Entering get_zero_bounce_access_token method.")
    if tool_config:
        zerobounce_config = next(
            (item for item in tool_config if item.get("name") == "zerobounce"), None
        )
        if zerobounce_config:
            config_map = {
                c["name"]: c["value"]
                for c in zerobounce_config.get("configuration", [])
                if c
            }
            ZERO_BOUNCE_API_KEY = config_map.get("apiKey")
        else:
            logger.warning("ZeroBounce config not provided or missing 'apiKey'.")
            ZERO_BOUNCE_API_KEY = None
    else:
        logger.warning("ZeroBounce config not provided or missing 'apiKey'.")
        ZERO_BOUNCE_API_KEY = None

    logger.info("Using environment variable for ZERO_BOUNCE_API_KEY if available.")
    ZERO_BOUNCE_API_KEY = ZERO_BOUNCE_API_KEY or os.getenv("ZERO_BOUNCE_API_KEY")
    if not ZERO_BOUNCE_API_KEY:
        raise ValueError("ZERO_BOUNCE_API_KEY not found in config or env.")

    logger.info("Exiting get_zero_bounce_access_token method with a valid API key.")
    return ZERO_BOUNCE_API_KEY

def get_debounce_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Retrieves the DeBounce access token from the provided tool configuration or environment.

    Raises:
        ValueError: If the token is not found.
    """
    if tool_config:
        debounce_config = next(
            (item for item in tool_config if item.get("name") == "debounce"), None
        )
        if debounce_config:
            config_map = {
                c["name"]: c["value"]
                for c in debounce_config.get("configuration", [])
                if c
            }
            DEBOUNCE_API_KEY = config_map.get("apiKey")
        else:
            logger.warning("DeBounce config not provided or missing 'apiKey'.")
            DEBOUNCE_API_KEY = None
    else:
        logger.warning("DeBounce config not provided or missing 'apiKey'.")
        DEBOUNCE_API_KEY = None

    logger.info("Using environment variable for DEBOUNCE_API_KEY if available.")
    DEBOUNCE_API_KEY = DEBOUNCE_API_KEY or os.getenv("DEBOUNCE_API_KEY")
    if not DEBOUNCE_API_KEY:
        raise ValueError("DEBOUNCE_API_KEY not found in config or env.")

    return DEBOUNCE_API_KEY

# --------------------------------------------------------------------------------
# 2. Provider-Specific Validation Functions
# --------------------------------------------------------------------------------

@assistant_tool
async def check_email_validity_with_zero_bounce(
    email_id: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, bool]:
    """
    Validate a single email address using the ZeroBounce API, with caching.

    Returns:
        dict: {"is_valid": bool}
    """
    logger.info("Entering check_email_validity_with_zero_bounce for email_id: %s", email_id)
    import re
    if (not email_id or 
        not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email_id) or 
        email_id.lower().endswith("@domain.com")):
        return {"is_valid": False}

    cache_key = f"zerobounce_validate_{email_id}"
    logger.info(f"check_email_validity_with_zero_bounce: Checking cache with key: {cache_key}")
    cached_response = retrieve_output(cache_key, email_id)
    if cached_response is not None:
        logger.info("Cache hit for ZeroBounce validate.")
        if not cached_response:
            return {"is_valid": False}
        return json.loads(cached_response[0])

    logger.info("No cache hit, proceeding to call ZeroBounce API.")
    ZERO_BOUNCE_API_KEY = get_zero_bounce_access_token(tool_config)
    url = (
        "https://api.zerobounce.net/v2/validate"
        f"?api_key={ZERO_BOUNCE_API_KEY}&email={email_id}"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                logger.warning("ZeroBounce returned a non-200 response code.")
                content = await safe_read_json_or_text(response)
                logger.warning(f"[ZeroBounce] Non-200 status: {response.status} => {content}")
                raise Exception(f"[ZeroBounce] Error: {content}")

            result = await response.json()

    status = result.get("status", "").lower()
    logger.info("ZeroBounce validation status: %s", status)
    is_valid = (status == "valid")
    final_response = {"is_valid": is_valid}
    cache_output(cache_key, email_id, [json.dumps(final_response)])
    logger.info("Exiting check_email_validity_with_zero_bounce.")
    return final_response

@assistant_tool
async def check_email_validity_with_debounce(
    email_id: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, bool]:
    """
    Validate a single email address using the DeBounce API, with caching.

    Returns:
        dict: {"is_valid": bool}
    """
    logger.info("Entering check_email_validity_with_debounce for email_id: %s", email_id)
    import re
    if (not email_id or 
        not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email_id) or 
        email_id.lower().endswith("@domain.com")):
        return {"is_valid": False}

    DEBOUNCE_API_KEY = get_debounce_access_token(tool_config)
    url = (
        "https://api.debounce.io/v1/"
        f"?api={DEBOUNCE_API_KEY}&email={email_id}"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                logger.warning("DeBounce returned a non-200 response code.")
                content = await safe_read_json_or_text(response)
                logger.warning(f"[DeBounce] Non-200 status: {response.status} => {content}")
                raise Exception(f"[DeBounce] Error: {content}")

            result = await response.json()

    code = result.get("debounce", {}).get("code")
    logger.info("DeBounce validation code: %s", code)
    is_valid = (code == "5")
    logger.info("Exiting check_email_validity_with_debounce.")
    return {"is_valid": is_valid}

@assistant_tool
async def guess_email_with_zero_bounce(
    first_name: str,
    last_name: str,
    domain: str,
    middle_name: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Attempt to guess the email using ZeroBounce's guessFormat endpoint, with caching.

    API Docs: https://www.zerobounce.net/docs
    """
    logger.info("Entering guess_email_with_zero_bounce.")
    if not first_name or not last_name or not domain:
        logger.error("Required parameters first_name, last_name, and domain must be provided.")
        return {"error": "first_name, last_name, and domain are required."}
    
    cache_key = f"zerobounce_guess_{first_name}_{last_name}_{domain}_{middle_name or ''}"
    logger.info(f"guess_email_with_zero_bounce: Checking cache with key: {cache_key}")
    cached_response = retrieve_output(cache_key, domain)
    if cached_response is not None:
        logger.info("Cache hit for ZeroBounce guess.")
        return json.loads(cached_response[0]) if cached_response else {}

    logger.info("No cache hit, proceeding to call ZeroBounce guessFormat.")
    ZERO_BOUNCE_API_KEY = get_zero_bounce_access_token(tool_config)
    base_url = "https://api.zerobounce.net/v2/guessformat"
    query_params = (
        f"?api_key={ZERO_BOUNCE_API_KEY}"
        f"&domain={domain}"
        f"&first_name={first_name or ''}"
        f"&middle_name={middle_name or ''}"
        f"&last_name={last_name or ''}"
    )
    url = base_url + query_params
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                logger.warning("ZeroBounce guessFormat returned a non-200 response code.")
                content = await safe_read_json_or_text(response)
                logger.warning(f"[ZeroBounce] guessFormat error: {response.status} => {content}")
                raise Exception(f"[ZeroBounce] Error: {content}")
            result = await response.json()

    cache_output(cache_key, domain, [json.dumps(result)])
    logger.info("Exiting guess_email_with_zero_bounce.")
    return result

GUESS_EMAIL_TOOL_MAP = {
    "zerobounce": guess_email_with_zero_bounce,
}

# --------------------------------------------------------------------------------
# 4. High-Level Validation + Guess
# --------------------------------------------------------------------------------

allowed_check_email_tools = ["zerobounce", "debounce"]

TOOL_NAME_TO_FUNCTION_MAP = {
    "zerobounce": check_email_validity_with_zero_bounce,
    "debounce": check_email_validity_with_debounce
}

@assistant_tool
async def check_email_validity(
    email_id: str,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, bool]:
    """
    Validate an email address by choosing the appropriate tool based on tool_config.

    Returns:
        dict: {"is_valid": True/False}.
    """
    logger.info("Entering check_email_validity method.")
    if not tool_config:
        raise ValueError("No tool configuration found.")

    chosen_tool_func = None
    for item in tool_config:
        name = item.get("name")
        if name in TOOL_NAME_TO_FUNCTION_MAP and name in allowed_check_email_tools:
            chosen_tool_func = TOOL_NAME_TO_FUNCTION_MAP[name]
            break

    if not chosen_tool_func:
        logger.warning("No suitable email validation tool found.")
        raise ValueError("No suitable email validation tool found in tool_config.")

    result = await chosen_tool_func(email_id, tool_config)
    logger.info("Exiting check_email_validity method.")
    return result

@assistant_tool
async def guess_email(
    first_name: str,
    last_name: str,
    domain: str,
    middle_name: Optional[str],
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Attempt to guess the email using the provider indicated in the tool_config.

    For now, only ZeroBounce is implemented. Extend as needed.
    """
    logger.info("Entering guess_email method.")
    if not tool_config:
        raise ValueError("No tool configuration found for guessing emails.")

    chosen_guess_func = None
    for item in tool_config:
        name = item.get("name")
        if name in GUESS_EMAIL_TOOL_MAP:
            chosen_guess_func = GUESS_EMAIL_TOOL_MAP[name]
            break

    if not chosen_guess_func:
        logger.warning("No suitable guess tool found.")
        raise ValueError("No suitable guess tool found in tool_config.")

    result = await chosen_guess_func(first_name, last_name, domain, middle_name, tool_config)
    logger.info("Exiting guess_email method.")
    return result

# --------------------------------------------------------------------------------
# 5. Orchestrating everything in a single function
# --------------------------------------------------------------------------------

@assistant_tool
async def process_email_properties(
    input_properties: Dict[str, Any],
    tool_config: Optional[List[Dict]] = None
) -> None:
    """
    1. Check if `input_properties["email"]` is present and non-empty.
    2. If present, validate the email.
       - If invalid, guess a new one.
    3. If empty, also guess a new one using domain + name fields.
    4. If guessed email is "valid" with "HIGH" confidence, replace `input_properties["email"]`.
       Otherwise, store guess in `additional_properties["zerobounce_guess_email"]`.
    """
    logger.info("Entering process_email_properties.")
    first_name = input_properties.get("first_name", "")
    last_name = input_properties.get("last_name", "")
    email = input_properties.get("email", "")
    additional_properties = input_properties.get("additional_properties", {})
    logger.info("Validating existing email or guessing new one.")
    if email:
        val_result = await check_email_validity(email, tool_config)
        if not val_result["is_valid"]:
            logger.warning("Email was invalid; attempting to guess a new address.")
            guessed_result = await guess_email(first_name, last_name, extract_domain(email), "", tool_config)
            if is_guess_usable(guessed_result):
                input_properties["email"] = guessed_result["email"]
            else:
                additional_properties["zerobounce_guess_email"] = guessed_result.get("email", "")
                input_properties["email"] = ""
    else:
        domain = input_properties.get("primary_domain_of_organization", "")
        if not domain:
            additional_properties["zerobounce_guess_email"] = ""
            input_properties["email"] = ""
            logger.info("Exiting process_email_properties.")
            return
        guessed_result = await guess_email(first_name, last_name, domain, "", tool_config)
        if is_guess_usable(guessed_result):
            input_properties["email"] = guessed_result["email"]
        else:
            additional_properties["zerobounce_guess_email"] = guessed_result.get("email", "")
            input_properties["email"] = ""
    input_properties["additional_properties"] = additional_properties
    logger.info("Exiting process_email_properties.")

# --------------------------------------------------------------------------------
# 6. Helper Functions
# --------------------------------------------------------------------------------

async def safe_read_json_or_text(response: aiohttp.ClientResponse) -> Any:
    """
    Safely attempts to parse an aiohttp response as JSON, else returns text.
    """
    try:
        return await response.json()
    except Exception:
        return await response.text()

def extract_domain(email: str) -> str:
    """Extract domain from email ( user@domain.com -> domain.com )."""
    if "@" not in email:
        return ""
    return email.split("@")[-1].strip()

def is_guess_usable(guess_result: Dict[str, Any]) -> bool:
    """
    Updated Behavior:
    Accept the guess as usable if email_confidence in guess_result is "high" or "medium".
    """
    if not guess_result:
        return False
    email_confidence = guess_result.get("email_confidence", "").lower()
    return email_confidence in ["high", "medium"]