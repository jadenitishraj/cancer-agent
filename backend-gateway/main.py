import os
import requests
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://langraph-orchestrator:8001")
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://rag-service:8004")

app = FastAPI(title="OncoAgent API Gateway")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/api/message")
async def get_message():
    return {
        "status": "online",
        "message": "Hello from the OncoAgent API Gateway!",
    }
