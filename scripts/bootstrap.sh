bash
#!/usr/bin/env bash
set -euo pipefail

echo "🦴 Initializing Doctor Apollyon's Lair..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Setting up directories..."
mkdir -p abyss_feed

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed!"
    echo "Please install Ollama from https://ollama.ai"
    echo "Then run: ollama serve"
    exit 1
fi

# Check if model is available
echo "Checking Ollama model..."
if ! ollama list | grep -q "$OLLAMA_MODEL" 2>/dev/null; then
    echo "Model $OLLAMA_MODEL not found. Pulling..."
    ollama pull "$OLLAMA_MODEL"
fi

# Set environment variable for Ollama (optional, can override in .env)
export OLLAMA_BASE_URL="http://localhost:11434"

echo "✅ Setup complete!"
echo ""
echo "To start Doctor Apollyon:"
echo "  source .venv/bin/activate"
echo "  streamlit run src/main.py"
echo ""
echo "Make sure Ollama is running: ollama serve"
```

## `Dockerfile` (Optional)
```dockerfile
# Optional Dockerfile for containerized deployment
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libgl1 libglib2.0-0 curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY .gitignore .
COPY README.md .
COPY LICENSE .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Create volume mounts for PDFs and index
VOLUME ["/app/abyss_feed", "/app/data"]

EXPOSE 8501
ENV PORT=8501
ENV OLLAMA_BASE_URL="http://host.docker.internal:11434"

CMD ["streamlit", "run", "src/main.py", "--server.port", "8501", "--server.enableCORS", "false"]
