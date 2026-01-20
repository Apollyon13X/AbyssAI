python
import fitz  # PyMuPDF
from pathlib import Path
from typing import List
import re
from .config import CHUNK_SIZE

def pdf_to_text(p: Path) -> str:
    """Extract raw text from a PDF using PyMuPDF."""
    try:
        doc = fitz.open(p)
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        print(f"Error reading PDF {p}: {e}")
        return ""

def split_chunks(txt: str, size: int = CHUNK_SIZE) -> List[str]:
    """Split text into overlapping chunks for better context retention."""
    if not txt.strip():
        return []
    
    words = txt.split()
    chunks = []
    stride = size // 2  # 50% overlap
    
    for i in range(0, len(words), stride):
        chunk = " ".join(words[i:i + size])
        if chunk:
            chunks.append(chunk)
    
    return chunks

