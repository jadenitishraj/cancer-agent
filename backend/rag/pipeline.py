import os
from rag.parser import parse_file

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "files")

def run_parsing_pipeline(filename: str) -> dict:
    """Parses a specific file from the upload directory and returns character count info."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}
        
    try:
        extracted_text, doc_type = parse_file(file_path)
        char_count = len(extracted_text)
        print(f"Successfully parsed {filename} ({char_count} chars, type: {doc_type})")
        return {
            "status": "parsed",
            "filename": filename,
            "char_count": char_count,
            "doc_type": doc_type
        }
    except Exception as e:
        print(f"Error parsing {filename}: {str(e)}")
        return {
            "status": "error",
            "filename": filename,
            "message": str(e)
        }
