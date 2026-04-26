import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)


def extract_video_id(url: str) -> str | None:
    patterns = [
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def clean_transcript(transcript_list) -> str:
    text_parts = []

    for entry in transcript_list:
        # ✅ supports both dict and object formats
        text = getattr(entry, "text", None)

        if text is None and isinstance(entry, dict):
            text = entry.get("text", "")

        if not text:
            continue

        text = re.sub(r"\[.*?\]", "", text).strip()

        if text:
            text_parts.append(text)

    return " ".join(text_parts)


def fetch_transcript(url: str) -> dict:
    video_id = extract_video_id(url)

    if not video_id:
        return {
            "success": False,
            "error": "Invalid YouTube URL. Please provide a valid YouTube link."
        }

    try:
        # ✅ Correct v1.x approach
        transcript_list = YouTubeTranscriptApi().fetch(video_id)

        transcript_text = clean_transcript(transcript_list)
        word_count = len(transcript_text.split())

        return {
            "success": True,
            "video_id": video_id,
            "transcript": transcript_text,
            "word_count": word_count,
            "language": "en"
        }

    except TranscriptsDisabled:
        return {
            "success": False,
            "error": "Captions are disabled for this video."
        }

    except NoTranscriptFound:
        return {
            "success": False,
            "error": "No transcript found for this video."
        }

    except VideoUnavailable:
        return {
            "success": False,
            "error": "Video is unavailable or private."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }