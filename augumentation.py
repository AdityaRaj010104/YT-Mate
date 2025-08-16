def build_augmented_prompt(retriever, question):
    """
    Builds an augmented prompt by combining the user query with
    retrieved transcript context for use in an LLM.

    Args:
        retriever: LangChain retriever object
        question (str): The user's question

    Returns:
        str: The final prompt string ready to send to the LLM
    """
    from langchain.prompts import PromptTemplate

    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)

    # Combine all retrieved chunks into one context string
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Define the prompt template
    prompt = PromptTemplate(
        template=(
            "You are a helpful assistant.\n"
            "Answer ONLY from the provided transcript context.\n"
            "If the context is insufficient, just say you don't know.\n\n"
            "{context}\n"
            "Question: {question}"
        ),
        input_variables=['context', 'question']
    )

    # Fill in the template
    final_prompt = prompt.format(context=context_text, question=question)

    return final_prompt
