
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter

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

def get_available_languages(url: str):
    """Return list of (language_name, language_code) for a YouTube video."""
    video_id = get_video_id(url)
    transcript_list = YouTubeTranscriptApi().list(video_id)

    langs = []
    for transcript in transcript_list:
        langs.append((transcript.language, transcript.language_code))
    return video_id, langs


def fetch_transcript(video_id: str, lang_code: str):
    """Fetch transcript for a given video and language code."""
    transcript = YouTubeTranscriptApi().fetch(video_id, languages=[lang_code])
    return transcript


# def extract_transcript_with_lang_choice(url: str):
#     # Step 1: Extract video ID (using your existing get_video_id function)
#     video_id = get_video_id(url)

#     # Step 2: Get all available transcripts
#     transcript_list = YouTubeTranscriptApi().list(video_id)

#     # Step 3: Show available languages
#     print("\nAvailable languages:")
#     available_langs = {}
#     idx = 1
#     for transcript in transcript_list:
#         lang_name = transcript.language
#         lang_code = transcript.language_code
#         available_langs[idx] = lang_code
#         print(f"{idx}. {lang_name} ({lang_code})")
#         idx += 1

#     # Step 4: Ask user for choice
#     choice = int(input("\nEnter the number of your preferred language: "))
#     chosen_lang = available_langs.get(choice)
#     if not chosen_lang:
#         raise ValueError("Invalid choice")

#     # Step 5: Fetch transcript in chosen language
#     transcript = YouTubeTranscriptApi().fetch(video_id, languages=[chosen_lang])
    
#     # transcript_text = " ".join([entry['text'] for entry in transcript])

#     return transcript


