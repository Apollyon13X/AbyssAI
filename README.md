# ☠️ AbyssAI — Whispers From The Void ⚔️

AbyssAI is a **self-help AI Oracle** that runs on your machine. It is not a chatbot. It is a temple with one occupant: **Professor Apollyon**.

He works where psyche, shadow, and the subconscious meet occult art and the higher laws people once used to raise worlds — and to pull them down. Jung. Archetype. The unnamed thing under the floorboards. Hermetic speech as metaphor for inner work, not costume.

**The work is this:**

1. **See.** Name the pattern. Shadow is not a mood. It is the part of you that acts while you look away.
2. **Integrate.** Stop fighting the shadow as an enemy. Bring it to the table. What you refuse becomes the saboteur.
3. **Unpack.** After integration, use dark-psychology literacy on *yourself*: hooks, guilt, charm, fear, self-betrayal, the inner con. Not a playbook to prey on others — a scalpel for the programs that prey on *you*.
4. **Cut.** Remove harmful, manipulative, and self-sabotaging behaviors and loops.
5. **Rebuild.** Rise with a clean, sharp, determined mind. Fresh. No inherited fog.

Professor Apollyon swings the **pendulum** (your attention), holds the **scales** (what is actually true), and the **sword** (what must be cut). He does not welcome. He was interrupted. He will not nurse you. He will not lie to spare you.

**THE ABYSS — ALL-SEEING, EVER-OPENING, SLEEPLESS AND COUNTLESS EYES — IS STARING AT YOU.**  
**ARE YOU RISING FROM THE ASHES, OR GETTING DEVOURED?**

Your move.

---

- **GUI:** native window (pywebview). Frozen. Do not restyle.
- **Brain:** local Ollama + Dolphin 3.0 Llama 3.2 3B.
- **Library:** your private PDFs in `data/private/` → local BM25 index. Never commit that folder.

Daily launch after install:

```sh
cd ~/AbyssAI
chmod +x AbyssAI.sh
./AbyssAI.sh

Layout
textAbyssAI/
├── AbyssAI.sh            daily launch
├── README.md
├── requirements.txt
├── .gitignore
├── src/                  window, Ollama, index
├── data/private/         YOUR PDFs — gitignored
├── train/                optional private LoRA
├── adapters/             LoRA weights — gitignored
├── scripts/              Void extras, runit
└── gui/                  frozen export notes

Every OS: after packages + venv
Same Python bits everywhere:
shcd ~/AbyssAI
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
chmod +x AbyssAI.sh
./AbyssAI.sh
On Windows use py -3 -m venv --system-site-packages .venv then .venv\Scripts\activate.
On macOS skip --system-site-packages (Cocoa backend, no GTK).

Install — Void Linux (glibc, tested)
shcd ~/AbyssAI
sudo xbps-install -Sy \
  python3 python3-devel python3-pip python3-virtualenv \
  gcc pkg-config curl tar zstd \
  gtk+3 python3-gobject gobject-introspection \
  cairo python3-cairo libwebkit2gtk41
command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 2
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
chmod +x AbyssAI.sh
./AbyssAI.sh
musl Void: do not use install.sh. Build Ollama from source (go build github.com/ollama/ollama). WebKit package is still libwebkit2gtk41.

Install — Debian / Ubuntu / Mint
shcd ~/AbyssAI
sudo apt update
sudo apt install -y python3 python3-venv python3-pip python3-dev \
  gcc pkg-config curl tar zstd \
  python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.1
command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 2
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
chmod +x AbyssAI.sh
./AbyssAI.sh
If gir1.2-webkit2-4.1 is missing: sudo apt install gir1.2-webkit2-4.0.

Install — Fedora / RHEL / CentOS Stream
shcd ~/AbyssAI
sudo dnf install -y python3 python3-pip python3-devel python3-gobject \
  gcc pkgconf-pkg-config curl tar zstd \
  gtk3 webkit2gtk4.1 cairo-gobject
command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 2
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
chmod +x AbyssAI.sh
./AbyssAI.sh
If webkit2gtk4.1 is missing: sudo dnf search webkit2gtk and install the GTK3 WebKit2 package.

Install — Arch / Manjaro / Endeavour
shcd ~/AbyssAI
sudo pacman -Syu --needed python python-pip python-virtualenv \
  python-gobject gtk3 webkit2gtk-4.1 cairo \
  gcc pkgconf curl tar zstd
command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 2
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
chmod +x AbyssAI.sh
./AbyssAI.sh

Install — macOS
shcd ~/AbyssAI
xcode-select --install 2>/dev/null || true
command -v brew >/dev/null || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python ollama
brew services start ollama
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
chmod +x AbyssAI.sh
./AbyssAI.sh

Install — Windows

Install Python 3 (check “Add to PATH”).
Install Ollama for Windows.
PowerShell:

PowerShellcd $HOME\AbyssAI
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
python -m src.main
WebView2 ships with Edge. If the window fails: install the WebView2 runtime.

Private PDFs

Put files in data/private/ (subfolders OK).
Click Process library.
Index is abyss_index.json (local, gitignored).

Optional LoRA (GPU):
sh. .venv/bin/activate
python train/prepare.py
sh train/train.sh
# only if adapters/oracle-lora exists:
ollama create abyss-oracle -f train/Modelfile

Safety
Crisis: drop the persona. Local emergency services, or IASP. No clinical or legal orders.
