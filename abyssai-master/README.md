# ☠ AbyssAI — Whispers From The Void

**MADE FOR EDUCATIONAL PURPOSES ONLY**

**A fully local, private AI grimoire** that turns your ethical hacking, digital forensics, and occult PDFs into a living oracle.

Professor Apollyon now whispers from the abyss — completely offline, no data ever leaves your machine.

---

## ✨ Features

- 100% local (Ollama + FAISS + Streamlit)
- Indexes **all** PDFs in `abyss_lessons/` and subfolders (including `abyss_whispers/`)
- **Pre-loaded with documentation on ethical hacking techniques, digital forensics methodologies, and curated forbidden knowledge** — ready to query out of the box
- Dark occult cyber aesthetic with animated seal background
- **Enter-to-send** + live streaming answers (Professor types in real time)
- 777-second timeout for slow machines
- History of your whispers
- Zero cloud, zero telemetry, zero censorship

---

## ⚡ 30-Second TL;DR

1. Install **Python 3.10+** and **Ollama**
2. Run: `ollama pull llama2-uncensored:7b`
3. Clone this repo: `git clone https://github.com/Apollyon13X/AbyssAI`
4. Create a virtual environment
5. `cd ~/AbyssAI/abyssai-master`
6. `pip install -r requirements.txt`
7. Put your PDFs into `abyss_lessons/`
8. Start Ollama: `ollama serve`
9. Launch AbyssAI: `streamlit run src/main.py`
10. Open `http://localhost:8501`
11. Click **Process PDFs**, then start asking questions

**Pro tip:** AI already contains built-in documentation on ethical hacking, digital forensics, and forbidden knowledge—query it directly without adding PDFs.

That's it — Professor Apollyon is online.

---

## 📁 Project Structure (your current layout)
~/AbyssAI/ ├── abyss_lessons/ ← YOUR PDFs (Cyber + Occult) │ ├── abyss_whispers/ │ └── all your other PDFs... ├── abyssai-master/ ← this repo │ ├── src/ │ ├── requirements.txt │ └── ...

Important: abyss_lessons must stay sibling to the abyssai-master folder.

🐧 Quick Start (Linux)
cd ~/AbyssAI/abyssai-master

# Activate environment
source .venv/bin/activate

# Start Ollama (if not running)
ollama serve   # or let the systemd service run

# Launch the abyss
streamlit run src/main.py

# Open http://localhost:8501
# First time:
# - Click Process PDFs (indexes all 36 of your PDFs)
# - Type any question → press Enter
# - Wait (slow laptop = up to 13 min)
Troubleshooting (Linux)
Issue	Solution
Answers take forever?	Your CPU is working. 777 seconds is already set. Just wait.
Ollama not found?	Run ollama serve in another terminal.
Want even more time?	Edit src/main.py and change timeout=777 to timeout=1800.
🪟 Quick Start (Windows)
# Prerequisites installed first:
# - Python 3.10+ from python.org (check "Add to PATH")
# - Git from git-scm.com
# - Ollama installer from ollama.ai/windows

# 1. Open PowerShell
cd ~\Documents
git clone https://github.com/Apollyon13X/AbyssAI.git
cd AbyssAI\abyssai-master

# 2. Create & Activate Virtual Environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Pull the Model (NEW terminal window!)
# Keep Ollama running in the background
ollama serve

# 5. Launch the abyss (in project terminal where venv is active)
streamlit run src/main.py

# Open http://localhost:8501
# First time: Click Process PDFs, then ask questions.
Troubleshooting (Windows)
Issue	Solution
Activation blocked?	Run PowerShell as Admin: Set-ExecutionPolicy RemoteSigned
Port already in use?	Close other Streamlit/Python instances or edit src/main.py port config
Slow answers?	Your CPU is working hard. 777-second timeout is standard. Wait it out.
🍎 Quick Start (macOS)
# Prerequisites installed first:
# - Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# - Python 3.10+: brew install python@3.10
# - Git: brew install git
# - Ollama: ollama.ai/mac DMG or `brew install ollama && ollama start`

# 1. Open Terminal
cd ~/Documents
git clone https://github.com/Apollyon13X/AbyssAI.git
cd AbyssAI/abyssai-master

# 2. Create & Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Dependencies
pip3 install -r requirements.txt

# 4. Pull the Model (SEPARATE tab/window)
# Ensure Ollama is running before launching AbyssAI
ollama pull llama2-uncensored:7b
ollama serve

# 5. Launch the abyss (main project terminal)
streamlit run src/main.py

# Open http://localhost:8501 in Safari or Chrome
# First time: Click Process PDFs, then ask questions.
Troubleshooting (macOS)
Issue	Solution
Permission Denied?	Allow "System Extension" in System Settings > Privacy & Security if Ollama blocks access
source command missing?	Use .venv/bin/activate directly
Gatekeeper blocking Ollama?	Right-click Ollama app > Open
CPU Fan going wild?	Normal for local inference. Adjust chunk size in src/config.py
🔧 Advanced Customization Examples
AbyssAI is intentionally minimal and hackable. Here are common ways people customize it:

📚 Change the Knowledge Domain
Simply replace the PDFs inside abyss_lessons/:

Programming / DevOps manuals → Coding assistant
Cybersecurity books → Red team / blue team tutor
Medical or psychology literature → Study or therapeutic companion
Philosophy or spiritual texts → Personal reflection oracle
No retraining required — just re-process PDFs.

🧠 Therapeutic / Self-Reflection Mode
Feed AbyssAI with:

CBT workbooks
Trauma-informed care guides
Academic psychology PDFs
Mindfulness manuals
The system will respond entirely based on your provided material, allowing private, offline self-exploration.

🛠 Developer Tweaks
Inside src/ you can:

Modify prompts
Change UI labels / theme
Swap embedding models
Adjust chunk sizes
Increase timeout (default: 1333 seconds)
AbyssAI is meant to be bent, reshaped, and personalized.

🔒 Security & Privacy
Everything runs on your machine only.
No internet required after model download.
Your grimoires stay private.
📜 License
MIT © 2026 Apollyon13X

Made for those who walk between the code and the occult.
