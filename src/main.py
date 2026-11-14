"""~/AbyssAI/src/main.py — native window. Vault + inlined seal. Unwelcome on open."""
from __future__ import annotations
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import webview
from src.api_client import check_ollama_health, query_ollama
from src.config import PDF_ROOT
from src.index import load_prebuilt_index, process_pdfs, search
from src.prompt import unwelcome as pick_unwelcome

SEAL = """
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="100" cy="100" r="92" fill="none" stroke="#c45c4a" stroke-width="1.2" opacity="0.55"/>
  <circle cx="100" cy="100" r="84" fill="none" stroke="#c45c4a" stroke-width="0.6" opacity="0.35"/>
  <circle cx="100" cy="100" r="38" fill="none" stroke="#c45c4a" stroke-width="0.8" opacity="0.45"/>
  <circle cx="100" cy="100" r="6" fill="#c45c4a" opacity="0.7"/>
  <path d="M 100.0 28.0 L 131.2 164.9 L 43.7 55.1 L 170.2 116.0 L 29.8 116.0 L 156.3 55.1 L 68.8 164.9 L 100.0 28.0"
        fill="none" stroke="#c45c4a" stroke-width="1.1" opacity="0.8"/>
  <g stroke="#c45c4a" opacity="0.45">
    <line x1="176" y1="100" x2="190" y2="100" stroke-width="1.2"/>
    <line x1="177.3" y1="120.7" x2="186.9" y2="123.3" stroke-width="0.6"/>
    <line x1="169.3" y1="140" x2="177.9" y2="145" stroke-width="0.6"/>
    <line x1="153.7" y1="153.7" x2="163.6" y2="163.6" stroke-width="1.2"/>
    <line x1="140" y1="169.3" x2="145" y2="177.9" stroke-width="0.6"/>
    <line x1="120.7" y1="177.3" x2="123.3" y2="186.9" stroke-width="0.6"/>
    <line x1="100" y1="176" x2="100" y2="190" stroke-width="1.2"/>
    <line x1="79.3" y1="177.3" x2="76.7" y2="186.9" stroke-width="0.6"/>
    <line x1="60" y1="169.3" x2="55" y2="177.9" stroke-width="0.6"/>
    <line x1="46.3" y1="153.7" x2="36.4" y2="163.6" stroke-width="1.2"/>
    <line x1="30.7" y1="140" x2="22.1" y2="145" stroke-width="0.6"/>
    <line x1="22.7" y1="120.7" x2="13.1" y2="123.3" stroke-width="0.6"/>
    <line x1="24" y1="100" x2="10" y2="100" stroke-width="1.2"/>
    <line x1="22.7" y1="79.3" x2="13.1" y2="76.7" stroke-width="0.6"/>
    <line x1="30.7" y1="60" x2="22.1" y2="55" stroke-width="0.6"/>
    <line x1="46.3" y1="46.3" x2="36.4" y2="36.4" stroke-width="1.2"/>
    <line x1="60" y1="30.7" x2="55" y2="22.1" stroke-width="0.6"/>
    <line x1="79.3" y1="22.7" x2="76.7" y2="13.1" stroke-width="0.6"/>
    <line x1="100" y1="24" x2="100" y2="10" stroke-width="1.2"/>
    <line x1="120.7" y1="22.7" x2="123.3" y2="13.1" stroke-width="0.6"/>
    <line x1="140" y1="30.7" x2="145" y2="22.1" stroke-width="0.6"/>
    <line x1="153.7" y1="46.3" x2="163.6" y2="36.4" stroke-width="1.2"/>
    <line x1="169.3" y1="60" x2="177.9" y2="55" stroke-width="0.6"/>
    <line x1="177.3" y1="79.3" x2="186.9" y2="76.7" stroke-width="0.6"/>
  </g>
</svg>
"""

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>AbyssAI</title>
<style>
  :root {
    --bg: #09070a; --surface: #141216; --surface-2: #1c191e;
    --fg: #ece8e4; --muted: #9a908c; --subtle: #6e6764;
    --accent: #c45c4a; --accent-fg: #1a0c0a;
    --border: rgba(236,232,228,.10);
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; background: var(--bg); color: var(--fg);
    font-family: Figtree, ui-sans-serif, system-ui, sans-serif; }
  body { display: flex; flex-direction: column; position: relative; }
  .vault, .veil, .grain { position: fixed; inset: 0; pointer-events: none; }
  .vault { z-index: 0; background: var(--bg) url("__VAULT__") center / cover no-repeat; }
  .veil { z-index: 1; background:
      linear-gradient(180deg, rgb(9 7 10 / 0.55) 0%, rgb(9 7 10 / 0.78) 42%, rgb(9 7 10 / 0.94) 100%),
      radial-gradient(ellipse at 50% 18%, rgb(196 92 74 / 0.12), transparent 55%); }
  .grain { z-index: 2;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E");
    opacity: 0.045; mix-blend-mode: overlay; }
  .seal-bg { position: fixed; z-index: 2; left: 50%; top: 46%; width: min(36vw, 280px); height: min(36vw, 280px);
    transform: translate(-50%, -50%); opacity: 0.22; pointer-events: none;
    animation: seal-turn 120s linear infinite; }
  .seal-bg svg, .logo svg { width: 100%; height: 100%; display: block; }
  @keyframes seal-turn { to { transform: translate(-50%, -50%) rotate(360deg); } }
  header, main { position: relative; z-index: 3; }
  header { display: flex; align-items: center; gap: 12px; padding: 14px 20px; }
  .logo { width: 40px; height: 40px; flex-shrink: 0; }
  h1 { font-family: "Cormorant Garamond", Georgia, serif; font-size: 26px; font-weight: 500;
    margin: 0; letter-spacing: -0.03em; }
  .kicker { font-size: 11px; letter-spacing: .22em; text-transform: uppercase; color: var(--muted); margin-top: 4px; }
  .stats { margin-left: auto; font-family: ui-monospace, monospace; font-size: 12px; color: var(--subtle); }
  main { flex: 1; display: grid; grid-template-columns: 280px 1fr; gap: 24px; min-height: 0; padding: 0 20px 16px; }
  aside { background: rgba(20,18,22,.8); border: 1px solid var(--border); border-radius: 16px; padding: 20px; overflow: auto; }
  aside h2 { font-family: "Cormorant Garamond", Georgia, serif; font-weight: 500; margin: 0 0 12px; }
  aside p { color: var(--muted); font-size: 13px; line-height: 1.5; }
  button { cursor: pointer; border: 0; border-radius: 8px; height: 40px; padding: 0 14px; font-weight: 500; }
  .primary { background: var(--accent); color: var(--accent-fg); width: 100%; }
  .thread { overflow: auto; display: flex; flex-direction: column; gap: 16px; padding: 8px 4px 16px; }
  .student { align-self: flex-end; max-width: 36rem; background: var(--surface-2);
    border: 1px solid var(--border); border-radius: 12px 12px 4px 12px; padding: 12px 16px; font-size: 14px; }
  .prof { align-self: flex-start; max-width: 40rem; background: rgba(20,18,22,.85);
    border: 1px solid var(--border); border-radius: 12px 4px 12px 12px; padding: 16px; font-size: 14px; line-height: 1.55; }
  .prof .who { font-size: 11px; letter-spacing: .2em; text-transform: uppercase; color: var(--accent); margin: 0 0 8px; }
  .composer { display: flex; gap: 8px; background: rgba(20,18,22,.9); border: 1px solid var(--border);
    border-radius: 12px; padding: 8px; }
  textarea { flex: 1; background: transparent; border: 0; color: var(--fg); resize: none; min-height: 44px;
    font: inherit; outline: none; }
  .send { background: var(--accent); color: var(--accent-fg); width: 44px; height: 44px; border-radius: 8px; }
  .desk { display: flex; flex-direction: column; min-width: 0; }
  .hint { text-align: center; font-size: 11px; color: var(--subtle); margin-top: 8px; }
  @media (max-width: 720px) { main { grid-template-columns: 1fr; } }
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Figtree:wght@400;500;600&display=swap"/>
</head>
<body>
  <div class="vault"></div>
  <div class="veil"></div>
  <div class="grain"></div>
  <div class="seal-bg">__SEAL__</div>
  <header>
    <div class="logo">__SEAL__</div>
    <div>
      <h1>Professor Apollyon</h1>
      <div class="kicker">Whispers from the void</div>
    </div>
    <div class="stats" id="stats">no library yet</div>
  </header>
  <main>
    <aside>
      <h2>The library</h2>
      <p>Process private PDFs. Native window — not Streamlit. Lecturer is local Dolphin 3B.</p>
      <p id="pdfroot" style="font-family: ui-monospace, monospace; font-size: 11px; color: var(--subtle);"></p>
      <button class="primary" id="process">Process library</button>
      <p id="status" style="margin-top:14px;font-size:12px;color:var(--muted)"></p>
    </aside>
    <div class="desk">
      <div class="thread" id="thread"></div>
      <form class="composer" id="form">
        <textarea id="q" placeholder="Whisper into the void" rows="1"></textarea>
        <button class="send" type="submit" title="Summon Apollyon">→</button>
      </form>
      <p class="hint">Ask the professor about the Inner Temple, the shadow, or the self. Feed your own PDFs when you want the brief enlarged.</p>
    </div>
  </main>
