import streamlit as st

def handle_search_db(question, qa_chain, chat_history):
    """Handle database search using RAG chain"""
    
    try:
        # Prepare chat history in the required format
        formatted_history = []
        for item in chat_history[-5:]:  # Use last 5 exchanges for context
            if isinstance(item, dict):
                formatted_history.append((item.get("user", ""), item.get("bot", "")))
        
        # Invoke RAG chain
        result = qa_chain.invoke({
            "question": question,
            "chat_history": formatted_history
        })
        
        # Extract answer
        answer = result.get("answer", "No data found").strip()
        
        # Display source documents
        source_docs = result.get("source_documents", [])
        if source_docs:
            with st.expander("📚 Source Documents", expanded=False):
                for i, doc in enumerate(source_docs, 1):
                    content = doc.page_content[:400]
                    st.write(f"**Document {i}:**")
                    st.text(content)
                    if len(doc.page_content) > 400:
                        st.caption("... (truncated)")
                    st.divider()
        
        return answer
    
    except Exception as e:
        error_msg = f"Error during search: {str(e)}"
        st.error(error_msg)
        return error_msg
