import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TokenCounter:
    """Count tokens using tiktoken for accurate token usage"""
    
    def __init__(self):
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.encoding = None

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            if self.encoding:
                return len(self.encoding.encode(text))
            # Fallback: rough estimation (1 token ≈ 4 characters)
            return len(text) // 4
        except Exception:
            return len(text) // 4

token_counter = TokenCounter()

def mongodb_to_searchable_text(transactions_collection):
    """Convert MongoDB transactions to searchable text chunks"""
    
    try:
        transactions = list(transactions_collection.find().limit(200))
        
        if not transactions:
            raise ValueError("No transactions found in MongoDB")
        
        # Create searchable text from transactions
        texts = []
        for txn in transactions:
            text = f"""
Transaction Details:
Invoice Number: {txn.get("invoice_number", "N/A")}
Transaction Number: {txn.get("txn_number", "N/A")}
Customer: {txn.get("customer_name", "Unknown")} (ID: {txn.get("customer_id", "N/A")})
Email: {txn.get("customer_email", "N/A") if "customer_email" in txn else "N/A"}
Product: {txn.get("product_name", "Unknown")} (ID: {txn.get("product_id", "N/A")})
Category: {txn.get("category", "N/A")}
Quantity Purchased: {txn.get("quantity", 0)} units
Gross Amount: ${txn.get("gross_amount", 0):.2f}
Discount: {txn.get("discount_percentage", 0)}%
Total Amount: ${txn.get("total_amount", 0):.2f}
GST: ${txn.get("gst", 0):.2f}
Payment Mode: {txn.get("payment_mode", "N/A")}
Purchase Date: {txn.get("date_of_purchase", "N/A")}
Channel: {txn.get("channel", "N/A")}
Store Location: {txn.get("store_location", "N/A")}
Status: {txn.get("status", "N/A")}
"""
            texts.append(text)
        
        # Split text into chunks for better retrieval
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = splitter.split_text("\n".join(texts))
        
        if not chunks:
            raise ValueError("No chunks created from transactions")
        
        return chunks
    
    except Exception as e:
        print(f"Error converting MongoDB to searchable text: {str(e)}")
        raise
