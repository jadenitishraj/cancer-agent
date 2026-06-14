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
    print(f"Successfully indexed {len(nodes)} chunks in ChromaDB for {filename}")
