
import hashlib
import os
import config_data as config
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str):
    if not os.path.exists(config.md5_path):
        # 确保目录存在
        os.makedirs(os.path.dirname(config.md5_path), exist_ok=True)
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        with open(config.md5_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if md5_str == line.strip():
                    return True
    return False


def save_md5(md5_str: str):
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    str_bytes = input_str.encode(encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    return md5_obj.hexdigest()


class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.embeddings = OllamaEmbeddings(
            model='bge-m3'
        )

        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embeddings,  
            persist_directory=config.persist_directory
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )

    def upload_by_str(self, data: str, filename):
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[skip]"


        knowledge_chunks = self.spliter.split_text(data)


        metadatas = [{
            "source": filename,
            "created_at": str(datetime.now()),  
            "operator": "lawson",
        } for _ in knowledge_chunks]

        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=metadatas,
        )

        save_md5(md5_hex)
        return "[success]"

