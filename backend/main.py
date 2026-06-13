from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from advisor import get_clinical_response
from file_handler import save_uploaded_file, get_uploaded_files
from rag.pipeline import run_parsing_pipeline

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

@app.post("/api/upload")
async def upload_file(file: UploadFile):
    filename = save_uploaded_file(file)
    pipeline_result = run_parsing_pipeline(filename)
    return {
        "status": "success",
        "filename": filename,
        "pipeline": pipeline_result
    }

@app.get("/api/files")
async def get_files():
    files = get_uploaded_files()
    results = []
    for f in files:
        try:
            _, doc_type = parse_file(os.path.join(os.path.dirname(__file__), "rag", "files", f))
        except Exception:
            doc_type = "unknown"
        results.append({"name": f, "type": doc_type})
    return {"files": results}



