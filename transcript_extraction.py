
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# Function to extract video ID from full URL
from urllib.parse import urlparse, parse_qs

def get_video_id(url: str) -> str | None:
    """
    Extracts the video ID from a YouTube URL.
    Works with normal, shortened, and embed links.
    Returns None if no valid video ID is found.
    """
    parsed_url = urlparse(url)

    # Case 1: Short URL (youtu.be/VIDEO_ID)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    # Case 2: Standard YouTube URL (youtube.com/watch?v=VIDEO_ID)
    if parsed_url.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        if parsed_url.path == "/watch":
            query_params = parse_qs(parsed_url.query)
            return query_params.get("v", [None])[0]
        # Case 3: Embed URL (youtube.com/embed/VIDEO_ID)
        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]
        # Case 4: /v/VIDEO_ID format
        if parsed_url.path.startswith("/v/"):
            return parsed_url.path.split("/")[2]

    return None

def extract_transcript(url: str, languages=None):
    """Fetches transcript text for a given YouTube URL."""
    video_id = get_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript = YouTubeTranscriptApi().fetch(video_id,languages=languages or ['en'])
    return transcript


# url = input("Enter YouTube video URL: ")

# video_id = get_video_id(url)

# if video_id:
#     try:
#         transcript = YouTubeTranscriptApi().fetch(video_id)
#         print("\n--- Transcript ---\n")
#         for entry in transcript:
#             print(f"{entry.start:.2f}s: {entry.text}")
#     except Exception as e:
#         print(f"Error: {e}")
# else:
#     print("Invalid YouTube URL")


