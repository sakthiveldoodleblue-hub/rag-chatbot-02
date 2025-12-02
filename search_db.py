import streamlit as st
from langchain.chains import ConversationalRetrievalChain

def handle_search_db(question, qa_chain, chat_history):
    result = qa_chain.invoke({"question": question, "chat_history": chat_history})
    answer = result.get("answer", "No data found")
    
    with st.expander("📎 Source Documents"):
        for i, doc in enumerate(result.get("source_documents", []), 1):
            st.write(f"**Doc {i}:** {doc.page_content[:300]}...")
    
    return answer
