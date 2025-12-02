import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

def get_mongodb_connection():
    """Establish MongoDB Atlas connection using Streamlit secrets"""
    try:
        MONGODB_URI = st.secrets.get("MONGODB_URI") or os.getenv("MONGODB_URI")
        DB_NAME = st.secrets.get("DB_NAME", "rag_chatbot_db")
        
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI not found in Streamlit secrets or environment")
        
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        st.success("✓ Connected to MongoDB Atlas")
        return client[DB_NAME]
    
    except ConnectionFailure as e:
        st.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

@st.cache_resource
def init_collections():
    """Initialize database collections with indexes"""
    db = get_mongodb_connection()
    
    collections = {
        "transactions": db["transactions"],
        "products": db["products"],
        "customers": db["customers"],
        "support_tickets": db["support_tickets"]
    }
    
    # Create indexes for faster queries
    collections["customers"].create_index("customer_id", unique=True)
    collections["products"].create_index("product_id", unique=True)
    collections["transactions"].create_index("customer_id")
    collections["support_tickets"].create_index("ticket_number", unique=True)
    
    return collections
