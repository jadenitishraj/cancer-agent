import fitz  # PyMuPDF

from parser import classify_text


def parse_pdf(file_path: str) -> str:
    """Extracts text from a PDF file page by page using PyMuPDF."""
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)


def parse_txt(file_path: str) -> str:
    """Extracts text from a plain text or markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def parse_file(file_path: str) -> tuple[str, str]:
    """Parses a file based on its extension and returns (text, type)."""
    ext = file_path.lower().split(".")[-1]
    if ext == "pdf":
        text = parse_pdf(file_path)
    elif ext in ("txt", "md"):
        text = parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return text, classify_text(text)
