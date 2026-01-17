# AbyssAI – Doctor Apollyon (Ethical Hacking & Dark Arts GPT)

> *“From the cryptic corridors of the internet to the hidden sigils of occult lore, Doctor Apollyon guides the way.”*  

A Streamlit‑powered Retrieval‑Augmented Generation (RAG) system that:

* **Indexes** any collection of PDFs (ethical‑hacking manuals, forensic guides, public‑domain occult tomes).  
* **Embeds** chunks with `sentence‑transformers/all‑MiniLM‑L6‑v2`.  
* **Queries** the Morpheus decentralized inference API (your `MORPHEUS_API_KEY`).  
* **Serves** a skull‑themed UI with a haunting background.

---

## Quick start (local)

```bash
git clone https://github.com/<you>/AbyssAI.git
cd AbyssAI
./scripts/bootstrap.sh   # installs deps, sets your API key, launches UI
