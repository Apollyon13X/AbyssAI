import fitz  # PyMuPDF
from pathlib import Path
from typing import List
from src.config import CHUNK_SIZE

def pdf_to_text(p: Path) -> str:
    try:
        doc = fitz.open(p)
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        print(f"Error reading PDF {p}: {e}")
        return ""

def split_chunks(txt: str, size: int = CHUNK_SIZE) -> List[str]:
    if not txt.strip():
        return []
    words = txt.split()
    chunks = []
    stride = size // 2
    for i in range(0, len(words), stride):
        chunk = " ".join(words[i:i + size])
        if chunk:
            chunks.append(chunk)
    return chunks
