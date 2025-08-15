def get_retriever(vectorstore_path="faiss_index", k=4):
    """
    Loads a FAISS vector store from local storage and returns a retriever.

    Args:
        vectorstore_path (str): Path to the saved FAISS index directory
        k (int): Number of similar results to retrieve

    Returns:
        BaseRetriever: A retriever object for similarity search
    """
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import os
    from dotenv import load_dotenv

    load_dotenv()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    vector_store = FAISS.load_local(
        vectorstore_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
