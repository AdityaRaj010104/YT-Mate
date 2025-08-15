
from transcript_extraction import extract_transcript_with_lang_choice
from text_splitter import split_text
from embedding_generation import generate_and_store_embeddings  # import your function

url = input("Enter YouTube video URL: ")

try:
    # Step 1: Extract transcript and join all text
    transcript = extract_transcript_with_lang_choice(url)
    joined_text = " ".join(entry.text for entry in transcript)  # flatten into single string

    # Step 2: Split text into chunks using RecursiveCharacterTextSplitter
    chunks = split_text(joined_text)

    print(f"\n--- Split into {len(chunks)} chunks ---\n")
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Chunk {idx}:\n{chunk.page_content}\n{'-'*50}")

    # Step 3: Generate embeddings & store in FAISS vector store
    vector_store = generate_and_store_embeddings(chunks)

    if vector_store:
        print("✅ Embeddings generated and stored successfully.")

except Exception as e:
    print(f"Error: {e}")


# from transcript_extraction import extract_transcript_with_lang_choice
# from text_splitter import split_text  # your splitter function

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

# except Exception as e:
#     print(f"Error: {e}")

