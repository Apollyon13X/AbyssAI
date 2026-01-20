python
import requests
import json
from typing import Dict, Any
from .config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

def query_ollama(prompt: str, timeout: int = None) -> str:
    """
    Send prompt to local Ollama instance.
    Returns the generated response text.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        resp = requests.post(
            url, 
            json=payload, 
            timeout=timeout or OLLAMA_TIMEOUT
        )
        resp.raise_for_status()
        
        result = resp.json()
        return result.get("response", "No response received from Ollama")
    
    except requests.exceptions.ConnectionError:
        return f"❌ Error: Cannot connect to Ollama at {OLLAMA_BASE_URL}. Is Ollama running? (ollama serve)"
    except requests.exceptions.Timeout:
        return "❌ Error: Ollama request timed out. Try a smaller model or increase timeout."
    except Exception as e:
        return f"❌ Error querying Ollama: {str(e)}"

def check_ollama_health() -> bool:
    """Check if Ollama is accessible and the configured model is available."""
    try:
        url = f"{OLLAMA_BASE_URL}/api/tags"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        
        models = resp.json().get("models", [])
        available = [m["name"] for m in models]
        
        if OLLAMA_MODEL in available:
            print(f"✅ Ollama ready with model: {OLLAMA_MODEL}")
            return True
        else:
            print(f"❌ Model '{OLLAMA_MODEL}' not found. Available models: {available}")
            print(f"Pull the model with: ollama pull {OLLAMA_MODEL}")
            return False
    
    except Exception as e:
        print(f"❌ Cannot reach Ollama: {e}")
        print("Start Ollama first: ollama serve")
        return False

