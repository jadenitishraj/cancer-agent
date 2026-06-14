import os
from rag.parser import parse_file
from rag.chunker import chunk_document
from rag.vector_store import add_chunks_to_vector_store

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "files")

def run_parsing_pipeline(filename: str) -> dict:
    """Parses and chunks a specific file from the upload directory."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}
        
    try:
        extracted_text, doc_type = parse_file(file_path)
        char_count = len(extracted_text)
        
        # Chunk document using LlamaIndex splitters
        chunks = chunk_document(extracted_text, filename, doc_type)
        
        print(f"Successfully processed {filename} ({char_count} chars, type: {doc_type}) -> {len(chunks)} nodes")
        print("--- CHUNKS START ---")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}/{len(chunks)} (ID: {chunk['id']}):")
            print(f"Text Preview: {chunk['text'].strip()[:150]}...")
            print(f"Metadata: {chunk['metadata']}")
            print("-" * 20)
        print("--- CHUNKS END ---")
        
        # Save chunks into ChromaDB using OpenAI embeddings
        add_chunks_to_vector_store(chunks, filename)
        
        return {
            "status": "parsed",
            "filename": filename,
            "char_count": char_count,
            "doc_type": doc_type,
            "chunk_count": len(chunks),
            "chunks": chunks[:3]  # Return preview of the first 3 chunks
        }
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        return {
            "status": "error",
            "filename": filename,
            "message": str(e)
        }
