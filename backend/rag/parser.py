import fitz  # PyMuPDF

def classify_text(text: str) -> str:
    """Classifies text type based on basic heuristics."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return "paragraph"
    
    # 1. Code detection
    keywords = {"def ", "import ", "class ", "const ", "let ", "function "}
    code_matches = sum(1 for l in lines if any(l.startswith(k) for k in keywords))
    if code_matches > 0.05 * len(lines):
        return "code"
        
    # 2. Table detection (delimiters or high numeric ratio)
    pipes_tabs = sum(1 for l in lines if l.count("|") >= 2 or l.count("\t") >= 2)
    words = text.split()
    nums = sum(1 for w in words if w.replace(".", "").replace(",", "").isdigit())
    is_numeric = (nums / len(words) > 0.25) if words else False
    if pipes_tabs > 0.1 * len(lines) or is_numeric:
        return "table_heavy"
        
    # 3. Transcript detection (short speaker prefix followed by colon)
    speakers = sum(1 for l in lines[:30] if ":" in l and len(l.split(":")[0]) < 15 and not l.split(":")[0].startswith("http"))
    if speakers > 0.2 * min(len(lines), 30):
        return "transcript"
        
    return "paragraph"

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
