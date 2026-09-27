# app.py
import streamlit as st
from rag import rag_answer

st.set_page_config(page_title="Notes RAG Chatbot", page_icon="📚")

st.title("📚 Notes RAG Chatbot")
st.caption("Ask a question — I'll search your notes and answer using only what's actually in them.")

# Keep the conversation in memory for this session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Redraw the full conversation so far, every time the page reruns
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            st.caption(f"Sources: {', '.join(msg['sources'])} (confidence: {msg['score']:.2f})")

# The input box at the bottom of the page
question = st.chat_input("Ask something about your notes...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your notes..."):
            answer, source_files, score = rag_answer(question)
        st.write(answer)
        if source_files:
            st.caption(f"Sources: {', '.join(source_files)} (confidence: {score:.2f})")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": source_files,
        "score": score
    })