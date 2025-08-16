from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

def generate_and_store_embeddings(chunks, vectorstore_path="faiss_index"):
    """
    Generates embeddings for text chunks using Gemini embeddings
    and stores them in a FAISS vector store.

    Args:
        chunks (list): List of LangChain Document objects from split_text()
        vectorstore_path (str): Directory path to save the FAISS index

    Returns:
        FAISS: The in-memory FAISS vector store object
    """
    try:
        # Create embeddings object using Gemini
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",  # Gemini embedding model
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Create FAISS vector store from documents
        vector_store = FAISS.from_documents(chunks, embeddings)

        # Save the vector store locally
        vector_store.save_local(vectorstore_path)
        print(f"✅Embedding generated and Vector store saved to '{vectorstore_path}'")

        return vector_store

    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return None
