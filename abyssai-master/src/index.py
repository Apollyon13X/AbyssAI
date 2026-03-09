import json
from pathlib import Path
from typing import List, Tuple, Optional
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import PDF_ROOT, INDEX_PATH, META_PATH, EMBED_MODEL, CHUNK_SIZE, ABYSS_ROOT
from src.pdf_utils import pdf_to_text, split_chunks

def embed_chunks(chunks: List[str], model: SentenceTransformer) -> np.ndarray:
    if not chunks:
        dim = model.get_sentence_embedding_dimension()
        return np.empty((0, dim), dtype=np.float32)
    return model.encode(chunks, normalize_embeddings=True, show_progress_bar=True).astype(np.float32)

def build_faiss_index(emb: np.ndarray) -> faiss.IndexFlatIP:
    if emb.size == 0:
        raise ValueError("No embeddings generated.")
    dim = emb.shape[1]
    idx = faiss.IndexFlatIP(dim)
    idx.add(emb)
    return idx

def load_prebuilt_index() -> Tuple[Optional[faiss.IndexFlatIP], List[dict]]:
    if INDEX_PATH.exists() and META_PATH.exists():
        try:
            index = faiss.read_index(str(INDEX_PATH))
            meta = json.loads(META_PATH.read_text(encoding='utf-8'))
            print(f"Loaded existing index with {len(meta)} chunks")
            return index, meta
        except Exception as e:
            print(f"Failed to load existing index: {e}")
    return None, []

def process_pdfs() -> Tuple[faiss.IndexFlatIP, List[dict]]:
    if not PDF_ROOT.exists():
        raise RuntimeError(f"PDF directory {PDF_ROOT} does not exist.")
    
    all_chunks, meta = [], []
    pdf_files = list(PDF_ROOT.rglob("*.pdf"))
    if not pdf_files:
        raise RuntimeError(f"No PDFs found in {PDF_ROOT}.")
    
    print(f"Found {len(pdf_files)} PDF(s) to process...")
    for pdf_path in pdf_files:
        print(f"Processing {pdf_path.name}...")
        raw = pdf_to_text(pdf_path)
        if not raw.strip():
            continue
        chunks = split_chunks(raw)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            meta.append({
                "source": str(pdf_path.relative_to(ABYSS_ROOT)),
                "chunk_id": i,
                "pdf_name": pdf_path.name
            })
    
    if not all_chunks:
        raise RuntimeError("No readable content found.")
    
    print(f"Generating embeddings for {len(all_chunks)} chunks...")
    embedder = SentenceTransformer(EMBED_MODEL)
    embeddings = embed_chunks(all_chunks, embedder)
    
    print("Building FAISS index...")
    index = build_faiss_index(embeddings)
    
    faiss.write_index(index, str(INDEX_PATH))
    META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"✅ Index built! {len(meta)} chunks from {len(pdf_files)} PDFs")
    return index, meta
