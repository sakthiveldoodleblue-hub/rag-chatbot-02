from datetime import datetime
from pathlib import Path
import json
import streamlit as st

def upload_json_to_mongodb(json_file_path: str, collections) -> int:
    """Upload and parse JSON file into MongoDB collections"""
    
    if not Path(json_file_path).exists():
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both list and dict formats
        documents = data if isinstance(data, list) else [data]
        
        # Limit to 100 documents for initial testing
        documents = documents[:100]
        
        if not documents:
            raise ValueError("No documents found in JSON file")
        
        # Initialize storage dicts
        customers_dict = {}
        products_dict = {}
        transactions = []
        
        # Process each document
        for doc in documents:
            try:
                # Extract customer data
                cid = str(doc.get("Customer ID", "UNKNOWN")).strip()
                if cid and cid not in customers_dict:
                    customers_dict[cid] = {
                        "customer_id": cid,
                        "name": str(doc.get("Customer name", "Unknown")).strip(),
                        "email": str(doc.get("Email", "N/A")).strip(),
                        "phone": str(doc.get("Phone", "N/A")).strip(),
                        "city": str(doc.get("City", "N/A")).strip(),
                        "loyalty_tier": str(doc.get("Loyalty_Tier", "Regular")).strip(),
                        "created_at": datetime.now()
                    }
                
                # Extract product data
                pid = str(doc.get("ID_product", "UNKNOWN")).strip()
                if pid and pid not in products_dict:
                    products_dict[pid] = {
                        "product_id": pid,
                        "name": str(doc.get("Product", "Unknown")).strip(),
                        "category": str(doc.get("Category", "N/A")).strip(),
                        "sku": str(doc.get("SKUs", "N/A")).strip(),
                        "cogs": float(doc.get("COGS", 0)) if doc.get("COGS") else 0,
                        "margin_percent": float(doc.get("Margin_per_piece_percent", 0)) 
                                        if doc.get("Margin_per_piece_percent") else 0,
                        "created_at": datetime.now()
                    }
                
                # Extract transaction data
                transactions.append({
                    "invoice_number": str(doc.get("Invoice Number", "N/A")).strip(),
                    "txn_number": str(doc.get("Txn_No", "N/A")).strip(),
                    "customer_id": cid,
                    "customer_name": str(doc.get("Customer name", "Unknown")).strip(),
                    "product_id": pid,
                    "product_name": str(doc.get("Product", "Unknown")).strip(),
                    "category": str(doc.get("Category", "N/A")).strip(),
                    "quantity": int(doc.get("Quantity_piece", 0)) if doc.get("Quantity_piece") else 0,
                    "gross_amount": float(doc.get("Gross_Amount", 0)) if doc.get("Gross_Amount") else 0,
                    "discount_percentage": float(doc.get("Discount_Percentage", 0)) 
                                          if doc.get("Discount_Percentage") else 0,
                    "total_amount": float(doc.get("Total Amount", 0)) if doc.get("Total Amount") else 0,
                    "gst": float(doc.get("GST", 0)) if doc.get("GST") else 0,
                    "payment_mode": str(doc.get("Payment_mode", "N/A")).strip(),
                    "date_of_purchase": str(doc.get("Date_of_purchase", datetime.now().isoformat())).strip(),
                    "channel": str(doc.get("Channel", "N/A")).strip(),
                    "store_location": str(doc.get("Store_location", "N/A")).strip(),
                    "mode": str(doc.get("Mode", "N/A")).strip(),
                    "status": "completed",
                    "created_at": datetime.now()
                })
            
            except Exception as e:
                print(f"Warning: Error processing document: {str(e)}")
                continue
        
        # Clear existing data
        collections["customers"].delete_many({})
        collections["products"].delete_many({})
        collections["transactions"].delete_many({})
        
        # Insert data into MongoDB
        if customers_dict:
            collections["customers"].insert_many(list(customers_dict.values()))
        
        if products_dict:
            collections["products"].insert_many(list(products_dict.values()))
        
        if transactions:
            result = collections["transactions"].insert_many(transactions)
            return len(result.inserted_ids)
        
        return 0
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise Exception(f"Error uploading data: {str(e)}")
