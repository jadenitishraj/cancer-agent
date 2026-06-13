from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from advisor import get_clinical_response

app = FastAPI(title="OncoAgent Backend")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
        "message": "Hello from the FastAPI Backend!"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    response_text = get_clinical_response(request.message)
    return {"response": response_text}
