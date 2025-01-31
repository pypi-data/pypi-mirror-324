import os
import uuid
import time
import asyncio
import aiohttp
from typing import Any, Dict, Optional, List

def get_task_agent_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Retrieves the TaskAgent access token from the provided tool configuration or environment.
    Raises:
        ValueError: If the token is not found.
    """
    if tool_config:
        task_agent_config = next(
            (item for item in tool_config if item.get("name") == "dhisana_workflow_tools"), None
        )
        if task_agent_config:
            config_map = {
                c["name"]: c["value"]
                for c in task_agent_config.get("configuration", [])
                if c
            }
            TASK_AGENT_API_KEY = config_map.get("apiKey")
        else:
            TASK_AGENT_API_KEY = None
    else:
        TASK_AGENT_API_KEY = None

    TASK_AGENT_API_KEY = TASK_AGENT_API_KEY or os.getenv("TASK_AGENT_API_KEY", "test")
    if not TASK_AGENT_API_KEY:
        raise ValueError("TASK_AGENT_API_KEY not found in config or env.")
    return TASK_AGENT_API_KEY


async def execute_task(
    command_name: str,
    command_args: Dict[str, Any],
    max_timeout: float = 2400,
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    1. Enqueues a task to the TaskAgent service using /add_agent_task.
    2. Polls /get_agent_task_result until completion or until max_timeout has passed.
    3. Removes task from status queue and pending queue.
    4. Returns the command result.

    This function is asynchronous and will yield control during sleep intervals,
    allowing other tasks to run concurrently.
    """
    # ----------------------------------------------------------------
    # CONFIG & PREP
    # ----------------------------------------------------------------
    TASK_AGENT_API_KEY = get_task_agent_access_token(tool_config)

    # Unique ID for this request
    request_id = str(uuid.uuid4())
    api_base_url = os.environ.get("AGENT_SERVICE_URL", "https://api.dhisana.ai/v1")

    # The payload to send when adding a task
    payload = {
        "command_request_id": request_id,
        "command_name": command_name,
        "command_args": command_args
    }

    # Build the various endpoints
    add_task_url = f"{api_base_url}/add_agent_task"
    get_task_result_url = f"{api_base_url}/get_agent_task_result"
    remove_task_url = f"{api_base_url}/remove_agent_task"
    remove_task_result_url = f"{api_base_url}/remove_agent_task_result"

    headers = {
        "Authorization": f"Bearer {TASK_AGENT_API_KEY}",
        "Content-Type": "application/json"
    }

    final_result: Dict[str, Any] = {}

    async with aiohttp.ClientSession() as session:
        # ----------------------------------------------------------------
        # 1) ENQUEUE THE TASK
        # ----------------------------------------------------------------
        async with session.post(
            add_task_url,
            json=payload,
            headers=headers
        ) as response:
            if response.status != 200:
                raise Exception(f"Failed to add task. Status code: {response.status}")
            add_resp = await response.json()
            if add_resp.get("status") != "OK":
                raise Exception(f"Error adding task: {add_resp}")

        # ----------------------------------------------------------------
        # 2) POLL UNTIL THE TASK IS COMPLETED OR TIMEOUT
        # ----------------------------------------------------------------
        start_time = time.time()
        end_time = start_time + max_timeout

        while time.time() < end_time:
            # Poll for the result
            async with session.post(
                get_task_result_url,
                params={"request_id": request_id},
                headers=headers
            ) as poll_response:
                if poll_response.status != 200:
                    raise Exception(
                        f"Failed to poll task result. "
                        f"Status code: {poll_response.status}"
                    )
                poll_data = await poll_response.json()

            if poll_data.get("status") == "ERROR":
                # Something went wrong in the service
                msg = poll_data.get("message", "Unknown error during polling")
                raise Exception(f"Task {request_id} returned an error: {msg}")

            current_status = poll_data.get("current_status", "")
            if current_status == "completed":
                # We have a final result
                final_result = poll_data.get("result", {})
                break

            # Not yet completed; wait a bit before polling again
            await asyncio.sleep(20)
        else:
            # If we exit the while-loop normally (no break), it's a timeout
            raise TimeoutError(
                f"Task {request_id} did not complete within {max_timeout} seconds."
            )

        # ----------------------------------------------------------------
        # 3) REMOVE THE TASK RESULTS FROM THE STATUS QUEUE
        # ----------------------------------------------------------------
        async with session.delete(
            remove_task_result_url,
            params={"request_id": request_id},
            headers=headers
        ) as remove_res_status:
            if remove_res_status.status != 200:
                raise Exception(
                    f"Failed to remove task result. "
                    f"Status code: {remove_res_status.status}"
                )
            remove_status_resp = await remove_res_status.json()
            if remove_status_resp.get("status") != "OK":
                # Not a fatal error, but raise to be safe
                raise Exception(f"Error removing task result: {remove_status_resp}")

    # ----------------------------------------------------------------
    # 4) RETURN THE RESULT
    # ----------------------------------------------------------------
    return final_result