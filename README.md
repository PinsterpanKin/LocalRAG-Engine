# Local RAG System: Retrieval-Augmented Generation

This is a localized **RAG (Retrieval-Augmented Generation)** system built with **LangChain**, **Streamlit**, and **Ollama**. It allows you to upload private text documents and chat with them using local Large Language Models (LLMs), ensuring total data privacy.

## 👀 1.Project Overview

### 🌟 Key Features
*   **Knowledge Base Management**: Upload `.txt` `.md` `.pdf` `.html` `.docx` files to create a searchable local vector database[cite: 1, 4].
*   **Intelligent Retrieval**: Uses the `bge-m3` embedding model to find the most relevant context for your questions[cite: 4, 6].
*   **Context-Aware Chat**: Powered by `llama3`, the system answers questions based specifically on your uploaded documents[cite: 5].
*   **Persistent Memory**: Chat history is saved locally in JSON format, allowing the AI to remember previous parts of the conversation[cite: 3].
*   **MD5 Deduplication**: Automatically skips files that have already been processed to save time and storage[cite: 4].

### 🛠️ Tech Stack
*   **Core Framework**: LangChain
*   **User Interface**: Streamlit
*   **Vector Database**: ChromaDB
*   **Local LLM Engine**: Ollama (Llama3 & BGE-M3)
*   **Programming Language**: Python

### 🚀 Quick Start

#### 1. Prerequisites
Install [Ollama](https://ollama.com/) and download the required models:
```bash
ollama pull llama3
ollama pull bge-m3
```

## 📥 2.Installation

### Clone the repo
git clone <our-link>
cd <your-folder>

### Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

### Install requirements
pip install streamlit langchain langchain-ollama langchain-chroma langchain-community langchain-text-splitters

## 💻 3.Running the App

*   **Step 1: Upload Documents**
    Run the uploader to index your knowledge, you can type following command on Linux:
```bash
streamlit run app_file_uploader.py
```   

*   **Step 2: Start Chatting**
    Open the QA interface to interact with your data:
```bash
streamlit run app_qa.py
```

## 📁 Current Project Structure
*   `app_file_uploader.py`: UI for uploading and processing text files[cite: 1].
*   `app_qa.py`: Main chat interface for the AI service[cite: 2].
*   `rag.py`: The core RAG logic and LangChain pipeline[cite: 5].
*   `knowledge_base.py`: Handles text splitting and vector embedding[cite: 4].
*   `vector_stores.py`: Manages the connection to the Chroma vector store[cite: 6].
*   `file_history_store.py`: Manages saving and loading chat history from local files[cite: 3].

## 🛡️ About License
This project is for educational purposes. More previous examples with different focus are  
available on GitHub, so just feel free to use and modify it for your own local AI 
experiments.

---
*Last updated: May 2nd 2026*