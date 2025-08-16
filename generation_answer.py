from langchain_google_genai import ChatGoogleGenerativeAI

def generate_answer_from_prompt(final_prompt):
    """
    Sends the final prompt string to Gemini LLM and returns the response.

    Args:
        final_prompt (str): The prompt string including context + question

    Returns:
        str: LLM-generated answer
    """
    try:
        # Instantiate Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # lightweight Gemini model
            temperature=0.2
        )

        # Call the LLM with the prompt
        response = llm.invoke(final_prompt)

        return response.content

    except Exception as e:
        print(f"❌ Error generating answer from Gemini: {e}")
        return "Error occurred while generating answer."
