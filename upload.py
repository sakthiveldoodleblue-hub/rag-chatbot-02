from datetime import datetime
from pathlib import Path
import json

def upload_json_to_mongodb(json_file_path: str, collections) -> int:
    """Upload JSON file to MongoDB Atlas collections"""
    if not Path(json_file_path).exists():
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    documents = data if isinstance(data, list) else [data]
    documents = documents[:100]

    # Clear existing data if user confirms (done in app.py UI)
    customers_dict, products_dict, transactions = {}, {}, []
    
    for doc in documents:
        # Customer
        cid = doc.get("Customer ID", "UNKNOWN")
        if cid not in customers_dict:
            customers_dict[cid] = {
                "customer_id": cid,
                "name": doc.get("Customer name", "Unknown"),
                "email": doc.get("Email", "N/A"),
                "phone": doc.get("Phone", "N/A"),
                "city": doc.get("City", "N/A"),
                "loyalty_tier": doc.get("Loyalty_Tier", "Regular"),
                "created_at": datetime.now()
            }
        # Product
        pid = doc.get("ID_product", "UNKNOWN")
        if pid not in products_dict:
            products_dict[pid] = {
                "product_id": pid,
                "name": doc.get("Product", "Unknown"),
                "category": doc.get("Category", "N/A"),
                "sku": doc.get("SKUs", "N/A"),
                "cogs": doc.get("COGS", 0),
                "margin_percent": doc.get("Margin_per_piece_percent", 0),
                "created_at": datetime.now()
            }
        # Transaction
        transactions.append({
            "invoice_number": doc.get("Invoice Number", "N/A"),
            "txn_number": doc.get("Txn_No", "N/A"),
            "customer_id": cid,
            "customer_name": doc.get("Customer name", "Unknown"),
            "product_id": pid,
            "product_name": doc.get("Product", "Unknown"),
            "category": doc.get("Category", "N/A"),
            "quantity": doc.get("Quantity_piece", 0),
            "gross_amount": doc.get("Gross_Amount", 0),
            "discount_percentage": doc.get("Discount_Percentage", 0),
            "total_amount": doc.get("Total Amount", 0),
            "gst": doc.get("GST", 0),
            "payment_mode": doc.get("Payment_mode", "N/A"),
            "date_of_purchase": doc.get("Date_of_purchase", datetime.now().isoformat()),
            "channel": doc.get("Channel", "N/A"),
            "store_location": doc.get("Store_location", "N/A"),
            "mode": doc.get("Mode", "N/A"),
            "status": "completed",
            "created_at": datetime.now()
        })
    
    # Insert data
    collections["customers"].insert_many(list(customers_dict.values()))
    collections["products"].insert_many(list(products_dict.values()))
    result = collections["transactions"].insert_many(transactions)
    return len(result.inserted_ids)
