# Task Plan: RAG Document Parsing & Pipeline Setup

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Dependency Update**: Add `pymupdf` to `backend/requirements.txt` and install
- [x] **Parser Implementation**: Create `/backend/rag/parser.py` using `pymupdf` (under 70 lines)
- [x] **Pipeline Implementation**: Create `/backend/rag/pipeline.py` to process the uploaded file immediately (under 70 lines)
- [x] **API Endpoint**: Integrate parsing execution directly inside the POST `/api/upload` endpoint in `main.py`
- [x] **Verification**: Validate text extraction immediately upon file upload via the frontend
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Build the initial stage of the RAG (Retrieval-Augmented Generation) pipeline by implementing document parsing.
- **Library**: Use `pymupdf` (Fitz) to open, read, and extract raw text from PDF files.
- **Immediate Execution**: Trigger the parsing pipeline directly in the file upload request loop.
- **Modular Code**:
  - `/backend/rag/parser.py` – Pure parsing utility for different file types (PDF, TXT, MD).
  - `/backend/rag/pipeline.py` – Coordinates file paths, triggers parsing, and logs the character extraction count.
- Keep all files strictly under the **70-line limit**.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/backend/requirements.txt` – Add `pymupdf`.
- [ ] `/backend/rag/parser.py` – Parser utilities for PDF, TXT, MD (approx 30 lines).
- [ ] `/backend/rag/pipeline.py` – Orchestrates immediate parsing of a saved file (approx 25 lines).
- [ ] `/backend/main.py` – Update POST `/api/upload` to run the pipeline on the uploaded file and return success state along with character counts.

### ⚙️ Parser Implementation (`/backend/rag/parser.py`)
```python
import fitz  # PyMuPDF

def parse_pdf(file_path: str) -> str:
    """Extracts text from a PDF file page by page using PyMuPDF."""
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)

def parse_txt(file_path: str) -> str:
    """Extracts text from a plain text or markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def parse_file(file_path: str) -> str:
    """Parses a file based on its extension."""
    ext = file_path.lower().split(".")[-1]
    if ext == "pdf":
        return parse_pdf(file_path)
    elif ext in ("txt", "md"):
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
```

### ⚙️ Pipeline Implementation (`/backend/rag/pipeline.py`)
```python
import os
from rag.parser import parse_file

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "files")

def run_parsing_pipeline(filename: str) -> dict:
    """Parses a specific file from the upload directory and returns character count info."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}
        
    try:
        extracted_text = parse_file(file_path)
        char_count = len(extracted_text)
        print(f"Successfully parsed {filename} ({char_count} chars)")
        return {
            "status": "parsed",
            "filename": filename,
            "char_count": char_count
        }
    except Exception as e:
        print(f"Error parsing {filename}: {str(e)}")
        return {
            "status": "error",
            "filename": filename,
            "message": str(e)
        }
```

---

## 3. Verification & Testing Plan
- [ ] Upload a file from the frontend "Documents" tab.
- [ ] Confirm that the backend immediately reports the success of the upload AND shows the parsed character counts in the terminal logs.
- [ ] Ensure all backend code files remain under 70 lines.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
