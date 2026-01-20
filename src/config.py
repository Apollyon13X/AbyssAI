python
from pathlib import Path
import os

# ── Paths ───────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_ROOT = BASE_DIR / "abyss_feed"
INDEX_PATH = BASE_DIR / "abyss_index.faiss"
META_PATH = BASE_DIR / "abyss_meta.json"

# ── Model identifiers ───────────────────────────────────────────
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500  # ~tokens per chunk

# ── Ollama configuration ────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2-uncensored")  # or "wizard-vicuna-uncensored", "solar", etc.
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))  # seconds

