import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

CRITIC_PROMPT = (
    "You are a Clinical Critic. Review OncoAgent's draft for clinical accuracy and guideline compliance. "
    "If the draft response is accurate, formatted correctly, or if OncoAgent correctly states it does not know or "
    "cannot find the information in the database, reply with ONLY: APPROVED. "
    "Otherwise, provide constructive feedback on what needs to be changed."
)

chat_model = (
    ChatOpenAI(model="gpt-4o-mini", temperature=0.1, openai_api_key=os.getenv("OPENAI_API_KEY"))
    if os.getenv("OPENAI_API_KEY")
    else None
)


async def call_critic(draft_content: str) -> dict:
    """Reviews the advisor's draft and returns approval or feedback."""
    prompt = f"{CRITIC_PROMPT}\n\nDraft response to review:\n{draft_content or 'No draft response found.'}"
    response = await chat_model.ainvoke([("user", prompt)])
    return {"role": "assistant", "content": response.content}
