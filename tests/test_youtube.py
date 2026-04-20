import pytest

from src.youtube_summarizer.youtube import extract_video_id


def test_extract_video_id_standard_url() -> None:
    assert (
        extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )


def test_extract_video_id_short_url() -> None:
    assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_video_id_invalid_url() -> None:
    with pytest.raises(ValueError):
        extract_video_id("https://example.com/video")
