"""~/AbyssAI/src/config.py — paths + Dolphin 3B (ultra-light uncensored)."""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ABYSS_ROOT = BASE_DIR
PDF_ROOT = Path(os.getenv("ABYSS_PDF_ROOT", BASE_DIR / "data" / "private"))
INDEX_PATH = BASE_DIR / "abyss_index.json"
CHUNK_SIZE = 160
CHUNK_STRIDE = 80
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "nchapman/dolphin3.0-llama3:3b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "777"))
