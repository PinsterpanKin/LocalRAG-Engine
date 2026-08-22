#file_history_store.py
import os
import json
from datetime import datetime
from urllib.parse import quote, unquote
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_DIRECTORY = os.path.join(PROJECT_DIR, "chat_history")


def _history_path(session_id):
    safe_session_id = quote(str(session_id), safe="")
    return os.path.join(HISTORY_DIRECTORY, f"{safe_session_id}.json")


def get_history(session_id):
    os.makedirs(HISTORY_DIRECTORY, exist_ok=True)
    return FileChatMessageHistory(_history_path(session_id))


def list_sessions(user_id):
    """Return saved sessions for one user, newest first."""
    os.makedirs(HISTORY_DIRECTORY, exist_ok=True)
    prefix = f"{quote(str(user_id), safe='')}__"
    sessions = []

    for filename in os.listdir(HISTORY_DIRECTORY):
        if not filename.startswith(prefix) or not filename.endswith(".json"):
            continue

        encoded_session_id = filename[len(prefix):-5]
        session_id = unquote(encoded_session_id)
        history = FileChatMessageHistory(os.path.join(HISTORY_DIRECTORY, filename))
        messages = history.messages
        user_messages = [message.content for message in messages if message.type == "human"]
        title = user_messages[0][:42].strip() if user_messages else "New conversation"
        sessions.append({
            "session_id": session_id,
            "title": title or "New conversation",
            "updated_at": datetime.fromtimestamp(
                os.path.getmtime(os.path.join(HISTORY_DIRECTORY, filename))
            ),
        })

    return sorted(sessions, key=lambda item: item["updated_at"], reverse=True)


def delete_session(user_id, session_id):
    """Delete one persisted conversation without affecting other users."""
    file_path = _history_path(f"{user_id}__{session_id}")
    if os.path.isfile(file_path):
        os.remove(file_path)


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