<script>
  const thread = document.getElementById('thread');
  const stats = document.getElementById('stats');
  const status = document.getElementById('status');
  function esc(s) {
    return String(s)
      .replace(/&/g, '&' + 'amp;')
      .replace(/</g, '&' + 'lt;')
      .replace(/\n/g, '<' + 'br>');
  }
  function add(role, text) {
    const el = document.createElement('div');
    el.className = role === 'student' ? 'student' : 'prof';
    el.innerHTML = role === 'professor'
      ? '<p class="who">Apollyon</p>' + esc(text)
      : esc(text);
    thread.appendChild(el);
    thread.scrollTop = thread.scrollHeight;
  }
  async function refresh() {
    const s = await window.pywebview.api.stats();
    stats.textContent = s.label;
    document.getElementById('pdfroot').textContent = s.pdf_root;
  }
  document.getElementById('process').onclick = async () => {
    status.textContent = 'Indexing…';
    try {
      status.textContent = await window.pywebview.api.process();
      await refresh();
    } catch (e) {
      status.textContent = String(e);
    }
  };
  document.getElementById('form').onsubmit = async (e) => {
    e.preventDefault();
    const q = document.getElementById('q');
    const text = q.value.trim();
    if (!text) return;
    q.value = '';
    add('student', text);
    add('professor', 'The professor is turning a page.');
    const last = thread.lastChild;
    try {
      const reply = await window.pywebview.api.consult(text);
      last.innerHTML = '<p class="who">Apollyon</p>' + esc(reply);
    } catch (err) {
      last.innerHTML = '<p class="who">Apollyon</p>' + esc(String(err));
    }
  };
  window.addEventListener('pywebviewready', async () => {
    await refresh();
    add('professor', await window.pywebview.api.unwelcome());
  });
