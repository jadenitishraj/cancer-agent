import fitz  # PyMuPDF


def classify_text(text: str) -> str:
    """Classifies text type based on basic heuristics."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return "paragraph"

    keywords = {"def ", "import ", "class ", "const ", "let ", "function "}
    code_matches = sum(1 for l in lines if any(l.startswith(k) for k in keywords))
    if code_matches > 0.05 * len(lines):
        return "code"

    pipes_tabs = sum(1 for l in lines if l.count("|") >= 2 or l.count("\t") >= 2)
    words = text.split()
    nums = sum(1 for w in words if w.replace(".", "").replace(",", "").isdigit())
    is_numeric = (nums / len(words) > 0.25) if words else False
    if pipes_tabs > 0.1 * len(lines) or is_numeric:
        return "table_heavy"

    speakers = sum(
        1
        for l in lines[:30]
        if ":" in l and len(l.split(":")[0]) < 15 and not l.split(":")[0].startswith("http")
    )
    if speakers > 0.2 * min(len(lines), 30):
        return "transcript"

    return "paragraph"
