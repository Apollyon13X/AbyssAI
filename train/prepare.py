"""~/AbyssAI/train/prepare.py — private PDFs → gitignored JSONL."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.pdf_utils import pdf_to_text, split_chunks

SRC = ROOT / "data" / "private"
OUT = SRC / "corpus.jsonl"


def main() -> None:
    pdfs = list(SRC.rglob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"Drop PDFs into {SRC} first.")
    n = 0
    with OUT.open("w", encoding="utf-8") as fh:
        for pdf in pdfs:
            raw = pdf_to_text(pdf)
            for chunk in split_chunks(raw):
                rec = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Professor Apollyon. Inner-work oracle. No attack recipes. No clinical orders.",
                        },
                        {
                            "role": "user",
                            "content": "Hold this passage.\n\n" + chunk,
                        },
                        {
                            "role": "assistant",
                            "content": "Held. Inner work only. I will not dump the source.",
                        },
                    ]
                }
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
    print(f"Wrote {n} private examples → {OUT}")


if __name__ == "__main__":
    main()
