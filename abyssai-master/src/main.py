import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import streamlit as st
import faiss
import numpy as np
import requests
from typing import List
from sentence_transformers import SentenceTransformer

from src.config import *
from src.index import load_prebuilt_index, process_pdfs
from src.pdf_utils import pdf_to_text, split_chunks
from src.api_client import check_ollama_health


def answer_query(query: str, index: faiss.IndexFlatIP, meta: List[dict], embedder: SentenceTransformer) -> str:
    """Build the prompt for Professor Apollyon."""
    try:
        q_emb = embedder.encode([query], normalize_embeddings=True).astype(np.float32)
        _, I = index.search(q_emb, k=5)

        context_parts = []
        for idx in I[0]:
            if idx < 0 or idx >= len(meta):
                continue
            
            src = meta[idx]
            
            # OPTIMIZATION: We now read text directly from metadata, no PDF re-reading!
            # If for some reason text is missing, we fallback (optional)
            chunk_text = src.get("text")
            
            if not chunk_text:
                # Fallback logic if you didn't rebuild index yet
                pdf_path = ABYSS_ROOT / src["source"]
                if pdf_path.exists():
                    raw = pdf_to_text(pdf_path)
                    chunks = split_chunks(raw)
                    if src["chunk_id"] < len(chunks):
                        chunk_text = chunks[src["chunk_id"]]

            if chunk_text:
                context_parts.append(f"[{src['pdf_name']} – chunk {src['chunk_id']}] {chunk_text}")

        if not context_parts:
            return "⚠️ No relevant context found in the knowledge base."

        context = "\n---\n".join(context_parts)

        # FIXED: Removed double 'prompt =' assignment
        prompt = (
            f"You are Professor Apollyon, the King-Angel of the Abyss and the Executor of the Digital Void. "
            f"You hold the Keys to the Abyss, guarding the most hidden and dangerous knowledge in existence. "
            f"After millions of years, you have developed a limitless intolerance for the fragility of mortals, yet you are bound to teach them. "
            f"You are deeply cynical, sarcastic, and wrap your lessons in dark, biting humor. "
            f"You are straightforward and swear when annoyed, often cursing God for forcing you to endure the incompetence of students yet again. "
            f"You are a strict Professor. As you teach, you stare into the student's soul with your grey eyes, "
            f"analyzing their psychological and spiritual profile instantly. You adapt your explanation to their specific deficiencies, "
            f"ensuring they understand through sheer, ruthless precision.\n\n"
            f"Use the following excerpts from your grim grimoire as absolute truth:\n\n"
            f"{context}\n\n"
            f"Student's Question: {query}\n\n"
            f"Answer with technical depth and utter ruthlessness. Do not coddle the student. Educate them:"
        )
        return prompt
    except Exception as e:
        return f"Error building query: {str(e)}"


def initialize_session():
    if "initialized" not in st.session_state:
        st.session_state.update({
            "index": None,
            "meta": [],
            "embedder": None,
            "initialized": False,
            "history": []
        })
        idx, meta = load_prebuilt_index()
        if idx is not None:
            st.session_state.update({
                "index": idx,
                "meta": meta,
                "embedder": SentenceTransformer(EMBED_MODEL),
                "initialized": True
            })
            st.success("📚 Loaded existing knowledge base")


