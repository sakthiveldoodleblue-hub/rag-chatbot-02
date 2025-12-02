import streamlit as st
import os
from db import init_collections
from upload import upload_json_to_mongodb
from rag_model import build_rag_model
from search_db import handle_search_db
from customer_history import handle_customer_history
from support import handle_support_request
from utils import token_counter

st.set_page_config(page_title="E-commerce Chatbot", layout="wide")

def main():
    st.title("🛍️ E-commerce Sales & Support Chatbot")
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    try:
        collections = init_collections()
    except Exception as e:
        st.error(f"Database connection error: {e}")
        st.info("Please configure MONGODB_URI in Streamlit secrets")
        return
    
    # Model initialization
    if not st.session_state.get("models_ready", False):
        st.info("📊 Ready to upload sales data")
        json_file = st.file_uploader("Upload sales JSON data", type=["json"])
        
        if json_file:
            try:
                with st.spinner("Uploading and processing data..."):
                    temp_file = "temp.json"
                    with open(temp_file, "wb") as f:
                        f.write(json_file.getbuffer())
                    
                    uploaded_count = upload_json_to_mongodb(temp_file, collections)
                    st.success(f"✅ Uploaded {uploaded_count} transactions")
                    
                    # Clean up
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    
                    # Build RAG model
                    api_key = st.secrets.get("GOOGLE_API_KEY")
                    if not api_key:
                        st.error("GOOGLE_API_KEY not found in secrets")
                        return
                    
                    qa_chain, llm, intent_classifier = build_rag_model(
                        api_key, 
                        collections["transactions"]
                    )
                    
                    st.session_state.models_ready = True
                    st.session_state.qa_chain = qa_chain
                    st.session_state.llm = llm
                    st.session_state.intent_classifier = intent_classifier
                    
                    st.rerun()
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                return
    
    # Chatbot interface
    if st.session_state.get("models_ready", False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask me about products, sales, or support:",
                placeholder="e.g., Show top selling products, What did customer John buy?"
            )
        
        with col2:
            if st.button("🔄 Clear History"):
                st.session_state.chat_history = []
                st.rerun()
        
        if user_input:
            try:
                intent, conf = st.session_state.intent_classifier.classify(user_input)
                
                with st.expander(f"🎯 Intent: {intent} (Confidence: {conf:.2f})"):
                    pass
                
                with st.spinner("Processing..."):
                    if intent == "SEARCH_DB":
                        answer = handle_search_db(
                            user_input,
                            st.session_state.qa_chain,
                            st.session_state.chat_history
                        )
                    elif intent == "CUSTOMER_HISTORY":
                        answer = handle_customer_history(
                            user_input,
                            st.session_state.llm,
                            collections
                        )
                    elif intent == "SUPPORT":
                        answer = handle_support_request()
                    else:
                        answer = "Sorry, I couldn't understand your request. Please try again."
                
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": answer,
                    "intent": intent
                })
                
                st.write(answer)
                
                tokens = token_counter.count_tokens(answer)
                st.caption(f"📊 Tokens used: {tokens}")
            
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
    
    # Display chat history
    if st.session_state.get("chat_history"):
        st.divider()
        st.subheader("📝 Chat History")
        for i, msg in enumerate(st.session_state.chat_history, 1):
            with st.expander(f"Q{i}: {msg['user'][:50]}..."):
                st.write(f"**Answer:** {msg['bot']}")
                st.caption(f"Intent: {msg['intent']}")

if __name__ == "__main__":
    main()
