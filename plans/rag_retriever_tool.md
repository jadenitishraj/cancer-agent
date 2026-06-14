# Task Plan: LangChain RAG Retrieval Tool & Agent Update

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Tool Implementation**: Create `/backend/tools/rag_retriever.py` with `@tool` decorator (under 70 lines)
- [x] **Agent Update**: Refactor `/backend/advisor.py` to bind the RAG tool, update system prompt to enforce tool usage, and run via a tool-calling executor (under 70 lines)
- [x] **Verification**: Validate tool call, logs, and final response generation
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Create a formal LangChain tool that retrieves oncology context from the local ChromaDB database using LlamaIndex, and wire it to the OncoAgent chat loop.
- **Rules**: Use only LlamaIndex for retrieval from ChromaDB inside the tool.
- **LangChain Tool**: Use `@tool` decorator.
- **System Prompt**: Explicitly instruct the agent to use the `retrieve_clinical_guidelines` tool to retrieve context for any medical or oncology questions.
- **Aesthetic / Logging**: Print structured logs in the console to show search queries and retrieved node snippets.
- Keep all backend files under the **70-line limit**.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/backend/tools/rag_retriever.py` – Implement the LangChain tool wrapping LlamaIndex database retriever.
- [ ] `/backend/advisor.py` – Update agent model to bind the tool, set system prompt to use the tool, and orchestrate execution.

### ⚙️ Tool Implementation (`/backend/tools/rag_retriever.py`)
```python
import os
import chromadb
from langchain_core.tools import tool
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "chroma_db")

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    dimensions=768
)

@tool
def retrieve_clinical_guidelines(query: str) -> str:
    """Retrieves relevant cancer reference materials, clinical trials, and oncology guidelines from the local vector database."""
    print(f"\n🔍 [RAG Tool] Querying ChromaDB for: '{query}'")
    
    db_client = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db_client.get_or_create_collection("onco_agent")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)
    
    retriever = index.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(query)
    
    if not nodes:
        print("🔍 [RAG Tool] No matching documents found in database.")
        return "No relevant oncology documents found."
        
    print(f"🔍 [RAG Tool] Found {len(nodes)} matches. Retrieving contents:")
    context_parts = []
    for i, node in enumerate(nodes):
        snippet = node.node.get_content().strip()
        score = node.score if node.score is not None else 0.0
        print(f"  -> Match {i+1} [Score: {score:.4f}]: {snippet[:100]}...")
        context_parts.append(f"--- Doc Chunk {i+1} ---\n{snippet}")
        
    return "\n\n".join(context_parts)
```

### ⚙️ Agent Update (`/backend/advisor.py`)
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.rag_retriever import retrieve_clinical_guidelines

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are OncoAgent, a specialized oncology research assistant. "
    "You must search the local database using the retrieve_clinical_guidelines tool for ANY medical, cancer, "
    "or oncology-related questions. Do not answer from general knowledge if you can retrieve data. "
    "Provide clinical insights, targeted therapy guidelines, and trial matching. "
    "Use markdown (bolding, lists) to format your replies."
)

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=api_key)
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

tools = [retrieve_clinical_guidelines]
agent = create_tool_calling_agent(chat_model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def get_clinical_response(query: str) -> str:
    if not api_key:
        return "⚠️ OncoAgent: API Key not configured."
    try:
        res = agent_executor.invoke({"input": query, "chat_history": []})
        return str(res["output"])
    except Exception as e:
        return f"⚠️ OncoAgent API Error: {str(e)}"
```

---

## 3. Verification & Testing Plan
- [ ] Ask a query related to a uploaded document (e.g. "What is the list of cancer types?").
- [ ] Verify that the backend console shows the `[RAG Tool] Querying ChromaDB` log statement.
- [ ] Confirm that retrieved chunks are printed in stdout and merged into the agent's final answer.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
