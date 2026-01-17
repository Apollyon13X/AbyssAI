from pathlib import Path

# ── Paths ───────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
PDF_ROOT   = BASE_DIR / "abyss_feed"          # mount point for PDFs
INDEX_PATH = BASE_DIR / "abyss_index.faiss"
META_PATH  = BASE_DIR / "abyss_meta.json"

# ── Model identifiers ───────────────────────────────────────────
EMBED_MODEL   = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE    = 500                         # ~tokens per chunk

# ── Morpheus endpoint ────────────────────────────────────────
# Replace with your actual gateway URL; keep the key out of source control.
MORPHEUS_URL = "https://api.mor.org/v1/query"
MORPHEUS_KEY = ""   # ← set via env var MORPHEUS_API_KEY at runtime
