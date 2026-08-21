import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from file_history_store import delete_session, get_history, list_sessions
from rag import RagService

st.set_page_config(
    page_title="Local RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { border-right: 1px solid rgba(128, 128, 128, .2); }
    .welcome { padding: 1.5rem 0 1rem; }
    .welcome h1 { margin-bottom: .35rem; }
    .session-note { color: #777; font-size: .85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
def new_session_id():
    return str(uuid.uuid4())


def load_messages(history_key):
    history_messages = get_history(history_key).messages
    messages = []
    for message in history_messages:
        if isinstance(message, HumanMessage):
            messages.append({"role": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            messages.append({"role": "assistant", "content": message.content})
    return messages


if "user_id" not in st.session_state:
    st.session_state.user_id = "local-user"
if "session_id" not in st.session_state:
    st.session_state.session_id = new_session_id()
if "loaded_history_key" not in st.session_state:
    st.session_state.loaded_history_key = None
if "rag" not in st.session_state:
    st.session_state.rag = RagService()
with st.sidebar:
    st.title("🧠 Local RAG")
    st.caption("Private document chat, powered by Ollama")

    st.subheader("👤 User profile")
    user_id = st.text_input(
        "User name",
        value=st.session_state.user_id,
        max_chars=40,
        help="Use a different name to keep each user's conversations separate.",
    ).strip()
    user_id = user_id or "local-user"
    if user_id != st.session_state.user_id:
        st.session_state.user_id = user_id
        st.session_state.session_id = new_session_id()
        st.session_state.loaded_history_key = None
        st.rerun()

    st.subheader("💬 Conversations")
    if st.button("➕ New conversation", use_container_width=True):
        st.session_state.session_id = new_session_id()
        st.session_state.loaded_history_key = None
        st.rerun()

    saved_sessions = list_sessions(st.session_state.user_id)
    session_ids = [item["session_id"] for item in saved_sessions]
    if session_ids:
        selected_index = session_ids.index(st.session_state.session_id) if st.session_state.session_id in session_ids else 0
        selected_session = st.selectbox(
            "Saved sessions",
            options=session_ids,
            index=selected_index,
            format_func=lambda session_id: next(
                item["title"] for item in saved_sessions if item["session_id"] == session_id
            ),
            label_visibility="collapsed",
        )
        if selected_session != st.session_state.session_id:
            st.session_state.session_id = selected_session
            st.session_state.loaded_history_key = None
            st.rerun()
    else:
        st.caption("No saved conversations yet.")

    if st.button("🗑️ Clear current history", use_container_width=True):
        delete_session(st.session_state.user_id, st.session_state.session_id)
        st.session_state.loaded_history_key = None
        st.session_state.session_id = new_session_id()
        st.rerun()

    st.divider()
    with st.expander("📖 How to use", expanded=True):
        st.markdown(
            """
            1. Open `app_file_uploader.py` and upload a document.
            2. Return here and ask questions about the indexed content.
            3. Use **New conversation** to start a separate thread.
            4. Change **User name** to switch user workspaces.

            Supported files: `.txt`, `.md`, `.pdf`, `.html`, `.docx`.
            """
        )

    with st.expander("⚙️ System status"):
        st.caption("Models: `bge-m3` embeddings, `llama3` chat")
        st.caption("Storage: local ChromaDB and JSON history")


history_key = f"{st.session_state.user_id}__{st.session_state.session_id}"
if st.session_state.loaded_history_key != history_key:
    st.session_state.messages = load_messages(history_key)
    st.session_state.loaded_history_key = history_key


if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome">
            <h1>Welcome to your local AI workspace</h1>
            <p>Ask questions about your indexed documents, keep separate conversations,
            and work privately through your local Ollama models.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Upload a document first, then start with a question such as: “What is this document about?”")
else:
    st.title("💬 Conversation")
    st.caption(f"User: {st.session_state.user_id} · Session: {st.session_state.session_id[:8]}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about your documents...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching your knowledge base..."):
            response = st.session_state.rag.chain.invoke(
                {"input": prompt},
                {"configurable": {"session_id": history_key}},
            )
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()