from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    CouldNotRetrieveTranscript,
    NoTranscriptFound,
    TranscriptsDisabled,
)

from .models import VideoMetadata


def extract_video_id(url: str) -> str:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()

    if "youtu.be" in host:
        video_id = parsed.path.strip("/")
        if video_id:
            return video_id

    if "youtube.com" in host:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
            if video_id:
                return video_id
        if parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/")[-1].split("/")[0]
            if video_id:
                return video_id
        if parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/")[-1].split("/")[0]
            if video_id:
                return video_id

    raise ValueError("Could not parse a valid YouTube video ID from the provided URL.")


def fetch_video_metadata(video_id: str) -> VideoMetadata:
    url = f"https://www.youtube.com/watch?v={video_id}"
    meta = VideoMetadata(video_id=video_id, url=url)
    oembed = "https://www.youtube.com/oembed"

    try:
        response = requests.get(
            oembed,
            params={"url": url, "format": "json"},
            timeout=10,
        )
        if response.ok:
            data = response.json()
            meta.title = data.get("title")
            meta.author_name = data.get("author_name")
            meta.thumbnail_url = data.get("thumbnail_url")
    except requests.RequestException:
        pass

    return meta


def fetch_transcript_text(
    video_id: str, language: str = "en", prefer_generated: bool = True
) -> str:
    api = YouTubeTranscriptApi()

    try:
        # youtube-transcript-api >= 1.x exposes instance methods (`list`/`fetch`)
        if hasattr(api, "list"):
            transcript_list = api.list(video_id)
        else:
            # Backward compatibility with older versions.
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)  # type: ignore[attr-defined]

        if prefer_generated and hasattr(transcript_list, "find_generated_transcript"):
            try:
                transcript_obj = transcript_list.find_generated_transcript([language])
            except NoTranscriptFound:
                transcript_obj = transcript_list.find_transcript([language])
            segments = transcript_obj.fetch()
        elif hasattr(transcript_list, "find_transcript"):
            try:
                transcript_obj = transcript_list.find_transcript([language])
            except NoTranscriptFound:
                transcript_obj = transcript_list.find_generated_transcript([language])
            segments = transcript_obj.fetch()
        else:
            # Defensive fallback for unexpected API surface.
            segments = api.fetch(video_id, languages=[language])

        return " ".join(getattr(chunk, "text", str(chunk)) for chunk in segments)
    except (NoTranscriptFound, TranscriptsDisabled, CouldNotRetrieveTranscript) as exc:
        raise ValueError(
            f"No usable transcript found for video '{video_id}' and language '{language}'."
        ) from exc
