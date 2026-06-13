# Task Plan: Claude-Themed Oncology Chatbot UI & API Integration

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Frontend Implementation**: Design Claude-themed UI and chat interaction
- [x] **Backend Implementation**: Build robust, modular chat endpoint (under 70 lines)
- [x] **Verification**: Validate interface aesthetic quality and connection flow
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Build a visually stunning oncology chatbot called **OncoAgent** with a theme inspired by Claude's clean, warm, minimalist aesthetic.
- **Frontend**:
  - Immersive warm-dark theme (charcoal, deep ivory/amber borders, clean typography).
  - Sidebar for chat history + "New Chat" button.
  - Center workspace with suggested prompt pills for quick oncology queries.
  - Message bubble streaming/rendering with markdown-like formatting.
  - Clean textarea with attachments and send controls.
- **Backend**:
  - Expose a POST `/api/chat` endpoint to receive messages.
  - Implement a mock/simulated medical advisor engine (under 70 lines of code) that responds intelligently to key cancer questions (genomics, clinical trials, staging) and supports general cancer discussions.
  - Keep all backend source files strictly under **70 lines of code**.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/frontend/src/app/page.tsx` – Overwrite with the Claude-themed chatbot page.
- [ ] `/frontend/src/app/page.module.css` – Add premium Claude chatbot styles (input boxes, speech bubbles, sidebar).
- [ ] `/backend/main.py` – Add a POST `/api/chat` endpoint (routing to the advisor).
- [ ] `/backend/advisor.py` – Create a new helper file for generating response payloads (must stay under 70 lines).

### 🎨 Frontend Implementation (Claude Chatbot Theme)
- **Theme Details**:
  - Background: Warm off-black `#181817`
  - User Message Bubble: Slate-grey `#262625`
  - Assistant Logo/Name: Warm peach/amber accent `#e05e36`
  - Borders: Minimal warm-grey `#333331`
- **Interactions**:
  - Streaming simulation (typing effect).
  - Instant loading skeletons.
  - Interactive suggestions: clicking a pill pre-fills and sends the query.

### ⚙️ Backend Implementation
- **`/backend/advisor.py`** (~50 lines):
  - Function `get_clinical_response(query: str) -> str`
  - If a query contains "EGFR" or "lung", return a detailed molecular analysis.
  - If it contains "breast" or "BRCA", return BRCA-mutation guidelines.
  - If it contains "trial" or "study", return target clinical trials search steps.
  - Provide a fallback friendly conversational medical AI assistant response otherwise.
- **`/backend/main.py`** (~35 lines):
  - Integrate `/api/chat` route with `get_clinical_response`.

---

## 3. Verification & Testing Plan
- [ ] Run the dev servers for both frontend and backend.
- [ ] Test typing, clicking suggestion pills, and sending messages.
- [ ] Verify CORS requests work without issues.
- [ ] Note: No automated browser-agent tests will be executed until the user explicitly confirms readiness.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
