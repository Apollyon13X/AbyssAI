# ☠ AbyssAI – Doctor Apollyon

*“From the cryptic corridors of the internet to the hidden sigils of occult lore, Doctor Apollyon guides the way.”*

A **local-first**, privacy-focused Retrieval-Augmented Generation (RAG) system powered by Streamlit and Ollama for educational ethical hacking and cybersecurity research.

---

## Features

- 📚 **Index any PDF collection**: Scans `abyss_feed/` directory for manuals, guides, and research papers
- 🔍 **Smart chunking**: Overlapping text chunks for better context retention
- 🧠 **Local embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2`
- 🤖 **Uncensored AI**: Integrates with local Ollama models (llama2-uncensored, wizard-vicuna, etc.)
- 💀 **Dark aesthetic**: Skull-themed UI with customizable branding
- 🔒 **100% local**: No cloud APIs required, perfect for sensitive research

---

## 🚀 Quick Start (Recommended: Local Installation)

### Prerequisites

- **Python 3.11** (3.10+ supported)
- **Ollama** installed and running: https://ollama.ai
- At least **4GB RAM** (8GB+ recommended for larger models)
- PDF files (ethical hacking manuals, security guides, etc.)

### Step-by-Step Setup

#### **1. Clone & Enter**
```bash
git clone https://github.com/Apollyon13X/abyssai.git
cd abyssai
```

#### **2. Run Bootstrap Script**
```bash
# Linux / macOS
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh

# Windows (PowerShell)
# First install Python 3.11 from python.org
# Then:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### **3. Add Your PDFs**
Place your ethical hacking PDFs in the `abyss_feed/` directory:
```bash
mkdir -p abyss_feed
cp ~/Downloads/hacking-guide.pdf abyss_feed/
```

#### **4. Start Ollama**
In a **separate terminal**:
```bash
ollama serve
```

Pull an uncensored model if needed:
```bash
ollama pull llama2-uncensored
# Alternative: ollama pull wizard-vicuna-uncensored
```

#### **5. Launch Doctor Apollyon**
```bash
# Activate venv if not already active
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

streamlit run src/main.py
```

Visit **http://localhost:8501**

---

## 📖 Usage Guide

### First Time Setup
1. Upload PDFs via the web interface OR place them in `abyss_feed/`
2. Click **"Process PDFs"** to build the vector index (one-time per PDF set)
3. Wait for "✅ Knowledge base ready!"

### Asking Questions
1. Type your question (e.g., "Explain buffer overflow exploitation")
2. Click **"Summon Apollyon"**
3. Doctor Apollyon will search the PDFs and provide an answer with citations

### Managing the Knowledge Base
- **Add PDFs**: Use the uploader or drag files into `abyss_feed/`
- **Rebuild index**: Click "Process PDFs" again after adding new files
- **Clear everything**: Delete `abyss_index.faiss`, `abyss_meta.json`, and PDFs

---

## 🔧 Configuration

Create a `.env` file in the project root to override settings:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2-uncensored
OLLAMA_TIMEOUT=120
CHUNK_SIZE=500
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## 🐳 Alternative: Docker Setup

If you prefer Docker (requires Ollama on host):
```bash
# Build image
docker build -t abyssai .

# Run container (mount PDFs and Ollama)
docker run -it --rm \
  -p 8501:8501 \
  -v $(pwd)/abyss_feed:/app/abyss_feed \
  -v $(pwd)/data:/app/data \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  abyssai
```

---

## 📁 Project Structure

```
abyssai/
├── abyss_feed/          # Your PDFs (gitignored)
├── src/
│   ├── main.py         # Streamlit UI
│   ├── config.py       # Configuration
│   ├── index.py        # FAISS indexing logic
│   ├── pdf_utils.py    # PDF text extraction
│   └── api_client.py   # Ollama integration
├── scripts/
│   └── bootstrap.sh    # Setup script
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔐 Security & Privacy

- **No data leaves your machine**: All processing is local
- **Secrets gitignored**: API keys (if any) belong in `.env`
- **Ollama models**: Run completely offline after downloading
- **PDF scanning**: Only reads files you explicitly provide

---

## 💻 OS-Specific Notes

### Linux (Ubuntu/Debian)
```bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
```

### macOS
```bash
# Install Python via Homebrew
brew install python@3.11

# Install Ollama
brew install ollama
```

### Windows 10/11
1. Install Python 3.11 from [python.org](https://python.org)
2. Install Ollama from [ollama.ai](https://ollama.ai)
3. Use PowerShell for all commands
4. Run Ollama from Start Menu, then keep it running

---

## 🍺 Model Recommendations

For uncensored ethical hacking education:

| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| `llama2-uncensored` | 7B | Good | Fast |
| `wizard-vicuna-uncensored` | 13B | Better | Medium |
| `solar` | 10.7B | Excellent | Medium |
| `mixtral` | 46.7B | Best | Slow (needs 16GB+ VRAM) |

Pull with: `ollama pull <model-name>`

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Cannot connect to Ollama"** | Verify `ollama serve` is running in another terminal |
| **Model not found** | Run `ollama pull llama2-uncensored` |
| **Slow indexing** | Normal for many PDFs. Uses CPU embedding |
| **Out of memory** | Reduce `CHUNK_SIZE` or use a smaller Ollama model |
| **PDFs not processing** | Check PDFs are text-based (not scanned images) |
| **Import errors** | Re-run `pip install -r requirements.txt` in venv |

---

## 🎓 Educational Use

This platform is designed for:
- Security researchers studying attack vectors
- Students learning ethical hacking techniques
- CTF participants researching challenges
- Educators building custom training materials

**⚠️ Legal Notice**: Only use on systems you own or have explicit permission to test.

---

## 📜 License

MIT License - See LICENSE file. Use responsibly.

---

## 🔮 Future Enhancements

- [ ] GPU acceleration for embeddings
- [ ] Multi-language PDF support
- [ ] Advanced chunking strategies
- [ ] Conversation memory
- [ ] Export chat logs
- [ ] Dark mode UI toggle

---

**Enter the void at your own risk. The doctor is waiting.** 💀
```

---

## Setup Instructions Summary

1. **Clone repo**: `git clone https://github.com/Apollyon13X/abyssai.git`
2. **Run setup**: `cd abyssai && ./scripts/bootstrap.sh` (or manual venv setup)
3. **Install Ollama**: From https://ollama.ai and run `ollama serve`
4. **Pull model**: `ollama pull llama2-uncensored`
5. **Add PDFs**: Place in `abyss_feed/` folder
6. **Launch**: `streamlit run src/main.py`
7. **Process PDFs**: Click button in UI to build index
8. **Query**: Ask Doctor Apollyon your questions
