#app_file_uploader
import streamlit as st
from knowledge_base import KnowledgeBaseService
#添加标题
st.title("知识库更新服务")
#文件上传服务
uploader_file=st.file_uploader(
    "上传txt文件",
    type=['txt'],
    accept_multiple_files=False,#仅接受上传一个文件
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
    st.write(f"格式:{file_type},大小:{file_size:.2f}")

#获取内容
    text=uploader_file.getvalue().decode("utf-8")

    st.session_state["counter"]+=1
    result=st.session_state["service"].upload_by_str(text,file_name)
    st.write(result)