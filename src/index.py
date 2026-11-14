"""~/AbyssAI/src/index.py — BM25 over private PDFs. No FAISS."""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from typing import Dict, List, Tuple

from src.config import INDEX_PATH, PDF_ROOT, ABYSS_ROOT
from src.pdf_utils import pdf_to_text, split_chunks

STOP = {
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to", "for",
    "of", "as", "is", "it", "by", "be", "are", "was", "were", "with", "from",
    "this", "that", "these", "those", "you", "your", "we", "our", "they",
}
TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> List[str]:
    return [t for t in TOKEN.findall(text.lower()) if len(t) > 1 and t not in STOP]


def load_prebuilt_index() -> Tuple[List[dict], None]:
    if INDEX_PATH.exists():
        try:
            meta = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            print(f"Loaded existing index with {len(meta)} chunks")
            return meta, None
        except Exception as exc:
            print(f"Failed to load existing index: {exc}")
    return [], None


def process_pdfs() -> List[dict]:
    if not PDF_ROOT.exists():
        raise RuntimeError(f"PDF directory {PDF_ROOT} does not exist.")
    pdf_files = list(PDF_ROOT.rglob("*.pdf"))
    if not pdf_files:
        raise RuntimeError(f"No PDFs found in {PDF_ROOT}.")
    meta: List[dict] = []
    for pdf_path in pdf_files:
        print(f"Processing {pdf_path.name}...")
        raw = pdf_to_text(pdf_path)
        if not raw.strip():
            continue
        try:
            rel = str(pdf_path.relative_to(ABYSS_ROOT))
        except ValueError:
            rel = pdf_path.name
        for i, chunk in enumerate(split_chunks(raw)):
            meta.append({
                "source": rel,
                "chunk_id": i,
                "pdf_name": pdf_path.name,
                "text": chunk,
            })
    if not meta:
        raise RuntimeError("No readable content found.")
    INDEX_PATH.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    print(f"Index built: {len(meta)} chunks from {len(pdf_files)} PDFs")
    return meta


def search(meta: List[dict], query: str, k: int = 5) -> List[dict]:
    if not meta:
        return []
    q = tokenize(query)
    if not q:
        return []
    docs = [tokenize(m.get("text") or "") for m in meta]
    df: Dict[str, int] = {}
    for tokens in docs:
        for t in set(tokens):
            df[t] = df.get(t, 0) + 1
    n = len(docs)
    avg = sum(len(d) for d in docs) / n
    k1, b = 1.5, 0.75
    scored: List[Tuple[float, dict]] = []
    qset = set(q)
    for tokens, row in zip(docs, meta):
        tf = Counter(tokens)
        length = len(tokens) or 1
        score = 0.0
        for term in qset:
            f = tf.get(term, 0)
            if not f:
                continue
            idf = math.log(1 + (n - df.get(term, 0) + 0.5) / (df.get(term, 0) + 0.5))
            score += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * (length / avg)))
        if score > 0:
            scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [row for _, row in scored[:k]]
