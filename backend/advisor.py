import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools.rag_retriever import retrieve_clinical_guidelines

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are OncoAgent, a specialized oncology research assistant. "
    "You must search the local database using the retrieve_clinical_guidelines tool for ANY medical, cancer, "
    "or oncology-related questions. Do not answer from general knowledge if you can retrieve data. "
    "Provide clinical insights, targeted therapy guidelines, and trial matching. "
    "Use markdown (bolding, lists) to format your replies. if you do not find in our data say, you dont know. dont answer on your own"
)

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=api_key) if api_key else None
llm_with_tools = chat_model.bind_tools([retrieve_clinical_guidelines]) if chat_model else None

def get_clinical_response(query: str) -> str:
    if not llm_with_tools:
        return "⚠️ OncoAgent: Model or API Key not configured."
    try:
        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", query)
        ]
        ai_msg = llm_with_tools.invoke(messages)
        
        if ai_msg.tool_calls:
            tool_call = ai_msg.tool_calls[0]
            tool_query = tool_call["args"]["query"]
            
            # Execute tool
            context = retrieve_clinical_guidelines.invoke(tool_query)
            
            messages.append(ai_msg)
            messages.append({
                "role": "tool",
                "content": context,
                "tool_call_id": tool_call["id"]
            })
            final_msg = llm_with_tools.invoke(messages)
            return str(final_msg.content)
            
        return str(ai_msg.content)
    except Exception as e:
        return f"⚠️ OncoAgent API Error: {str(e)}"
