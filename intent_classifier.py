import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingIntentClassifier:
    def __init__(self, embeddings_model):
        self.embeddings_model = embeddings_model
        self.intent_templates = {
            "SEARCH_DB": [
                "What products do you have?",
                "Show me sales data",
                "How many items sold?",
                "What is the price of product?",
                "List all products in category",
                "Show inventory",
                "What are the top selling products?",
                "Total sales amount",
                "How much revenue?",
                "Product information",
                "Category details",
                "Stock availability",
                "Product pricing",
                "Sales statistics",
                "Business analytics"
            ], 
            "CUSTOMER_HISTORY": [
                 "Show my purchase history",
                "What did I buy?",
                "My previous orders",
                "My transaction history",
                "Orders for customer John Doe",
                "Show transactions for customer ID",
                "My account purchases",
                "What have I ordered before?",
                "My past invoices",
                "Show my receipts",
                "Customer order history",
                "My shopping history",
                "Previous purchases",
                "Order history for email",
                "Track my orders"
            ],
            "SUPPORT": ["I have a problem",
                "Need help with my order",
                "Product is broken",
                "Issue with delivery",
                "Customer service needed",
                "Contact support team",
                "File a complaint",
                "Not working properly",
                "Report an issue",
                "Need assistance",
                "Something went wrong",
                "Call customer care",
                "Urgent help required",
                "Refund request",
                "Product defect"
                ]
        }
        print("\n🧠 Pre-computing intent template embeddings...")
        self.intent_embeddings = {}
        for intent, templates in self.intent_templates.items():
            embeddings = self.embeddings_model.embed_documents(templates)
            self.intent_embeddings[intent] = np.mean(embeddings, axis=0)

    def classify(self, question):
        question_embedding = self.embeddings_model.embed_query(question)
        sims = {intent: cosine_similarity([question_embedding], [embed])[0][0]
                for intent, embed in self.intent_embeddings.items()}
        best_intent = max(sims, key=sims.get)
        return best_intent, sims[best_intent]
