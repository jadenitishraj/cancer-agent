import os
import requests

AGENTS_SERVICE_URL = os.getenv("AGENTS_SERVICE_URL", "http://agents-service:8002")


async def call_advisor_remote(messages: list[dict]) -> dict:
    """Calls the remote Agents Service advisor endpoint."""
    response = requests.post(
        f"{AGENTS_SERVICE_URL}/agents/advisor",
        json={"messages": messages},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


async def call_critic_remote(draft_content: str) -> dict:
    """Calls the remote Agents Service critic endpoint."""
    response = requests.post(
        f"{AGENTS_SERVICE_URL}/agents/critic",
        json={"draft_content": draft_content},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
