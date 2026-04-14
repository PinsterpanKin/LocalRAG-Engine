#rag.py
from vector_stores import VectorStoreService
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history


class RagService:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model='bge-m3')
        self.model = OllamaLLM(model="llama3")
        self.vector_service = VectorStoreService(embedding=self.embeddings)

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "according to the contexts that are offered by me "
                           "answer the question professionally and concisely. contexts:{context}."),
                ("placeholder", "{history}"),
                ("user", "answer the question:{input}."),
            ]
        )
        self.chat_model = self.model
        self.chain = self._get_chain()

    def _get_chain(self):
        retriever = self.vector_service.get_retriever()

        def extract_input(value):
            if isinstance(value, dict):
                return value.get("input", "")
            return str(value)

        def format_document(docs: list[Document]):
            if not docs: return "No documents found"
            return "\n\n".join([f"page:{doc.page_content}" for doc in docs])

        def format_for_prompt_template(value):
            return {
                "input": value["input"],
                "context": value["context"],
                "history": value.get("history", [])  
            }

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(extract_input) | retriever | format_document,
                    "history": RunnablePassthrough()
                }
                | RunnableLambda(format_for_prompt_template)
                | self.prompt_template
                | self.chat_model
                | StrOutputParser()
        )

        return RunnableWithMessageHistory(
            chain,
            get_history,
            input_message_key="input",
            history_message_key="history",
        )


if __name__ == "__main__":
    session_config = {"configurable": {"session_id": "001"}}
    # 确保传入的是标准的字典格式
    res = RagService().chain.invoke({"input": "why is it dangerous "}, session_config)
    print(res)
