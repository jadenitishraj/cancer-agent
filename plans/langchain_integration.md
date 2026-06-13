# Task Plan: LangChain Integration for Oncology Chatbot

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Dependency Update**: Add `langchain-openai` to `requirements.txt` and install
- [x] **Backend Refactoring**: Rewrite `advisor.py` to use LangChain ChatOpenAI and ChatPromptTemplate (under 70 lines)
- [x] **Verification**: Validate functional LangChain chain invoke responses
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Transition the backend oncology research advisor from raw `openai` library calls to a `LangChain` pipeline.
- Maintain the strict **70-line limit** per backend file.
- Use modern LCEL (LangChain Expression Language) syntax for prompt templating and invocation.
- Handle fallback states gracefully if the key is missing or the invocation fails.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/backend/requirements.txt` – Add `langchain-openai`.
- [ ] `/backend/advisor.py` – Refactor imports and LLM setup to use LangChain objects.

### ⚙️ Backend Implementation
Update `/backend/advisor.py` to run:
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

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
```
*(Total lines: ~35, well below the 70-line limit).*

---

## 3. Verification & Testing Plan
- [ ] Install package updates via `pip install -r requirements.txt`.
- [ ] Verify the Uvicorn reload doesn't trigger any import errors.
- [ ] Execute chatbot queries and check that responses are returned via the LangChain run execution.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
