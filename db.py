import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_mongodb_connection():
    """Establish MongoDB Atlas connection using Streamlit secrets"""
    MONGODB_URI = st.secrets.get("MONGODB_URI", "")
    DB_NAME = st.secrets.get("DB_NAME", "rag_chatbot_db")
    
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI not found in Streamlit secrets")
    
    client = MongoClient(MONGODB_URI)
    client.admin.command('ping')  # Test connection
    st.success("✓ Connected to MongoDB Atlas")
    return client[DB_NAME]

# Initialize collections once
@st.cache_resource
def init_collections():
    db = get_mongodb_connection()
    return {
        "transactions": db["transactions"],
        "products": db["products"],
        "customers": db["customers"],
        "support_tickets": db["support_tickets"]
    }
