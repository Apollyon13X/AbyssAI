from pathlib import Path
import os

# ── Paths ───────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ABYSS_ROOT = BASE_DIR.parent
PDF_ROOT = ABYSS_ROOT / "abyss_lessons"

INDEX_PATH = BASE_DIR / "abyss_index.faiss"
META_PATH  = BASE_DIR / "abyss_meta.json"

# ── Model identifiers ───────────────────────────────────────────
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500

# ── Ollama configuration ────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "llama2-uncensored:7b")
OLLAMA_TIMEOUT  = 300          # ← changed from 120 to 300 seconds (5 minutes)
