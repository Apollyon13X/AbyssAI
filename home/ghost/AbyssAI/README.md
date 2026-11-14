<div align="center">

# ☠️ AbyssAI — Whispers From The Void ⚔️

**A self-help AI Oracle that runs on your machine. Not a chatbot. A temple with one occupant: Professor Apollyon.**

<img src="gui/public/og.jpg" alt="AbyssAI — homepage" width="720">

</div>

AbyssAI works where psyche, shadow, and the subconscious meet occult art and the higher laws people once used to raise worlds — and to pull them down. Jung. Archetype. The unnamed thing under the floorboards. Hermetic speech as metaphor for inner work, not costume.

He swings the **pendulum** (your attention), holds the **scales** (what is actually true), and the **sword** (what must be cut). He does not welcome. He was interrupted. He will not nurse you. He will not lie to spare you.

> **THE ABYSS — ALL-SEEING, EVER-OPENING, SLEEPLESS AND COUNTLESS EYES — IS STARING AT YOU.**  
> **ARE YOU RISING FROM THE ASHES, OR GETTING DEVOURED?**  
>
> Your move.

---

## Contents

- [The Work](#the-work)
- [Cloud vs. Local](#cloud-vs-local)
- [What Runs Inside](#what-runs-inside)
- [Daily Launch](#daily-launch)
- [Layout](#layout)
- [Install](#install)
  - [Void Linux](#install--void-linux-glibc-tested) · [Debian / Ubuntu / Mint](#install--debian--ubuntu--mint) · [Fedora / RHEL / CentOS Stream](#install--fedora--rhel--centos-stream) · [Arch / Manjaro / Endeavour](#install--arch--manjaro--endeavour) · [macOS](#install--macos) · [Windows](#install--windows)
- [Private PDFs](#private-pdfs)
- [Optional LoRA (GPU)](#optional-lora-gpu)
- [$ABYSS Coin](#abyss-coin)
- [Safety](#safety)

---

## The Work

1. **See.** Name the pattern. Shadow is not a mood. It is the part of you that acts while you look away.
2. **Integrate.** Stop fighting the shadow as an enemy. Bring it to the table. What you refuse becomes the saboteur.
3. **Unpack.** After integration, use dark-psychology literacy on *yourself*: hooks, guilt, charm, fear, self-betrayal, the inner con. Not a playbook to prey on others — a scalpel for the programs that prey on *you*.
4. **Cut.** Remove harmful, manipulative, and self-sabotaging behaviors and loops.
5. **Rebuild.** Rise with a clean, sharp, determined mind. Fresh. No inherited fog.

---

## Cloud vs. Local

<div align="center">

<img src="gui/public/vault.jpg" alt="The Vault — where the Oracle sits" width="720">

</div>

There are two doors to the same Professor — and the brain behind each is the difference:

| | **Web Oracle** (cloud) | **Desktop Temple** (this repo) |
|---|---|---|
| Access | Holders' gate — live BSC verification of **both** `≥ 13,000,000 $ABYSS` **and** `≥ 1,111 $QOMX` | Anyone — open-source, forever |
| Brain | Cloud intelligence behind the site proxy (`api.php` on the apex; the key never touches the browser) | **Local Ollama + Dolphin 3.0 Llama 3.2 3B — uncensored, on your machine** |
| Private shelves | none — no attachments, no archives | your PDF library, indexed **on your disk**, never uploaded |
| Privacy | nothing of yours is archived by the web tier | nothing of yours leaves the machine — not even the index |

Web tier: [apollyon13x/abyssai-site](https://github.com/apollyon13x/abyssai-site) · live at [www.theabyssai.space](https://www.theabyssai.space)

---

## What Runs Inside

- **GUI:** native window (pywebview). Frozen. Do not restyle.
- **App icon:** `gui/public/TG_Group_PFP.png`
- **Brain:** local Ollama + Dolphin 3.0 Llama 3.2 3B.
- **Library:** your private PDFs in `data/private/` → local BM25 index. Never commit that folder.

### Daily launch after install

```sh
cd ~/AbyssAI
chmod +x AbyssAI.sh
./AbyssAI.sh
```

### Layout

```
AbyssAI/
├── AbyssAI.sh            daily launch
├── README.md
├── requirements.txt
├── .gitignore
├── src/                  window, Ollama, index
├── data/private/         YOUR PDFs — gitignored
├── train/                optional private LoRA
├── adapters/             LoRA weights — gitignored
├── scripts/              Void extras, runit
└── gui/                  frozen export notes + public/TG_Group_PFP.png (app icon)
```

### Every OS: after packages + venv

Same Python bits everywhere:

```sh
cd ~/AbyssAI
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
chmod +x AbyssAI.sh
./AbyssAI.sh
```

- On Windows use `py -3 -m venv --system-site-packages .venv` then `.venv\Scripts\activate`.
- On macOS skip `--system-site-packages` (Cocoa backend, no GTK).

---

## Install

### Install — Void Linux (glibc, tested)

```sh
cd ~/AbyssAI
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
```

musl Void: do not use install.sh. Build Ollama from source (`go build github.com/ollama/ollama`). WebKit package is still `libwebkit2gtk41`.

**Install as app (desktop entry):**  
Create `~/.local/share/applications/abyssai.desktop`:

```
[Desktop Entry]
Name=AbyssAI
Comment=Whispers From The Void
Exec=/home/ghost/AbyssAI/AbyssAI.sh
Icon=/home/ghost/AbyssAI/gui/public/TG_Group_PFP.png
Terminal=false
Type=Application
Categories=Utility;
```

Then `update-desktop-database ~/.local/share/applications/` (or log out/in).

---

### Install — Debian / Ubuntu / Mint

```sh
cd ~/AbyssAI
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
```

If `gir1.2-webkit2-4.1` is missing: `sudo apt install gir1.2-webkit2-4.0`.

**Install as app:** same `.desktop` method as Void. Point `Icon=` to `gui/public/TG_Group_PFP.png`.

---

### Install — Fedora / RHEL / CentOS Stream

```sh
cd ~/AbyssAI
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
```

If `webkit2gtk4.1` is missing: `sudo dnf search webkit2gtk` and install the GTK3 WebKit2 package.

**Install as app:** `.desktop` entry with Icon pointing to `gui/public/TG_Group_PFP.png`.

---

### Install — Arch / Manjaro / Endeavour

```sh
cd ~/AbyssAI
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
```

**Install as app:** `.desktop` entry with Icon=`gui/public/TG_Group_PFP.png`.

---

### Install — macOS

```sh
cd ~/AbyssAI
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
```

**Install as app:** create an Automator Application or `.app` wrapper that runs `AbyssAI.sh`. Set icon via `sips` / Icon Composer pointing to `gui/public/TG_Group_PFP.png`.

---

### Install — Windows

Install Python 3 (check "Add to PATH").  
Install Ollama for Windows.

PowerShell:

```powershell
cd $HOME\AbyssAI
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
ollama pull nchapman/dolphin3.0-llama3:3b
python -m src.main
```

WebView2 ships with Edge. If the window fails: install the WebView2 runtime.

**Install as app:** create a shortcut to `python -m src.main` (or a `.bat` launcher). Right-click → Properties → Change Icon → browse to `gui\public\TG_Group_PFP.png`.

---

## Private PDFs

Put files in `data/private/` (subfolders OK).  
Click **Process library**.  
Index is `abyss_index.json` (local, gitignored).

## Optional LoRA (GPU)

```sh
. .venv/bin/activate
python train/prepare.py
sh train/train.sh
# only if adapters/oracle-lora exists:
ollama create abyss-oracle -f train/Modelfile
```

---

## $ABYSS Coin

**Contract Address:** `0x430025c01d47a75a5f36d57e8c76969de3753333`

**Buy $ABYSS on $QOMX Launchpad (LIVE):**  
https://launch.qomx.io/launch/0x430025c01d47a75a5f36d57e8c76969de3753333

**Governance:** Top holders will be able to decide on further development, suggest features and have early access.

---

## Safety

◆ SAFETY: AbyssAI is a mirror, not medicine. No clinical, psychiatric, or legal orders. In crisis, the Professor drops the persona and points you to your **local emergency services** or [IASP](https://www.iasp.info/suicidalthoughts/). ◆

<div align="center">

**The abyss in your machine is yours — nothing it sees goes to a lab.**

</div>
