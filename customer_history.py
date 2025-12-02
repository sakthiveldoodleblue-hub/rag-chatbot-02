import streamlit as st
from db import init_collections
from langchain_google_genai import ChatGoogleGenerativeAI

def handle_customer_history(question, llm):
    collections = init_collections()
    
    # Simple keyword extraction
    customer_id = st.text_input("🔍 Enter Customer ID/Name/Email:")
    if customer_id:
        customer = collections['customers'].find_one({
            "$or": [
                {"name": {"$regex": customer_id, "$options": "i"}},
                {"customer_id": customer_id},
                {"email": {"$regex": customer_id, "$options": "i"}}
            ]
        })
        
        if customer:
            txns = list(collections['transactions'].find(
                {"customer_id": customer["customer_id"]}
            ).sort("date_of_purchase", -1).limit(10))
            
            total_spent = sum(t.get("total_amount", 0) for t in txns)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Spent", f"${total_spent:.2f}")
            with col2:
                st.metric("Transactions", len(txns))
            
            st.dataframe(txns)
            return f"Found {len(txns)} transactions for {customer['name']}"
        else:
            return "❌ Customer not found"
    
    return "Please enter customer details above"
