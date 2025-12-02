import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TokenCounter:
    def __init__(self):
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.encoding = None

    def count_tokens(self, text: str) -> int:
        if self.encoding:
            return len(self.encoding.encode(text))
        return len(text) // 4

token_counter = TokenCounter()

def mongodb_to_searchable_text(transactions_collection):
    transactions = list(transactions_collection.find())
    if not transactions:
        raise ValueError("No transactions found in MongoDB")

    texts = []
    for txn in transactions:
        texts.append(f"""
Transaction:
Invoice: {txn.get("invoice_number")}
Customer: {txn.get("customer_name")} (ID: {txn.get("customer_id")})
Product: {txn.get("product_name")} (Category: {txn.get("category")})
Quantity: {txn.get("quantity")}
Total: ${txn.get("total_amount"):.2f}
Date: {txn.get("date_of_purchase")}
Payment Mode: {txn.get("payment_mode")}
Status: {txn.get("status")}
""")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_text("\n".join(texts))
    return chunks
