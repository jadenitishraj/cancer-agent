# Task Plan: local File Upload Integration & RAG Storage Setup

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Backend Folder Setup**: Create `/backend/rag/files/` directory structure
- [x] **Backend Implementation**: Create file upload endpoint in FastAPI (under 70 lines)
- [x] **Frontend Implementation**: Add Tab navigation (Chat vs. Upload) and design a drag-and-drop file upload interface
- [x] **Verification**: Validate file upload transmission and verification on disk
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Add file upload support to let users upload medical reference documents (PDFs, TXT, etc.) directly from the frontend interface and store them in the backend for future RAG indexing.
- **Directories**:
  - Store files in `/backend/rag/files/`.
- **Frontend**:
  - Add a sub-navigation bar (or toggle tabs) to switch between the **OncoAgent Chat** workspace and the **Document Center**.
  - Create a premium drag-and-drop file upload UI with state trackers (uploading, success, error) and a table of uploaded documents.
- **Backend**:
  - Create a POST `/api/upload` multipart endpoint.
  - Safely write uploaded bytes to disk.
  - Keep all backend files under the **70-line limit**.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/backend/rag/files/` – Directory for uploaded documents.
- [ ] `/backend/file_handler.py` – Create module for saving files and listing stored documents (under 70 lines).
- [ ] `/backend/main.py` – Expose POST `/api/upload` and GET `/api/files` endpoints.
- [ ] `/frontend/src/app/page.tsx` – Refactor to include Tab navigation ("Chat" and "Documents") and the document upload form.
- [ ] `/frontend/src/app/page.module.css` – Add styles for the upload dropzone, files list table, and tab items.

### 🎨 Frontend Implementation (Document Upload Tab)
- Add a state variable `activeTab` ("chat" | "documents").
- When `activeTab === "documents"`, display:
  - A beautiful drag-and-drop area with dashed borders, file upload progress bar, and list of files currently stored on the backend.
  - A file picker to select text files, PDFs, or markdown files.
  - An instant file upload hook that sends the file to the backend `multipart/form-data` endpoint.

### ⚙️ Backend Implementation
- **`/backend/file_handler.py`** (~30 lines):
```python
import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "rag", "files")

def save_uploaded_file(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

def get_uploaded_files() -> list:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.listdir(UPLOAD_DIR)
```
- **`/backend/main.py`** (~50 lines):
  - Add imports from `file_handler`.
  - Add `/api/upload` endpoint.
  - Add `/api/files` endpoint.

---

## 3. Verification & Testing Plan
- [ ] Upload sample files (.txt, .pdf) from the frontend tab.
- [ ] Verify that files are correctly written to the `/backend/rag/files/` directory.
- [ ] Verify that the uploaded files immediately appear in the document list on the frontend.
- [ ] Note: No automated browser-agent tests will be executed until the user explicitly confirms readiness.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
