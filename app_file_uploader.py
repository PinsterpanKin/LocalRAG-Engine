#app_file_uploader
import streamlit as st
from knowledge_base import KnowledgeBaseService
st.title("data bases updating service")
uploader_file=st.file_uploader(
    "please upload txt files",
    type=['txt'],
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

    st.subheader(f"{file_name}")
    st.write(f"type:{file_type},size:{file_size:.2f}")

    text=uploader_file.getvalue().decode("utf-8")

    st.session_state["counter"]+=1
    result=st.session_state["service"].upload_by_str(text,file_name)
    st.write(result)
