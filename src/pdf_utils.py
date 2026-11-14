"""~/AbyssAI/src/pdf_utils.py — extract PDF text, overlapping chunks."""
from pathlib import Path
from typing import List

from src.config import CHUNK_SIZE, CHUNK_STRIDE


def pdf_to_text(path: Path) -> str:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("pip install pymupdf") from exc
    try:
        doc = fitz.open(path)
        pages = []
        for page in doc:
            text = " ".join((page.get_text("text") or "").split())
            if text:
                pages.append(text)
        return "\n\n".join(pages)
    except Exception as exc:
        print(f"Error reading PDF {path}: {exc}")
        return ""


def split_chunks(txt: str, size: int = CHUNK_SIZE, stride: int = CHUNK_STRIDE) -> List[str]:
    words = txt.split()
    if not words:
        return []
    if len(words) <= size:
        return [" ".join(words)]
    chunks: List[str] = []
    i = 0
    while i < len(words):
        slice_ = words[i : i + size]
        if len(slice_) < 24 and chunks:
            chunks[-1] = chunks[-1] + " " + " ".join(slice_)
            break
        chunks.append(" ".join(slice_))
        if i + size >= len(words):
            break
        i += stride
    return chunks
