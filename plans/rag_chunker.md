# Task Plan: LAMA Index Multi-Strategy Chunking Pipeline

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Dependency Update**: Add `llama-index` and `llama-index-embeddings-openai` to `backend/requirements.txt` and install
- [x] **Chunker Implementation**: Create `/backend/rag/chunker.py` with 4 LlamaIndex splitters (under 70 lines)
- [x] **Pipeline Integration**: Modify `/backend/rag/pipeline.py` to route parsed text into the LlamaIndex chunker
- [x] **Verification**: Validate node creation and chunk metadata mapping
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Upgrade the RAG pipeline to chunk the extracted document text using LlamaIndex node splitters.
- **Rules**: Do not write custom text slicing code. Use only LlamaIndex splitters.
- **Chunk Size / Overlap**: Set the limit to **600** with **100** overlap for text splitting.
- **Strategies (4 Splitters)**:
  1. **Semantic Splitter** (`SemanticSplitterNodeParser` with `OpenAIEmbedding`): Used for `"paragraph"` documents.
  2. **Code Splitter** (`CodeSplitter`): Used for `"code"` documents.
  3. **Sentence Window Splitter** (`SentenceWindowNodeParser`): Used for `"transcript"` documents to preserve surrounding conversation context.
  4. **Sentence Splitter** (`SentenceSplitter`): Standard splitter used as a fallback and for `"table_heavy"` files.
- Keep all backend files under the **70-line limit**.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/backend/requirements.txt` – Add `llama-index` and `llama-index-embeddings-openai`.
- [ ] `/backend/rag/chunker.py` – Implement strategy selection and chunk execution (approx 45 lines).
- [ ] `/backend/rag/pipeline.py` – Trigger the chunking stage immediately after parsing.

### ⚙️ Chunker Implementation (`/backend/rag/chunker.py`)
```python
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter, CodeSplitter, SentenceWindowNodeParser, SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

def get_splitter_for_type(doc_type: str):
    """Returns the appropriate LlamaIndex splitter based on document type."""
    if doc_type == "paragraph":
        # Uses OpenAIEmbedding for semantic boundaries
        return SemanticSplitterNodeParser(
            buffer_size=1, 
            breakpoint_percentile_threshold=95, 
            embed_model=OpenAIEmbedding()
        )
    elif doc_type == "code":
        return CodeSplitter.from_language(language="python", chunk_lines=40)
    elif doc_type == "transcript":
        return SentenceWindowNodeParser.from_defaults(
            window_size=3,
            window_metadata_key="window",
            original_text_metadata_key="original_text"
        )
    else:
        return SentenceSplitter(chunk_size=600, chunk_overlap=100)

def chunk_document(text: str, filename: str, doc_type: str) -> list:
    """Wraps text in a LlamaIndex Document and splits it into nodes."""
    doc = Document(
        text=text,
        metadata={"filename": filename, "doc_type": doc_type}
    )
    splitter = get_splitter_for_type(doc_type)
    nodes = splitter.get_nodes_from_documents([doc])
    
    return [
        {
            "id": node.node_id,
            "text": node.get_content(),
            "metadata": node.metadata
        }
        for node in nodes
    ]
```

---

## 3. Verification & Testing Plan
- [ ] Upload a test markdown file or clinical text.
- [ ] Verify that the pipeline outputs LlamaIndex chunk count and first chunk previews.
- [ ] Verify that the backend runs cleanly without crashes.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
