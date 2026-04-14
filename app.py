"""RAG 文档问答 Demo — Streamlit 前端"""

import streamlit as st
from rag import parse_file, build_vectorstore, create_chain

st.set_page_config(page_title="📄 RAG 文档问答", layout="wide")
st.title("📄 RAG 文档问答 Demo")

# --- 侧边栏：上传文档 ---
with st.sidebar:
    st.header("上传文档")
    files = st.file_uploader("支持 PDF / Word", type=["pdf", "docx", "doc"], accept_multiple_files=True)

    if files and st.button("🔨 解析并构建索引"):
        with st.spinner("解析文档 + 构建向量索引..."):
            all_docs = []
            for f in files:
                all_docs.extend(parse_file(f))
            if not all_docs:
                st.error("未从文档中提取到文本")
            else:
                st.session_state.vectorstore = build_vectorstore(all_docs)
                st.session_state.chain = create_chain(st.session_state.vectorstore)
                st.session_state.messages = []
                st.success(f"✅ 索引完成，共 {len(all_docs)} 个文档片段")

# --- 主区域：对话 ---
if "chain" not in st.session_state:
    st.info("👈 请先在左侧上传文档并构建索引")
    st.stop()

# 显示历史消息
for msg in st.session_state.get("messages", []):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if question := st.chat_input("输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            result = st.session_state.chain.invoke({"question": question})
            answer = result["answer"]

            # 拼接引用来源
            sources = result.get("source_documents", [])
            if sources:
                refs = set()
                for doc in sources:
                    m = doc.metadata
                    loc = f"第{m['page']}页" if "page" in m else m.get("section", "")
                    refs.add(f"📎 {m['source']} {loc}")
                answer += "\n\n---\n**引用来源：**\n" + "\n".join(f"- {r}" for r in refs)

            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
