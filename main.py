from transcript_extraction import extract_transcript_with_lang_choice
from text_splitter import split_text  # your splitter function

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

except Exception as e:
    print(f"Error: {e}")

# from transcript_extraction import extract_transcript_with_lang_choice

# url = input("Enter YouTube video URL: ")

# try:
#     transcript = extract_transcript_with_lang_choice(url)

#     print("\n--- Transcript ---\n")
#     # print(transcript_text)
#     for entry in transcript:
#         # Use attribute access, not dictionary keys
#         # print(f"{entry.start:.2f}s: {entry.text}")
#         joined_text = " ".join(entry.text for entry in transcript)
#         print(joined_text)

# except Exception as e:
#     print(f"Error: {e}")


