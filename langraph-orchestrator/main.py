from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from workflow import run_orchestration

app = FastAPI(title="LangGraph Orchestrator")


class OrchestrateRequest(BaseModel):
    query: str


@app.post("/orchestrate")
async def orchestrate(request: OrchestrateRequest):
    """Runs the full advisor-critic workflow and returns the result."""
    result = await run_orchestration(request.query)
    return {"response": result}


@app.post("/orchestrate/stream")
async def orchestrate_stream(request: OrchestrateRequest):
    """Streams the orchestrated response back to the caller."""

    async def generate():
        result = await run_orchestration(request.query)
        # Stream the result in chunks for a smoother UX
        chunk_size = 50
        for i in range(0, len(result), chunk_size):
            yield result[i : i + chunk_size]

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "langraph-orchestrator"}
