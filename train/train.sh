#!/bin/sh
# ~/AbyssAI/train/train.sh
set -eu
cd "$(dirname "$0")/.."
. .venv/bin/activate
python train/prepare.py
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "No GPU. JSONL ready at data/private/corpus.jsonl — do not commit it."
  exit 0
fi
pip install -q "unsloth>=2024.12"
python - <<'PY'
from pathlib import Path
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.2-3B-Instruct", max_seq_length=2048, load_in_4bit=True
)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16, lora_dropout=0)
ds = load_dataset("json", data_files="data/private/corpus.jsonl", split="train")
SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=ds,
    args=TrainingArguments(output_dir="train/out", per_device_train_batch_size=2, num_train_epochs=1, fp16=True),
).train()
Path("adapters/oracle-lora").mkdir(parents=True, exist_ok=True)
model.save_pretrained("adapters/oracle-lora")
print("Adapter saved. ollama create abyss-oracle -f train/Modelfile")
PY
