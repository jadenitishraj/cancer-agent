from fastapi import FastAPI
from pydantic import BaseModel

from advisor import call_advisor
from critic import call_critic

app = FastAPI(title="Agents Service")


class MessageItem(BaseModel):
    role: str
    content: str


class AdvisorRequest(BaseModel):
    messages: list[MessageItem]


class CriticRequest(BaseModel):
    draft_content: str


@app.post("/agents/advisor")
async def advisor_endpoint(request: AdvisorRequest):
    """Invokes the advisor agent with the provided message history."""
    messages_data = [m.model_dump() for m in request.messages]
    result = await call_advisor(messages_data)
    return result


@app.post("/agents/critic")
async def critic_endpoint(request: CriticRequest):
    """Invokes the critic agent to review a draft response."""
    result = await call_critic(request.draft_content)
    return result


@app.get("/health")
async def health():
    return {"status": "ok", "service": "agents-service"}
