from agent_client import call_advisor_remote, call_critic_remote

MAX_ITERATIONS = 3


async def run_orchestration(query: str) -> str:
    """Runs the advisor->critic loop and returns the final response."""
    messages = [{"role": "user", "content": query}]

    for iteration in range(MAX_ITERATIONS):
        # Step 1: Call advisor
        advisor_result = await call_advisor_remote(messages)
        draft = advisor_result.get("content", "")

        # Step 2: Call critic
        critic_result = await call_critic_remote(draft)
        critic_response = critic_result.get("content", "")

        if "APPROVED" in critic_response.upper():
            return draft

        # Critic had feedback — add it and loop again
        messages.append({"role": "assistant", "content": draft})
        messages.append({
            "role": "user",
            "content": f"Clinical Critic feedback: {critic_response}. Please revise.",
        })

    # If max iterations reached, return the last draft
    return draft
