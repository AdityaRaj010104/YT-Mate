
from transcript_extraction import extract_transcript

url = input("Enter YouTube video URL: ")

try:
    transcript = extract_transcript(url,languages=['en', 'hi'])
    print("\n--- Transcript ---\n")
    for entry in transcript:
        print(f"{entry.start:.2f}s: {entry.text}")
except Exception as e:
    print(f"Error: {e}")
