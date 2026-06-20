import os
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import TextNode

CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# Globally configure LlamaIndex to use OpenAI text-embedding-3-small with 768 dimensions
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    dimensions=768,
)


def get_chroma_client():
    """Returns an HTTP client connected to the ChromaDB server container."""
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def add_chunks_to_vector_store(chunks: list, filename: str) -> None:
    """Converts chunk dicts to TextNodes and indexes them in ChromaDB."""
    db_client = get_chroma_client()
    chroma_collection = db_client.get_or_create_collection("onco_agent")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    nodes = []
    for c in chunks:
        nodes.append(
            TextNode(text=c["text"], id_=c["id"], metadata=c["metadata"])
        )

    VectorStoreIndex(nodes, storage_context=storage_context)
    print(f"Successfully indexed {len(nodes)} chunks in ChromaDB for {filename}")


def retrieve_from_vector_store(query: str, top_k: int = 3) -> list:
    """Queries ChromaDB and returns matched document chunks."""
    db_client = get_chroma_client()
    chroma_collection = db_client.get_or_create_collection("onco_agent")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)

    results = []
    for i, node in enumerate(nodes):
        snippet = node.node.get_content().strip()
        score = node.score if node.score is not None else 0.0
        results.append({"chunk_index": i + 1, "score": score, "text": snippet})

    return results
