from fastapi import FastAPI
from pydantic import BaseModel

from rag_tool import retrieve_clinical_guidelines

app = FastAPI(title="Tools Service")


class ToolRequest(BaseModel):
    query: str


@app.post("/tools/retrieve_clinical_guidelines")
async def run_retrieve_tool(request: ToolRequest):
    """Executes the RAG retrieval tool and returns context."""
    result = retrieve_clinical_guidelines(request.query)
    return {"result": result}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "tools-service"}