</script>
</body></html>
"""


class Bridge:
    def __init__(self) -> None:
        self.meta, _ = load_prebuilt_index()
        self.history: list[dict] = []
        self.live = check_ollama_health()

    def stats(self) -> dict:
        n = len(self.meta)
        sources = {m.get("pdf_name") for m in self.meta}
        mode = "Dolphin 3B" if self.live else "library only"
        return {
            "label": f"{len(sources)} folios · {n} passages · {mode}",
            "pdf_root": str(PDF_ROOT),
        }

    def unwelcome(self) -> str:
        return pick_unwelcome()

    def process(self) -> str:
        self.meta = process_pdfs()
        return f"Indexed {len(self.meta)} passages."

    def consult(self, query: str) -> str:
        query = (query or "").strip()
        if not query:
            return "Ask something."
        hits = search(self.meta, query, k=5)
        if self.live:
            try:
                reply = query_ollama(query, hits, self.history)
            except Exception as exc:
                reply = _library_only(query, hits) + f"\n\n(Dolphin failed: {exc})"
        else:
            reply = _library_only(query, hits)
        self.history.append({"role": "user", "content": query})
        self.history.append({"role": "assistant", "content": reply})
        return reply


def _library_only(query: str, hits: list[dict]) -> str:
    if not hits:
        return (
            "Dolphin is not answering, and the shelves are silent. "
            "ollama pull nchapman/dolphin3.0-llama3:3b — then Process library."
        )
    body = "\n\n".join(
        f"{i}. {h.get('pdf_name')}\n{h.get('text')}" for i, h in enumerate(hits[:4], 1)
    )
    return (
        "Dolphin is sealed. The private library, at its word.\n\n"
        f"You asked: {query}\n\n{body}"
    )


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    vault_path = root / "gui" / "public" / "vault.jpg"
    icon_path = root / "gui" / "public" / "TG_Group_PFP.png"

    if vault_path.is_file():
        vault = "data:image/jpeg;base64," + base64.b64encode(vault_path.read_bytes()).decode("ascii")
    else:
        vault = ""

    html = HTML.replace("__VAULT__", vault).replace("__SEAL__", SEAL)
    api = Bridge()

    webview.create_window(
        "AbyssAI — Whispers From The Void",
        html=html,
        js_api=api,
        width=1180,
        height=760,
        min_size=(720, 560),
        background_color="#09070a",
    )

    # Icon: GTK / QT / macOS / Windows via start()
    # Path relative to repo root; falls back silently if missing
    icon = str(icon_path) if icon_path.is_file() else None
    webview.start(icon=icon)


if __name__ == "__main__":
    main()
