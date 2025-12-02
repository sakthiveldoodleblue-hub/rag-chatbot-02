import streamlit as st
from db import init_collections
from upload import upload_json_to_mongodb
from rag_model import build_rag_model
from search_db import handle_search_db
from customer_history import handle_customer_history
from support import handle_support_request
from utils import token_counter

def main():
    st.title("E-commerce Sales & Support Chatbot")

    collections = init_collections()

    if not st.session_state.get("models_ready", False):
        json_file = st.file_uploader("Upload sales JSON data", type=["json"])
        if json_file:
            with open("temp.json", "wb") as f:
                f.write(json_file.getbuffer())
            uploaded_count = upload_json_to_mongodb("temp.json", collections)
            st.success(f"Uploaded {uploaded_count} transactions.")
            
            qa_chain, llm, intent_classifier = build_rag_model(st.secrets["GOOGLE_API_KEY"], collections["transactions"])
            st.session_state.models_ready = True
            st.session_state["qa_chain"] = qa_chain
            st.session_state["llm"] = llm
            st.session_state["intent_classifier"] = intent_classifier

    if st.session_state.get("models_ready", False):
        user_input = st.text_input("Ask me about products, sales, or support")
        if user_input:
            intent, conf = st.session_state["intent_classifier"].classify(user_input)
            st.write(f"**Intent:** {intent} (Confidence: {conf:.2f})")

            if intent == "SEARCH_DB":
                answer = handle_search_db(user_input, st.session_state["qa_chain"], [])
            elif intent == "CUSTOMER_HISTORY":
                answer = handle_customer_history(user_input, st.session_state["llm"], collections["transactions"], collections["customers"])
            elif intent == "SUPPORT":
                answer = handle_support_request(collections["support_tickets"])
            else:
                answer = "Sorry, I couldn't understand your request."

            st.write(answer)
            tokens = token_counter.count_tokens(answer)
            st.caption(f"Tokens used: {tokens}")

if __name__ == "__main__":
    main()