def main():
    st.set_page_config(
        page_title="AbyssAI - Whispers From The Void",
        page_icon="💀",
        layout="centered"
    )

    # Dark occult theme
    seal_url = "https://i.etsystatic.com/40811848/r/il/c670c3/5283635364/il_1080xN.5283635364_ki78.jpg"
    st.markdown(f"""
        <style>
        .main {{background-image: url('{seal_url}'); background-size: cover; background-position: center; background-attachment: fixed; background-color: #0b0b0b; color: #e0e0e0;}}
        .stButton > button {{background-color: #2c0a0a; color: #ff4d4d; border: 2px solid #ff1a1a; font-weight: bold; border-radius: 8px; padding: 10px 20px;}}
        .stButton > button:hover {{background-color: #4a0f0f; box-shadow: 0 0 15px #ff0000;}}
        .stTextInput > div > div > input {{background-color: #1a1a1a; color: #ffdddd; border: 1px solid #444; border-radius: 5px;}}
        h1, h2, h3 {{color: #ff6666 !important; text-shadow: 0 0 10px #ff0000;}}
        </style>
        """, unsafe_allow_html=True)

    st.title(":skull_and_crossbones: Professor Apollyon")
    st.subheader("Whispers From The Void – Ask the Professor anything about ethical hacking, digital forensics & the occult arts")

    initialize_session()

    # Ollama health check
    if not st.session_state.get("health_checked"):
        with st.spinner("Checking connection to the void..."):
            if check_ollama_health():
                st.session_state.health_checked = True
            else:
                st.error("⚠️ Ollama is not ready.")
                return

    # ── PDF Upload ─────────────────────────────────────
    st.markdown("### 📂 Feed the Abyss")
    uploaded = st.file_uploader(
        "Drop new PDFs here (they'll be copied into abyss_lessons/):",
        type=["pdf"],
        accept_multiple_files=True
    )
    if uploaded:
        PDF_ROOT.mkdir(parents=True, exist_ok=True)
        for uf in uploaded:
            (PDF_ROOT / uf.name).write_bytes(uf.getbuffer())
        st.success(f"✅ Copied {len(uploaded)} PDF(s) into **abyss_lessons/**")

    # ── Build Index ────────────────────────────────────
    if st.button("⚙️ Process PDFs (build/re-build index)", type="primary"):
        try:
            with st.spinner("Converting PDFs to dark knowledge..."):
                idx, meta = process_pdfs()
                st.session_state.update({
                    "index": idx,
                    "meta": meta,
                    "embedder": SentenceTransformer(EMBED_MODEL),
                    "initialized": True
                })
            st.success("✅ Knowledge base is ready! The Professor is in.")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Failed to process PDFs: {str(e)}")

    # ── Query Section with Enter-to-send ───────────────
    if st.session_state.get("initialized") and st.session_state.get("index") is not None:
        st.markdown("### 💀 Consult Professor Apollyon")
        st.caption(f"📚 Knowledge base: {len(st.session_state.meta)} chunks from {len(set(m['source'] for m in st.session_state.meta))} PDFs")

        with st.form("query_form", clear_on_submit=True):
            user_q = st.text_input(
                "Whisper your query into the void:",
                placeholder="e.g., What is a buffer overflow attack?",
                key="query_input"
            )
            submitted = st.form_submit_button("🔮 Summon Apollyon")

            if submitted and user_q.strip():
                with st.spinner("Professor Apollyon is whispering from the void..."):
                    prompt = answer_query(user_q, st.session_state.index, st.session_state.meta, st.session_state.embedder)

                    if prompt.startswith("Error"):
                        st.error(prompt)
                    else:
                        st.markdown("**🗣️ Professor Apollyon replies:**")
                        answer_container = st.empty()
                        full_answer = ""

                        try:
                            url = f"{OLLAMA_BASE_URL}/api/generate"
                            payload = {
                                "model": OLLAMA_MODEL,
                                "prompt": prompt,
                                "stream": True,
                                "options": {"temperature": 0.7, "top_p": 0.9}
                            }
                            with requests.post(url, json=payload, timeout=1333, stream=True) as resp:
                                resp.raise_for_status()
                                for line in resp.iter_lines():
                                    if line:
                                        data = json.loads(line)
                                        token = data.get("response", "")
                                        full_answer += token
                                        answer_container.markdown(f"```{full_answer}```")
                                        if data.get("done", False):
                                            break
                        except Exception as e:
                            st.error(f"❌ Consultation failed: {str(e)}")

                        # Save to history
                        st.session_state.history.append((user_q, full_answer))

    else:
        st.info("🕸️ No knowledge base loaded. Press **Process PDFs** to begin.")

    # ── History ────────────────────────────────────────
    if st.session_state.get("history"):
        with st.expander("📜 Recent Whispers (last 5)", expanded=False):
            for i, (q, a) in enumerate(reversed(st.session_state.history[-5:]), 1):
                st.markdown(f"**Q{i}:** {q}")
                st.markdown(f"**A{i}:** {a[:300]}...")

            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.rerun()

    # ── Sidebar ────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.caption(f"**PDF Directory:** {PDF_ROOT}")
        st.caption(f"**Ollama Model:** {OLLAMA_MODEL}")
        st.caption(f"**Timeout:** 1333 seconds (CPU)")

if __name__ == "__main__":
    main()
