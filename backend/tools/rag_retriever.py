import os
import chromadb
from langchain_core.tools import tool
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "chroma_db")

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    dimensions=768
)

@tool
def retrieve_clinical_guidelines(query: str) -> str:
    """Retrieves relevant cancer reference materials, clinical trials, and oncology guidelines from the local vector database."""
    print(f"\n🔍 [RAG Tool] Querying ChromaDB for: '{query}'")
    
    db_client = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db_client.get_or_create_collection("onco_agent")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)
    
    retriever = index.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(query)
    
    if not nodes:
        print("🔍 [RAG Tool] No matching documents found in database.")
        return "No relevant oncology documents found."
        
    print(f"🔍 [RAG Tool] Found {len(nodes)} matches. Retrieving contents:")
    context_parts = []
    for i, node in enumerate(nodes):
        snippet = node.node.get_content().strip()
        score = node.score if node.score is not None else 0.0
        print(f"  -> Match {i+1} [Score: {score:.4f}]: {snippet[:100]}...")
        context_parts.append(f"--- Doc Chunk {i+1} ---\n{snippet}")
        
    return "\n\n".join(context_parts)
