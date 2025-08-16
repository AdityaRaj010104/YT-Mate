from transcript_extraction import extract_transcript_with_lang_choice
from text_splitter import split_text
from embedding_generation import generate_and_store_embeddings
from retriever import retrieve_from_vectorstore
from dotenv import load_dotenv

load_dotenv()

def main():
    url = input("Enter YouTube video URL: ")

    try:
        # Step 1: Extract transcript
        transcript = extract_transcript_with_lang_choice(url)
        joined_text = " ".join(entry.text for entry in transcript)

        # Step 2: Split into chunks
        chunks = split_text(joined_text)
        print(f"✅ Split into {len(chunks)} chunks")

        # Step 3: Generate embeddings & store in FAISS
        vector_store = generate_and_store_embeddings(chunks)

        # Step 4: Ask user query for retrieval
        query = input("\nEnter your question: ")
        results = retrieve_from_vectorstore(query)

        # print("\n🔎 Retrieved Results:")
        # for i, doc in enumerate(results, start=1):
        #     print(f"\nResult {i}:\n{doc.page_content}\n{'-'*50}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()





# from transcript_extraction import extract_transcript_with_lang_choice
# from text_splitter import split_text
# from embedding_generation import generate_and_store_embeddings
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import os
# from dotenv import load_dotenv

# load_dotenv()

# url = input("Enter YouTube video URL: ")

# try:
#     # Step 1: Extract transcript and join all text
#     transcript = extract_transcript_with_lang_choice(url)
#     joined_text = " ".join(entry.text for entry in transcript)  # flatten into single string

#     # Step 2: Split text into chunks using RecursiveCharacterTextSplitter
#     chunks = split_text(joined_text)

#     print(f"\n--- Split into {len(chunks)} chunks ---\n")
#     for idx, chunk in enumerate(chunks, start=1):
#         print(f"Chunk {idx}:\n{chunk.page_content}\n{'-'*50}")

#     # Step 3: Generate embeddings & store in FAISS vector store
#     vector_store = generate_and_store_embeddings(chunks)

#     if vector_store:
#         print("✅ Embeddings generated and stored successfully.")
#         print(vector_store.index_to_docstore_id)

#         # Step 4: Create retriever (change search_type to "mmr" if needed)
#         retriever = vector_store.as_retriever(
#             search_type="similarity",   # or "mmr"
#             search_kwargs={"k": 4}      # number of results
#         )

#         print("✅ Retriever created successfully.")

# except Exception as e:
#     print(f"Error: {e}")
