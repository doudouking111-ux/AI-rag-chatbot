"""RAG 核心：文档解析 → 切分 → 向量化 → 检索问答"""

import os, fitz, docx
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import Document

load_dotenv()


def parse_file(uploaded_file) -> list[Document]:
    """解析 PDF/Word，返回 Document 列表（保留来源元数据）"""
    name = uploaded_file.name
    raw = uploaded_file.read()
    docs = []

    if name.endswith(".pdf"):
        with fitz.open(stream=raw, filetype="pdf") as pdf:
            for i, page in enumerate(pdf):
                text = page.get_text()
                if text.strip():
                    docs.append(Document(page_content=text, metadata={"source": name, "page": i + 1}))
    elif name.endswith((".docx", ".doc")):
        import io
        doc = docx.Document(io.BytesIO(raw))
        # 每 10 段合并为一个 chunk，避免太碎
        buf, start = [], 1
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                buf.append(para.text)
            if len(buf) >= 10:
                docs.append(Document(page_content="\n".join(buf), metadata={"source": name, "section": f"段落{start}-{i+1}"}))
                buf, start = [], i + 2
        if buf:
            docs.append(Document(page_content="\n".join(buf), metadata={"source": name, "section": f"段落{start}-{len(doc.paragraphs)}"}))

    return docs


def build_vectorstore(docs: list[Document]) -> FAISS:
    """切分 + 向量化，返回 FAISS 向量库"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80, separators=["\n\n", "\n", "。", ".", " "])
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return FAISS.from_documents(chunks, embeddings)


def create_chain(vectorstore: FAISS) -> ConversationalRetrievalChain:
    """创建带记忆的 RAG 问答链"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True, output_key="answer")
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        memory=memory,
        return_source_documents=True,
        verbose=False,
    )
