# import re
# from youtube_transcript_api import YouTubeTranscriptApi


# def extract_youtube_id(url):

#     pattern = r"(?:v=|youtu\.be/|embed/|shorts/)([^&?/]+)"
#     match = re.search(pattern, url)

#     return match.group(1) if match else None


# def get_transcript(video_id):

#     api = YouTubeTranscriptApi()

#     transcript = api.fetch(
#         video_id=video_id,
#         languages=["en", "hi"]
#     )

#     text = " ".join(t.text for t in transcript.snippets)

#     return text










# Backend/youtube_utils.py

import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig


def extract_youtube_id(url):

    pattern = r"(?:v=|youtu\.be/|embed/|shorts/)([^&?/]+)"
    match = re.search(pattern, url)

    return match.group(1) if match else None


def get_transcript(video_id):

    proxy_user = os.environ.get("PROXY_USER")
    proxy_pass = os.environ.get("PROXY_PASS")

    if proxy_user and proxy_pass:
        proxy_config = WebshareProxyConfig(
            proxy_username=proxy_user,
            proxy_password=proxy_pass,
        )
        api = YouTubeTranscriptApi(proxy_config=proxy_config)
    else:
        api = YouTubeTranscriptApi()  # works locally, blocked on Render

    transcript = api.fetch(
        video_id=video_id,
        languages=["en", "hi"]
    )

    text = " ".join(t.text for t in transcript.snippets)

    return text