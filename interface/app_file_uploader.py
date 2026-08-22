import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from services.knowledge_base import KnowledgeBaseService, parse_text_from_bytes

SUPPORTED_TYPES = ['txt', 'md', 'pdf', 'html', 'htm', 'docx']

st.title('Data Base Updating Service')
st.write('Upload `.txt`, `.md`, `.pdf`, `.html`, or `.docx` files to add them to the local vector store.')

uploader_file = st.file_uploader(
    'Please upload a supported document:',
    type=SUPPORTED_TYPES,
    accept_multiple_files=False,
)
if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()

if "counter" not in st.session_state:
    st.session_state["counter"] = 0

if uploader_file is not None:
    file_name=uploader_file.name
    file_type=uploader_file.type
    file_size=uploader_file.size/1024#KB

    st.subheader(f'{file_name}')
    st.write(f'type: {file_type}, size: {file_size:.2f} KB')

    try:
        file_bytes = uploader_file.getvalue()
        text = parse_text_from_bytes(file_bytes, file_name)
        if not text.strip():
            st.error('Unable to extract text from this file. Please try another document.')
        else:
            st.session_state['counter'] += 1
            result = st.session_state['service'].upload_by_str(text, file_name)
            st.success(result)
    except ValueError as exc:
        st.error(str(exc))
    except ImportError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f'Upload failed: {exc}')
