#------------------------------------------------USING CHAINS------------------------------------------------


from transcript_extraction import extract_transcript_with_lang_choice
from text_splitter import split_text
from embedding_generation import generate_and_store_embeddings
from retriever import retrieve_from_vectorstore
from augumentation import build_augmented_prompt
from generation_answer import generate_answer_from_prompt

from langchain_core.runnables import RunnableLambda  # Correct import
from dotenv import load_dotenv

load_dotenv()

# Define runnables using RunnableLambda (or rely on coercion if you prefer)
transcript_rl = RunnableLambda(
    lambda url: " ".join(entry.text for entry in extract_transcript_with_lang_choice(url))
)
chunk_rl = RunnableLambda(lambda text: split_text(text))
embed_rl = RunnableLambda(lambda chunks: generate_and_store_embeddings(chunks))
retrieve_rl = RunnableLambda(lambda query: retrieve_from_vectorstore(query))
augment_rl = RunnableLambda(lambda data: build_augmented_prompt(data["query"], data["docs"]))
answer_rl = RunnableLambda(lambda prompt: generate_answer_from_prompt(prompt))

# Build pipelines using the pipe operator
prep_chain = transcript_rl | chunk_rl | embed_rl

def main():
    url = input("Enter YouTube video URL: ")
    prep_chain.invoke(url)  # Prepares the FAISS index

    query = input("\nEnter your question: ")
    qa_chain = (
        retrieve_rl
        | (lambda docs: {"query": query, "docs": docs})  # auto-coerced to RunnableLambda
        | augment_rl
        | answer_rl
    )

    answer = qa_chain.invoke(query)
    print("\n🤖 Gemini Answer:\n", answer)

if __name__ == "__main__":
    main()

#---------------------------------------------WITHOUT USING CHAINS ----------------------------------------




# from transcript_extraction import extract_transcript_with_lang_choice
# from text_splitter import split_text
# from embedding_generation import generate_and_store_embeddings
# from retriever import retrieve_from_vectorstore
# from augumentation import build_augmented_prompt
# from generation_answer import generate_answer_from_prompt
# from dotenv import load_dotenv

# load_dotenv()

# def main():
#     url = input("Enter YouTube video URL: ")

#     try:
#         # Step 1: Extract transcript
#         transcript = extract_transcript_with_lang_choice(url)
#         joined_text = " ".join(entry.text for entry in transcript)

#         # Step 2: Split into chunks
#         chunks = split_text(joined_text)
#         print(f"✅ Split into {len(chunks)} chunks")

#         # Step 3: Generate embeddings & store in FAISS
#         vector_store = generate_and_store_embeddings(chunks)

#         # Step 4: Ask user query for retrieval
#         query = input("\nEnter your question: ")
#         retrieved_docs = retrieve_from_vectorstore(query)

#         # print("\n🔎 Retrieved Results:")
#         # for i, doc in enumerate(results, start=1):
#         #     print(f"\nResult {i}:\n{doc.page_content}\n{'-'*50}")
        
#         # Step 6: Augment query with retrieved docs + Gemini
#         final_prompt = build_augmented_prompt(query, retrieved_docs)
        
#         #Step 7: Generate answer using gemini
#         answer = generate_answer_from_prompt(final_prompt)
#         print("\n🤖 Gemini Answer:\n",answer)

#     except Exception as e:
#         print(f"❌ Error: {e}")


# if __name__ == "__main__":
#     main()






