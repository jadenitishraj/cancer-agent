import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are OncoAgent, a specialized oncology research assistant. "
    "Provide clinical insights, targeted therapy guidelines (e.g. EGFR, BRCA), "
    "and trial criteria matching. Be professional, structured, and medically accurate. "
    "Use markdown (bolding, lists) to format your replies."
)

chat_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    openai_api_key=api_key
) if api_key else None

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{query}")
])

chain = prompt | chat_model if chat_model else None

def get_clinical_response(query: str) -> str:
    if not chain:
        return "⚠️ OncoAgent: LangChain model not configured. Please add OPENAI_API_KEY to your .env file."
    
    try:
        response = chain.invoke({"query": query})
        return str(response.content)
    except Exception as e:
        return f"⚠️ OncoAgent API Error: {str(e)}"
