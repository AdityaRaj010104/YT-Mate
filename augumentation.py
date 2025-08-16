from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def build_augmented_prompt(query, retrieved_docs):
    """
    Builds an augmented prompt by combining retrieved transcript docs
    and querying Gemini LLM for an answer.

    Args:
        query (str): User's question
        retrieved_docs (list): List of LangChain Document objects

    Returns:
        str: LLM-generated answer
    """
    try:
        # Join retrieved docs into a single context string
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        # Define the augmentation prompt
        prompt = PromptTemplate(
            template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context below.
            If the context is insufficient, respond with "I don't know".

            Transcript Context:
            {context}

            Question: {question}
            """,
            input_variables=["context", "question"]
        )

        # Instantiate Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # ✅ lightweight, fast Gemini model
            temperature=0.2
        )

        # Format the prompt with context + question
        final_prompt = prompt.format(context=context, question=query)

        # Run the LLM
        response = llm.invoke(final_prompt)

        return response.content

    except Exception as e:
        print(f"❌ Error in augmentation: {e}")
        return "Error occurred while generating answer."
