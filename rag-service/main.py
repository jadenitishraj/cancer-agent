import os
import shutil
from fastapi import FastAPI, UploadFile, Query
from pydantic import BaseModel

from pdf_reader import parse_file
from chunker import chunk_document
from vector_store import add_chunks_to_vector_store, retrieve_from_vector_store

app = FastAPI(title="RAG Service")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "files")


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 3


@app.post("/ingest")
async def ingest_file(file: UploadFile):
    """Receives a file, parses, chunks, and indexes it into ChromaDB."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text, doc_type = parse_file(file_path)
        chunks = chunk_document(extracted_text, file.filename, doc_type)
        add_chunks_to_vector_store(chunks, file.filename)
        return {
            "status": "parsed",
            "filename": file.filename,
            "char_count": len(extracted_text),
            "doc_type": doc_type,
            "chunk_count": len(chunks),
        }
    except Exception as e:
        return {"status": "error", "filename": file.filename, "message": str(e)}


@app.post("/retrieve")
async def retrieve_docs(request: RetrieveRequest):
    """Queries ChromaDB for matching documents."""
    results = retrieve_from_vector_store(request.query, request.top_k)
    return {"results": results}


@app.get("/files")
async def list_files():
    """Lists all uploaded files."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    files = [
        f
        for f in os.listdir(UPLOAD_DIR)
        if os.path.isfile(os.path.join(UPLOAD_DIR, f)) and not f.startswith(".")
    ]
    file_info = []
    for f in files:
        try:
            _, doc_type = parse_file(os.path.join(UPLOAD_DIR, f))
        except Exception:
            doc_type = "unknown"
        file_info.append({"name": f, "type": doc_type})
    return {"files": file_info}
