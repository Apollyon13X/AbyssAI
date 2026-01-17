#!/usr/bin/env bash
set -euo pipefail

# 1️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 2️⃣ Install deps
pip install -r requirements.txt

# 3️⃣ Export your Morpheus key (never commit!)
export MORPHEUS_API_KEY="sk-kLSeGS.2c7344ead2cefd7f9f74d60e3d307cbc68fc1290b39863e01dbedc6f70d262ea"

# 4️⃣ Launch Streamlit UI
streamlit run src/main.py
