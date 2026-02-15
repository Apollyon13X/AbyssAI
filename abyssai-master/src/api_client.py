import requests
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

def query_ollama(prompt: str, timeout: int = None) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.7, "top_p": 0.9}}
    try:
        resp = requests.post(url, json=payload, timeout=timeout or OLLAMA_TIMEOUT)
        resp.raise_for_status()
        return resp.json().get("response", "No response")
    except requests.exceptions.ConnectionError:
        return f"❌ Cannot connect to Ollama at {OLLAMA_BASE_URL}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def check_ollama_health() -> bool:
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
        if OLLAMA_MODEL in models:
            print(f"✅ Ollama ready with {OLLAMA_MODEL}")
            return True
        else:
            print(f"❌ Model {OLLAMA_MODEL} not found. Available: {models}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach Ollama: {e}")
        return False
