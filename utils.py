from src.youtube_summarizer.text_utils import clean_transcript_text
from src.youtube_summarizer.youtube import extract_video_id, fetch_transcript_text


def get_video_id(url: str) -> str:
    return extract_video_id(url)


def get_transcript(url: str, language: str = "en") -> str:
    video_id = extract_video_id(url)
    raw_text = fetch_transcript_text(video_id=video_id, language=language)
    return clean_transcript_text(raw_text)
