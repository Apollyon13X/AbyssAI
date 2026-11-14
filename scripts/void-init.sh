#!/bin/sh
# ~/AbyssAI/scripts/void-init.sh
# Void Linux: system packages, Ollama, Dolphin 3B, .venv
set -eu

ROOT="${HOME}/AbyssAI"
cd "$ROOT"

echo "==> packages"
sudo xbps-install -Syu
sudo xbps-install -Sy \
  python3 python3-devel python3-pip python3-virtualenv \
  gcc pkg-config curl tar zstd \
  gtk+3 python3-gobject gobject-introspection \
  cairo python3-cairo
# WebKit for pywebview (name varies on Void)
sudo xbps-install -Sy webkit2gtk 2>/dev/null \
  || sudo xbps-install -Sy webkitgtk 2>/dev/null \
  || sudo xbps-install -Sy webkit2gtk41 2>/dev/null \
  || echo "WARN: install a webkit2gtk package manually"

echo "==> ollama"
if ! command -v ollama >/dev/null 2>&1; then
  if ldd --version 2>&1 | grep -qi musl; then
    echo "musl Void: official install.sh is glibc. Build Ollama from source."
    exit 1
  fi
  curl -fsSL https://ollama.com/install.sh | sh
fi

if ! curl -sf --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  ollama serve >/tmp/ollama.log 2>&1 &
  sleep 3
fi

echo "==> model"
ollama pull nchapman/dolphin3.0-llama3:3b

echo "==> venv"
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

mkdir -p adapters data/private train/out
touch data/private/.keep adapters/.keep 2>/dev/null || true

echo "==> done"
echo "  activate:  . .venv/bin/activate"
echo "  run:       python -m src.main"
