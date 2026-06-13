import os
import shutil
from fastapi import UploadFile

# Store files in a RAG storage subdirectory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "rag", "files")

def save_uploaded_file(file: UploadFile) -> str:
    """Saves an uploaded file to the local RAG files directory."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return file.filename

def get_uploaded_files() -> list[str]:
    """Lists all files in the local RAG files directory."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f)) and not f.startswith(".")]
