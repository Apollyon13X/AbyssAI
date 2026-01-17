import os
import requests
from .config import MORPHEUS_URL, MORPHEUS_KEY

def query_morpheus(prompt: str, timeout: int = 30) -> str:
    """Send the assembled prompt to the Morpheus inference gateway."""
    headers = {"Authorization": f"Bearer {MORPHEUS_KEY}"}
    payload = {"question": prompt}
    resp = requests.post(MORPHEUS_URL, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    # Expected: {"answer": "..."} – fall back to raw text if the key is missing
    return resp.json().get("answer") or resp.text
