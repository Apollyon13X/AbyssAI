import json
from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .config import PDF_ROOT, INDEX_PATH, META_PATH, EMBED_MODEL, CHUNK_SIZE
from .pdf_utils import pdf_to_text, split_chunks


def embed_chunks(chunks: List[str], model: SentenceTransformer) -> np.ndarray:
    if not chunks:
        return np.empty((0, model.get_sentence_embedding_dimension()), dtype=np.float32)
    return model.encode(chunks, normalize_embeddings=True).astype(np.float32)


def build_faiss_index(emb: np.ndarray) -> faiss.IndexFlatIP:
    if emb.size == 0:
        raise ValueError("No embeddings – you must feed PDFs first.")
    dim = emb.shape[1]
    idx = faiss.IndexFlatIP(dim)      # inner‑product ≈ cosine similarity
    idx.add(emb)
    return idx


def load_prebuilt_index() -> Tuple[faiss.IndexFlatIP | None, List[dict]]:
    """Return existing FAISS index + metadata, or (None, [])."""
    if INDEX_PATH.exists() and META_PATH.exists():
        index = faiss.read_index(str(INDEX_PATH))
        meta = json.loads(META_PATH.read_text())
        return index, meta
    return None, []


def process_pdfs() -> Tuple[faiss.IndexFlatIP, List[dict]]:
    """Walk PDF_ROOT, extract, chunk, embed, persist."""
    all_chunks, meta = [], []

    for pdf_path in PDF_ROOT.rglob("*.pdf"):
        raw = pdf_to_text(pdf_path)
        if not raw.strip():
            continue
        for i, chunk in enumerate(split_chunks(raw)):
            all_chunks.append(chunk)
            meta.append({"source": str(pdf_path), "chunk_id": i})

    if not all_chunks:
        raise RuntimeError("No readable PDFs found in abyss_feed/")

    embedder = SentenceTransformer(EMBED_MODEL)
    embeddings = embed_chunks(all_chunks, embedder)

    index = build_faiss_index(embeddings)

    # Persist for future runs
    faiss.write_index(index, str(INDEX_PATH))
    META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    return index, meta
