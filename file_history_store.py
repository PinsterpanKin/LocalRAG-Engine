#file_history_store.py
import os
import json
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory


def get_history(session_id):
    directory = "chat_history"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f"{session_id}.json")
    return FileChatMessageHistory(file_path)


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, file_path):
        self.file_path = file_path
        parent_dir = os.path.dirname(self.file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

    @property
    def messages(self):
        if not os.path.exists(self.file_path) or os.path.isdir(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_messages(self, messages):
        current_messages = self.messages
        current_messages.extend(messages)

        messages_dict = [message_to_dict(m) for m in current_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(messages_dict, f, ensure_ascii=False, indent=2)

    def clear(self):
        if os.path.exists(self.file_path):
            if os.path.isdir(self.file_path):
                import shutil
                shutil.rmtree(self.file_path)
            else:
                os.remove(self.file_path)
