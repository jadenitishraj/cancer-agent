# Planning: Decoupling OncoAgent into Modular Microservices

This plan outlines how the monolithic repository will be refactored into independent services, how they will communicate, and how Docker containerization will be set up.

---

## 1. Target Microservices & Repositories

We will split the system into **6 individual service directories** under the root folder:

| Service Name | Directory Name | Primary Role | Port | Key Technologies |
|---|---|---|---|---|
| **Frontend** | `/frontend` | User UI, handles chat input/streaming and PDF file uploads | `3000` | Next.js, React |
| **API Gateway** | `/backend-gateway` | The main API entry point (accepts user queries and routes file uploads) | `8000` | FastAPI, Uvicorn |
| **LangGraph Orchestrator** | `/langraph-orchestrator` | Defines and runs the LangGraph StateGraph workflow (`advisor` <-> `critic`) | `8001` | LangGraph, FastAPI |
| **Agents Service** | `/agents-service` | Executes LLM model logic for the `advisor` and `critic` nodes | `8002` | LangChain, OpenAI, FastAPI |
| **Tools Service** | `/tools-service` | Standardizes and executes tool calls (like querying vector database) | `8003` | LangChain, FastAPI |
| **RAG Service** | `/rag-service` | Manages file chunking, document parsing, and ChromaDB vector operations | `8004` | LlamaIndex, FastAPI |
| **ChromaDB Server** | *(Docker-Only)* | Centralized vector database server | `8000` | ChromaDB |

---

## 2. Communication Protocols & Data Flow

To decouple python imports, we will convert internal Python method calls into network-based HTTP requests.

### A. Chat Ingestion Flow
1. **User** submits a chat query via `/frontend`.
2. **Frontend** POSTs to `/backend-gateway` (`/api/chat`).
3. **Backend-Gateway** forwards the chat request to `/langraph-orchestrator` (`/orchestrate`).
4. **LangGraph Orchestrator** processes the graph:
   - Calls **Agents Service** (`/agents/advisor`) to invoke the advisor agent.
   - **Agents Service** realizes it needs to search. It sends an HTTP POST request to the **Tools Service** (`/tools/retrieve_clinical_guidelines`).
   - **Tools Service** queries the **RAG Service** `/retrieve` endpoint.
   - **RAG Service** executes similarity search against **ChromaDB Server** and returns results back up the chain.
   - Once the Advisor responds, **LangGraph Orchestrator** calls **Agents Service** (`/agents/critic`) for clinical validation.
   - The final stream is piped back to the user.

### B. Ingestion (File Upload) Flow
1. **User** uploads a PDF in `/frontend`.
2. **Frontend** POSTs to `/backend-gateway` (`/api/upload`).
3. **Backend-Gateway** saves the file locally and forwards it via a multipart form request to `/rag-service` (`/ingest`).
4. **RAG Service** runs parsing, chunking, and writes the vectors directly to `/chromadb` via TCP.

---

## 3. Step-by-Step Migration Plan

We will perform the migration in the following order:

### Phase 1: Environment & Shared DB Setup
1. Create a `docker-compose.yml` in the root folder containing the official **ChromaDB** image.
2. Verify we can spin up ChromaDB and connect to it as a network service.

### Phase 2: Create RAG Service (`/rag-service`)
1. Create `/rag-service` directory.
2. Move `/backend/rag` contents into the service.
3. Replace `chromadb.PersistentClient` in RAG vector store code with `chromadb.HttpClient(host="chromadb", port=8000)`.
4. Wrap the ingestion and retrieval routines inside a FastAPI application (`main.py`) with `/ingest` and `/retrieve` endpoints.
5. Create a `Dockerfile` and `requirements.txt`.

### Phase 3: Create Tools Service (`/tools-service`)
1. Create `/tools-service` directory.
2. Move `/backend/tools` contents into the service.
3. Rewrite the `retrieve_clinical_guidelines` tool to make an HTTP request to `/rag-service/retrieve` instead of executing LlamaIndex locally.
4. Expose the tools via a FastAPI `/tools/retrieve_clinical_guidelines` endpoint.
5. Create a `Dockerfile` and `requirements.txt`.

### Phase 4: Create Agents Service (`/agents-service`)
1. Create `/agents-service` directory.
2. Move `/backend/agents` contents into the service.
3. In `advisor.py`, replace local tool execution references with HTTP requests to the Tools Service.
4. Wrap both `advisor` and `critic` nodes in FastAPI endpoints.
5. Create a `Dockerfile` and `requirements.txt`.

### Phase 5: Create LangGraph Orchestrator (`/langraph-orchestrator`)
1. Create `/langraph-orchestrator` directory.
2. Move `/backend/langraph` contents into the service.
3. In `agent_graph.py`, replace direct imports of `call_model` and `call_critic` with HTTP calls to the Agents Service.
4. Wrap the state machine and the response stream logic in a FastAPI streaming endpoint.
5. Create a `Dockerfile` and `requirements.txt`.

### Phase 6: Create API Gateway (`/backend-gateway`)
1. Create `/backend-gateway` directory.
2. Move `main.py` and file upload handling.
3. Update routing to target `/langraph-orchestrator` and `/rag-service`.
4. Create a `Dockerfile` and `requirements.txt`.

### Phase 7: Connect Frontend and Launch
1. Update `/frontend` environment variables to target the `/backend-gateway`.
2. Launch everything using `docker-compose up --build`.

---

## 4. Verification Checklist

To ensure safety and functionality, we will verify:
- [ ] ChromaDB starts up and persists data correctly.
- [ ] RAG ingestion works by uploading a test PDF file.
- [ ] Vector retrieval returns matching nodes via HTTP.
- [ ] Agent calls are routed successfully through LangGraph.
- [ ] Next.js frontend connects without CORS or network resolution errors.
