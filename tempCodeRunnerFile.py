from transcript_extraction import extract_transcript_with_lang_choice

url = input("Enter YouTube video URL: ")

try:
    transcript = extract_transcript_with_lang_choice(url)

    print("\n--- Transcript ---\n")
    print(transcript)  # plain joined string
except Exception as e:
    print(f"Error: {e}")