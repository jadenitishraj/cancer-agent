import os
import requests

RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://rag-service:8004")


def retrieve_clinical_guidelines(query: str) -> str:
    """Queries the RAG service for relevant oncology documents."""
    print(f"\n🔍 [RAG Tool] Querying RAG Service for: '{query}'")

    try:
        response = requests.post(
            f"{RAG_SERVICE_URL}/retrieve",
            json={"query": query, "top_k": 3},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"🔍 [RAG Tool] Error contacting RAG service: {e}")
        return "No relevant oncology documents found (service error)."

    results = data.get("results", [])
    if not results:
        print("🔍 [RAG Tool] No matching documents found in database.")
        return "No relevant oncology documents found."

    print(f"🔍 [RAG Tool] Found {len(results)} matches.")
    context_parts = []
    for r in results:
        snippet = r["text"]
        score = r.get("score", 0.0)
        print(f"  -> Match {r['chunk_index']} [Score: {score:.4f}]: {snippet[:100]}...")
        context_parts.append(f"--- Doc Chunk {r['chunk_index']} ---\n{snippet}")

    return "\n\n".join(context_parts)
