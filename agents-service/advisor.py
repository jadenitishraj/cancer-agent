import os
import requests
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool

from config import SYSTEM_PROMPT, TOOLS_SERVICE_URL

chat_model = (
    ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=os.getenv("OPENAI_API_KEY"))
    if os.getenv("OPENAI_API_KEY")
    else None
)


@tool
def retrieve_clinical_guidelines(query: str) -> str:
    """Retrieves relevant cancer reference materials, clinical trials, and oncology guidelines from the local vector database."""
    resp = requests.post(
        f"{TOOLS_SERVICE_URL}/tools/retrieve_clinical_guidelines",
        json={"query": query},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("result", "No results found.")


llm_with_tools = chat_model.bind_tools([retrieve_clinical_guidelines]) if chat_model else None


async def call_advisor(messages_data: list[dict]) -> dict:
    """Runs the advisor agent with tool-calling loop."""
    messages = [("system", SYSTEM_PROMPT)]
    for m in messages_data:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    while True:
        response = await llm_with_tools.ainvoke(messages)
        if not response.tool_calls:
            return {"role": "assistant", "content": response.content}
        messages.append(response)
        for tc in response.tool_calls:
            context = retrieve_clinical_guidelines.invoke(tc["args"]["query"])
            messages.append(ToolMessage(content=context, tool_call_id=tc["id"]))
