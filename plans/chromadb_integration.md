# Task Plan: ChromaDB Vector Database Storage Integration

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Dependency Update**: Add `chromadb` and `llama-index-vector-stores-chroma` to `backend/requirements.txt` and install
- [x] **Vector Store Implementation**: Create `/backend/rag/vector_store.py` to handle database storage (under 70 lines)
- [x] **Pipeline Integration**: Modify `/backend/rag/pipeline.py` to persist chunk nodes into ChromaDB upon parsing
- [x] **Verification**: Validate data persistence and retrieval from ChromaDB local files
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Persist parsed and chunked document nodes into a local vector database.
- **Vector DB**: Use **ChromaDB** with LlamaIndex's `ChromaVectorStore` integration.
- **Persistence**: Save database files locally in `/backend/rag/chroma_db/`.
- **Embedding Model**: Configure LlamaIndex globally with **OpenAI's `text-embedding-3-small`** model set to **768 dimensions**.
- Keep all files strictly under the **70-line limit**.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/backend/requirements.txt` – Add `chromadb` and `llama-index-vector-stores-chroma`.
- [ ] `/backend/rag/vector_store.py` – Manage ChromaDB initialization, document indexing, and persistence (approx 35 lines).
- [ ] `/backend/rag/pipeline.py` – Call the vector store indexing function immediately after chunking.

### ⚙️ Vector Store Implementation (`/backend/rag/vector_store.py`)
```python
import os
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import TextNode

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "chroma_db")

# Globally configure LlamaIndex to use OpenAI text-embedding-3-small with 768 dimensions
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    dimensions=768
)

def add_chunks_to_vector_store(chunks: list, filename: str) -> None:
    """Converts chunk dicts to TextNodes and indexes them in ChromaDB using OpenAI embeddings."""
    db_client = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db_client.get_or_create_collection("onco_agent")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    nodes = []
    for c in chunks:
        nodes.append(TextNode(
            text=c["text"],
            id_=c["id"],
            metadata=c["metadata"]
        ))
        
    # Index nodes (persisted automatically via Chroma client using Settings.embed_model)
    VectorStoreIndex(nodes, storage_context=storage_context)
    print(f"Indexed {len(nodes)} chunks in ChromaDB for {filename}")
```

---

## 3. Verification & Testing Plan
- [ ] Upload a test file via the Document center.
- [ ] Verify that `/backend/rag/chroma_db/` folder is created on disk.
- [ ] Confirm that terminal output shows the indexing success message.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
