import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

load_dotenv()

TOOLS_SERVICE_URL = os.getenv("TOOLS_SERVICE_URL", "http://tools-service:8003")

SYSTEM_PROMPT = (
    "You are OncoAgent, a specialized oncology research assistant. "
    "You must search the local database using the retrieve_clinical_guidelines tool for ANY medical, cancer, "
    "or oncology-related questions. Do not answer from general knowledge if you can retrieve data. "
    "Provide clinical insights, targeted therapy guidelines, and trial matching. "
    "Use markdown (bolding, lists) to format your replies. if you do not find in our data say, you dont know. dont answer on your own"
)


def _build_tool_schema():
    """Returns the tool definition for the LLM to call."""
    return {
        "type": "function",
        "function": {
            "name": "retrieve_clinical_guidelines",
            "description": "Retrieves relevant cancer reference materials, clinical trials, and oncology guidelines from the local vector database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query for clinical guidelines."}
                },
                "required": ["query"],
            },
        },
    }
