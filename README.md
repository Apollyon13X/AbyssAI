 # ☠ AbyssAI - Local AI Knowledge Base 🌪️

A private, uncensored AI assistant that builds a searchable knowledge base from your PDF documents using local models.

---

## ⚠️ URL Access Note
The scraping attempt for `http://localhost:8501**` failed because this is a **local development address** that runs on your machine, not a public website. Once you start AbyssAI, you'll access it at **http://localhost:8501** in your own browser.

---

## 📋 Prerequisites

### All Platforms
- **Python 3.8+** installed
- **Git** installed
- **Ollama** installed and working
- At least **4GB RAM** (8GB recommended)
- **PDF files** to build your knowledge base

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv git curl

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
- **Python**: Download from [python.org](https://www.python.org/downloads/) (check "Add to PATH" during install)
- **Git**: Download from [git-scm.com](https://git-scm.com/download/win)
- **Ollama**: Download installer from [ollama.ai](https://ollama.ai/)
- **Windows Terminal** (recommended, from Microsoft Store)

### Mac
```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python git

# Install Ollama
brew install ollama
```

---

## 🚀 Installation Guide

### 🐧 Linux Setup

#### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/abyssai.git
cd abyssai
```

#### Step 2: Create Virtual Environment
```bash
# Remove any broken venv first
rm -rf .venv

# Create fresh venv
python3 -m venv .venv

# Activate (Linux syntax - IMPORTANT!)
source .venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 4: Make Bootstrap Executable
```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

#### Step 5: Create Data Directory
```bash
mkdir -p abyss_feed
```

#### Step 6: Pull AI Model
Open a **new terminal** and run:
```bash
ollama serve
```
Then in your main terminal:
```bash
ollama pull llama2-uncensored
```

---

### 🪟 Windows Setup

#### Step 1: Clone the Repository
```powershell
# In Windows Terminal or PowerShell
git clone https://github.com/yourusername/abyssai.git
cd abyssai
```

#### Step 2: Create Virtual Environment
```powershell
# Remove any broken venv first
if (Test-Path .venv) { Remove-Item -Recurse -Force .venv }

# Create fresh venv
python -m venv .venv

# Activate (Windows syntax - IMPORTANT!)
.venv\Scripts\activate
```

#### Step 3: Install Dependencies
```powershell
# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 4: Run Bootstrap Script
```powershell
# Windows doesn't need chmod
.\scripts\bootstrap.sh

# If the above fails, run the commands manually:
# python -m pip install --upgrade pip
# pip install -r requirements.txt
```

#### Step 5: Create Data Directory
```powershell
mkdir abyss_feed
```

#### Step 6: Pull AI Model
1. Open **Ollama Desktop App** or
2. Open a **new terminal** and run:
```powershell
ollama serve
```
Then in your main terminal:
```powershell
ollama pull llama2-uncensored
```

---

### 🍎 Mac Setup

#### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/abyssai.git
cd abyssai
```

#### Step 2: Create Virtual Environment
```bash
# Remove any broken venv first
rm -rf .venv

# Create fresh venv
python3 -m venv .venv

# Activate (Mac/Linux syntax)
source .venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 4: Make Bootstrap Executable
```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

#### Step 5: Create Data Directory
```bash
mkdir -p abyss_feed
```

#### Step 6: Pull AI Model
Open a **new terminal** and run:
```bash
ollama serve
```
Then in your main terminal:
```bash
ollama pull llama2-uncensored
```

---

## 📁 Project Structure After Setup
```
abyssai/
├── .venv/                 # Virtual environment
├── abyss_feed/            # YOUR PDFs GO HERE
├── scripts/
│   └── bootstrap.sh       # Setup script
├── src/
│   └── main.py           # Main application
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── abyss_index.faiss    # Generated search index
└── abyss_meta.json      # Generated metadata
```

---

## 🎯 Usage Instructions (All Platforms)

### Step 1: Add Your PDFs
Copy your PDF files into the `abyss_feed/` folder.

### Step 2: Activate Virtual Environment
**Linux/Mac:**
```bash
source .venv/bin/activate
```

**Windows:**
```powershell
.venv\Scripts\activate
```

### Step 3: Start Ollama
In a **separate terminal**:
```bash
ollama serve
```

### Step 4: Launch AbyssAI
In your main terminal:
```bash
streamlit run src/main.py
```

### Step 5: Access the Interface
Open your browser and go to: **http://localhost:8501**

### Step 6: Build Knowledge Base
Click the **"Process PDFs"** button to index your documents.

### Step 7: Start Chatting
Ask questions about your PDFs in the chat interface!

---

## 🔧 Troubleshooting

### Virtual Environment Issues

| Problem | Linux/Mac Solution | Windows Solution |
|---------|-------------------|------------------|
| `command not found` | Use `source .venv/bin/activate` | Use `.venv\Scripts\activate` |
| Can't deactivate | `deactivate` | `deactivate` |
| Venv won't create | Install `python3-venv` | Reinstall Python with "Add to PATH" |

### Pip Install Failures

**On all platforms:**
1. Ensure venv is activated (see prompt prefix `(.venv)`)
2. Run `pip install --upgrade pip` first
3. Check you're in the `abyssai/` directory: `pwd` or `cd`

### Ollama Connection Errors

**Error:** "Cannot connect to Ollama"
- **Solution 1:** Run `ollama serve` in a **separate terminal**
- **Solution 2:** Check Ollama is installed: `ollama --version`
- **Solution 3:** Try `OLLAMA_HOST=0.0.0.0 ollama serve` (Linux/Mac)

### Import Errors After Install

**Error:** `ModuleNotFoundError: No module named 'streamlit'`
- **Solution:** Re-run installation with venv active:
  ```bash
  source .venv/bin/activate  # or Windows equivalent
  pip install -r requirements.txt
  ```

### Permission Denied (Linux/Mac)

**Error:** `Permission denied: scripts/bootstrap.sh`
- **Solution:** `chmod +x scripts/bootstrap.sh`

### Memory Issues

**Error:** "CUDA out of memory" or system hangs
- **Solution:** Use smaller PDF batches, close other applications, or add more RAM

### Port Already in Use

**Error:** "Address already in use: 8501"
- **Solution:** Kill other Streamlit processes or specify a different port:
  ```bash
  streamlit run src/main.py --server.port 8502
  ```

---

## 🔄 Updating AbyssAI

```bash
# Activate venv first
source .venv/bin/activate  # or Windows equivalent

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt
```

---

## 🗑️ Starting Fresh (If All Else Fails)

**Linux/Mac:**
```bash
deactivate
rm -rf .venv abyss_index.faiss abyss_meta.json
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```powershell
deactivate
Remove-Item -Recurse -Force .venv
Remove-Item abyss_index.faiss, abyss_meta.json
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🛡️ Security Note
All processing happens **locally on your machine**. Your PDFs and data never leave your system.

---

## 📚 Need More Help?
- Check the logs in your terminal for specific error messages
- Ensure Ollama is running before starting Streamlit
- Verify PDFs are in the `abyss_feed/` directory

Happy hacking with your local AI knowledge base!
