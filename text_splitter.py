

from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(transcript):
    """
    Splits the transcript text into chunks.

    Args:
        transcript (str): The text to be split.

    Returns:
        list: A list of Document objects containing the text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.create_documents([transcript])
    return chunks


# Run only if file is executed directly
if __name__ == "__main__":
    sample_text = """Your transcript text goes here..."""
    result_chunks = split_text(sample_text)

    for i, chunk in enumerate(result_chunks, start=1):
        print(f"Chunk {i}:\n{chunk.page_content}\n{'-'*50}")
