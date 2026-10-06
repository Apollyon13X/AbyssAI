"""~/AbyssAI/src/api_client.py — Ollama chat to Dolphin 3B."""
from __future__ import annotations

from typing import Iterator, List

import requests

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT
from src.prompt import SYSTEM, build_user_prompt


def check_ollama_health() -> bool:
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=4)
        resp.raise_for_status()
        names = [m.get("name", "") for m in resp.json().get("models", [])]
        if not any(OLLAMA_MODEL in n or n.startswith(OLLAMA_MODEL.split(":")[0]) for n in names):
            print(f"Ollama is up, but {OLLAMA_MODEL} is not pulled yet.")
            print(f"  ollama pull {OLLAMA_MODEL}")
            return False
        print(f"Ollama ready ({OLLAMA_MODEL})")
        return True
    except Exception as exc:
        print(f"Cannot reach Ollama at {OLLAMA_BASE_URL}: {exc}")
        print("  On Void: ollama serve")
        return False


def _messages(query: str, contexts: List[dict], history: List[dict] | None) -> list:
    messages = [{"role": "system", "content": SYSTEM}]
    for turn in (history or [])[-8:]:
        messages.append(turn)
    messages.append({"role": "user", "content": build_user_prompt(query, contexts)})
    return messages


def query_ollama(query: str, contexts: List[dict], history: List[dict] | None = None) -> str:
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": _messages(query, contexts, history),
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 900},
        },
        timeout=OLLAMA_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def stream_ollama(query: str, contexts: List[dict], history: List[dict] | None = None) -> Iterator[str]:
    import json

    with requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": _messages(query, contexts, history),
            "stream": True,
            "options": {"temperature": 0.7, "num_predict": 900},
        },
        timeout=OLLAMA_TIMEOUT,
        stream=True,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            try:
                token = json.loads(line)["message"].get("content") or ""
            except Exception:
                continue
            if token:
                yield token
