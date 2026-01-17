# --------------------------------------------------------------
# Base image – slim Python, small enough for a decentralized node
# --------------------------------------------------------------
FROM python:3.11-slim

# System libraries needed by PyMuPDF & FAISS
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cache dependencies early
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY .gitignore .
COPY README.md .
COPY LICENSE .

# Non‑root user – good hygiene on public nodes
RUN useradd -m appuser
USER appuser

EXPOSE 8501
ENV PORT=8501
CMD ["streamlit", "run", "src/main.py", "--server.port", "8501", "--server.enableCORS", "false"]
