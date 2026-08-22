import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(PROJECT_DIR, "chroma_db")
HISTORY_DIR = os.path.join(PROJECT_DIR, "history")
MD5_PATH = os.path.join(HISTORY_DIR, "md5.txt")

os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

collection_name = "rag_collection"
persist_directory = PERSIST_DIRECTORY
md5_path = MD5_PATH
chunk_size = 500
chunk_overlap = 50
separators = ["\n\n", "\n", " ", ""]
similarity_threshold = 3

session_config = {"configurable": {"session_id": "default"}}
