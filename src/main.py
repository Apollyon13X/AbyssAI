import json
import streamlit as st
import faiss
from sentence_transformers import SentenceTransformer

from .config import *
from .index import load_prebuilt_index, process_pdfs
from .pdf_utils import pdf_to_text, split_chunks
from .api_client import query_morpheus


def answer_query(query: str, index: faiss.IndexFlatIP, meta: List[dict],
                 embedder: SentenceTransformer) -> str:
    """Retrieve top‑k chunks, stitch them into a prompt for Doctor Apollyon."""
    q_emb = embedder.encode([query], normalize_embeddings=True).astype(np.float32)
    _, I = index.search(q_emb, k=5)                     # top‑5 most similar

    context_parts = []
    for idx in I[0]:
        src = meta[idx]
        pdf_path = Path(src["source"])
        raw = pdf_to_text(pdf_path)
        chunk = split_chunks(raw)[src["chunk_id"]]
        context_parts.append(f"[{pdf_path.name} – chunk {src['chunk_id']}] {chunk}")

    context = "\n---\n".join(context_parts)

    prompt = (
        f"You are Doctor Apollyon, a seasoned cyber‑mage who teaches ethical hacking.\n"
        f"Use the following excerpts from the supplied PDFs as your grim grimoire:\n\n"
        f"{context}\n\n"
        f"Answer concisely and with technical depth:\n{query}"
    )
    return prompt


def main():
    st.set_page_config(page_title="🦴 Doctor Apollyon", layout="centered")

    # ── UI cosmetics (keep your skull‑theme) ───────────────────────
    seal_url = "https://i.etsystatic.com/40811848/r/il/c670c3/5283635364/il_1080xN.5283635364_ki78.jpg"
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url('{seal_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: #0b0b0b;
            color: #e0e0e0;
        }}
        .stButton > button {{
            background-color:#2c0a0a;
            color:#ff4d4d;
            border:2px solid #ff1a1a;
            font-weight:bold;
        }}
        .stTextInput > div > div > input {{
            background-color:#1a1a1a;
            color:#ffdddd;
        }}
        .stHeader > h1 {{color:#ff6666; text-shadow:0 0 10px #ff0000;}}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title(":skull_and_crossbones: Doctor Apollyon")
    st.subheader("Ask the dark doctor anything about ethical hacking.")

    # ── Load or build index ───────────────────────────────────────
    if "index" not in st.session_state:
        idx, meta = load_prebuilt_index()
        if idx:
            st.session_state.update(
                {"index": idx, "meta": meta, "embedder": SentenceTransformer(EMBED_MODEL)}
            )
        else:
            st.session_state.update({"index": None, "meta": [], "embedder": None})

    # ── PDF uploader ───────────────────────────────────────────────
    uploaded = st.file_uploader(
        "📂 Drop new PDFs here (they’ll be copied into **abyss_feed**):",
        type=["pdf"],
        accept_multiple_files=True,
    )
    if uploaded:
        PDF_ROOT.mkdir(parents=True, exist_ok=True)
        for uf in uploaded:
            dest = PDF_ROOT / uf.name
            dest.write_bytes(uf.getbuffer())
        st.success(f"✅ Copied {len(uploaded)} PDF(s) into **abyss_feed**.")

    # ── Build index button ───────────────────────────────────────
    if st.button("⚙️ Process PDFs (build/re‑build index)"):
        try:
            idx, meta = process_pdfs()
            st.session_state.update(
                {"index": idx, "meta": meta, "embedder": SentenceTransformer(EMBED_MODEL)}
            )
            st.success("✅ Knowledge base ready!")
        except Exception as e:
            st.error(f"❌ Failed to process PDFs: {e}")

    # ── Query UI ─────────────────────────────────────────────────
    if st.session_state.get("index"):
        user_q = st.text_input("💀 Whisper your query:", "")
        if st.button("Summon Apollyon"):
            if not user_q.strip():
                st.warning("The void is silent… type a question first.")
            else:
                prompt = answer_query(
                    user_q,
                    st.session_state.index,
                    st.session_state.meta,
                    st.session_state.embedder,
                )
                answer = query_morpheus(prompt)
                st.markdown(f"**🗣️ Doctor Apollyon replies:**\n\n{answer}")
    else:
        st.info("🕸️ No index loaded. Upload PDFs and press **Process PDFs** to begin.")


if __name__ == "__main__":
    main()
