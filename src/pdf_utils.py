import fitz  # pymupdf
from pathlib import Path
from typing import List
from .config import CHUNK_SIZE

def pdf_to_text(p: Path) -> str:
    """Extract raw text from a PDF."""
    doc = fitz.open(p)
    return "\n".join(page.get_text() for page in doc)


def split_chunks(txt: str, size: int = CHUNK_SIZE) -> List[str]:
    """Simple whitespace splitter – good enough for English docs."""
    words = txt.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]
