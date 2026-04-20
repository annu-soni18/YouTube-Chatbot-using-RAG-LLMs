import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_youtube_id(url):

    pattern = r"(?:v=|youtu\.be/|embed/|shorts/)([^&?/]+)"
    match = re.search(pattern, url)

    return match.group(1) if match else None


def get_transcript(video_id):

    api = YouTubeTranscriptApi()

    transcript = api.fetch(
        video_id=video_id,
        languages=["en", "hi"]
    )

    text = " ".join(t.text for t in transcript.snippets)

    return text