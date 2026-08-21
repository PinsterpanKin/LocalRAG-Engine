git clone <https://github.com/PinsterpanKin/LocalRAG-Engine>
available on GitHub, so just feel free to use and modify it for your own local AI 
# Local Retrieval Augmented Generation Engine

This repository is a local Retrieval-Augmented Generation (RAG) system combining
LangChain, ChromaDB, Streamlit and Ollama. It lets you upload private documents
and chat with them locally using Ollama-powered LLMs.

## 👀 Project Overview

### 🌟 Key Features
- **Knowledge Base Management** — Upload `.txt`, `.md`, `.pdf`, `.html`, `.docx` files and index them into a local vector store.
- **Intelligent Retrieval** — Uses the `bge-m3` embedding model (via Ollama) to find relevant context.
- **Context-Aware Chat** — Answers questions based on your documents using `llama3` (run via Ollama).
- **Persistent Memory** — Chat history and metadata are saved locally for continuity.
- **Multi-user Conversations** — Use a user name to keep separate local conversation workspaces.
- **Session Management** — View saved conversations, create new sessions, and clear the current session from the chat sidebar.
- **MD5 Deduplication** — Uploaded files are skipped if identical content has already been indexed.

### 🛠️ Tech Stack
- **Core Framework**: LangChain
- **UI**: Streamlit (`app_file_uploader.py`, `interface/app_qa.py`)
- **Vector DB**: ChromaDB (persisted to `chroma_db/`)
- **Local LLM Engine**: Ollama (models: `llama3`, `bge-m3`)
- **Language**: Python 3.12

## 🚀 Quick Start

### 1) Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2) Install Python dependencies (example)

```bash
./venv/bin/python -m pip install --upgrade pip setuptools wheel
./venv/bin/python -m pip install \
  streamlit langchain langchain-ollama langchain-chroma \
  langchain-text-splitters chromadb beautifulsoup4 python-docx \
  pypdf PyPDF2
```

## Ollama (local LLM) — install & models

This project relies on a locally-running Ollama API. Install Ollama and pull models:

1. Install `zstd` (required by installer) and run installer:

```bash
sudo apt-get update
sudo apt-get install -y zstd
curl -fsSL https://ollama.com/install.sh -o /tmp/ollama-install.sh
sudo bash /tmp/ollama-install.sh
rm -f /tmp/ollama-install.sh
```

2. Pull the example models used by this repo:

```bash
/usr/local/bin/ollama pull llama3
/usr/local/bin/ollama pull bge-m3
```

3. Confirm Ollama is listening on the default API port:

```bash
ss -ltnp | grep 11434 || true
ollama ps
```

If you need to run a model directly:

```bash
ollama run llama3
```

## Running the Streamlit apps

Start the uploader (index documents):

```bash
./venv/bin/streamlit run app_file_uploader.py
```

Start the QA chat interface from the project root:

```bash
./venv/bin/streamlit run interface/app_qa.py
```

If Streamlit prints `gio: http://localhost:8501: Operation not supported` on WSL, open the Local URL manually in your browser.

## Configuration and storage

- `config_data.py` defines:
  - `persist_directory` — where ChromaDB stores vectors (default: `chroma_db/`)
  - `md5_path` — `history/md5.txt` used to deduplicate uploads
  - chunking settings used by `knowledge_base.py`
- `chat_history/` stores conversation JSON files locally and is excluded from Git.
- `history/` stores upload deduplication data locally and is excluded from Git.

## Project structure

- `app_file_uploader.py` — Streamlit uploader & indexer
- `interface/app_qa.py` — Streamlit chat frontend with multi-user, multi-session history
- `knowledge_base.py` — parsing, splitting and Chroma ingestion
- `vector_stores.py` — Chroma vector store helper
- `file_history_store.py` — local JSON chat history
- `rag.py` — RAG pipeline wiring with LangChain + Ollama

## Notes & Troubleshooting

- If you see "failed to connect to Ollama", ensure:
  - Ollama is installed and the API is running (`ollama ps`).
  - Required models have been pulled (`ollama pull ...`).
- The chat UI supports local user profiles rather than account authentication. Do not use it as a security boundary for untrusted users.
- To verify Python imports in the venv:

```bash
./venv/bin/python -c "import streamlit, langchain, langchain_ollama, chromadb, bs4, docx, pypdf; print('import-ok')"
```

## Support

I can:

- Add a `requirements.txt` for reproducible installs.
- Create a short `SHUTDOWN.md` checklist to stop apps and save terminal history.

---
Last updated: 2026-08-13