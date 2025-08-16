from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def retrieve_from_vectorstore(query, vectorstore_path="faiss_index", k=4):
    """
    Retrieves the most relevant chunks from a stored FAISS vector store.

    Args:
        query (str): The user query to search against the vector store.
        vectorstore_path (str): Path to the saved FAISS index.
        k (int): Number of top results to retrieve.

    Returns:
        list: A list of matching documents (LangChain Document objects).
    """
    try:
        # Load embeddings object (same as used during storage)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Load the existing FAISS index
        vector_store = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

        # Create retriever
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})

        # Retrieve results
        results = retriever.invoke(query)

        return results

    except Exception as e:
        print(f"❌ Error during retrieval: {e}")
        return []
