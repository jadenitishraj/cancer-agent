import os
import requests
from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from main import app, ChatRequest

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://langraph-orchestrator:8001")
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://rag-service:8004")


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Forwards chat queries to the LangGraph Orchestrator and streams the response."""

    def stream_response():
        try:
            resp = requests.post(
                f"{ORCHESTRATOR_URL}/orchestrate/stream",
                json={"query": request.message},
                stream=True,
                timeout=120,
            )
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    yield chunk
        except Exception as e:
            yield f"⚠️ OncoAgent API Error: {str(e)}"

    return StreamingResponse(stream_response(), media_type="text/plain")


@app.post("/api/upload")
async def upload_file(file: UploadFile):
    """Forwards file uploads to the RAG Service for ingestion."""
    try:
        files = {"file": (file.filename, file.file, file.content_type)}
        resp = requests.post(f"{RAG_SERVICE_URL}/ingest", files=files, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return {"status": "success", "filename": file.filename, "pipeline": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/files")
async def get_files():
    """Retrieves the file list from the RAG Service."""
    try:
        resp = requests.get(f"{RAG_SERVICE_URL}/files", timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"files": [], "error": str(e)}
