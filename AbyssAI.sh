#!/bin/sh
# Installed launcher. No terminal required.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PATH="/usr/local/bin:/usr/bin:$PATH"
LOGDIR="${XDG_STATE_HOME:-$HOME/.local/state}/abyssai"
mkdir -p "$LOGDIR"
LOG="$LOGDIR/abyssai.log"

fail() {
  echo "$*" >>"$LOG"
  command -v notify-send >/dev/null 2>&1 && notify-send "AbyssAI" "$*" || true
  exit 1
}

if [ ! -d .venv ]; then
  fail "No .venv. Run: python3 -m venv --system-site-packages .venv && . .venv/bin/activate && pip install -r requirements.txt"
fi

. .venv/bin/activate

if ! command -v ollama >/dev/null 2>&1; then
  fail "ollama not in PATH"
fi

if ! curl -sf --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  ollama serve >>"$LOG" 2>&1 &
  i=0
  while [ "$i" -lt 20 ]; do
    curl -sf --max-time 1 http://127.0.0.1:11434/api/tags >/dev/null 2>&1 && break
    i=$((i + 1))
    sleep 0.3
  done
fi

exec python -m src.main >>"$LOG" 2>&1
