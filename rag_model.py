from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from utils import mongodb_to_searchable_text
from intent_classifier import EmbeddingIntentClassifier

def build_rag_model(api_key, transactions_collection):
    chunks = mongodb_to_searchable_text(transactions_collection)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)
    vectorstore = FAISS.from_texts(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, max_output_tokens=1500, google_api_key=api_key)

    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a helpful e-commerce customer assistant. Based on transaction data, answer:\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )
    )

    qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": qa_prompt})

    intent_classifier = EmbeddingIntentClassifier(embeddings)

    return qa_chain, llm, intent_classifier
