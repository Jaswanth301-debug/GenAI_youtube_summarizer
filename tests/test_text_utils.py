from src.youtube_summarizer.text_utils import clean_transcript_text, slugify, split_by_words


def test_clean_transcript_text_compacts_whitespace() -> None:
    raw = "Hello   world \n\n this is   a test"
    assert clean_transcript_text(raw) == "Hello world this is a test"


def test_split_by_words() -> None:
    text = "one two three four five"
    assert split_by_words(text, max_words=2) == ["one two", "three four", "five"]


def test_slugify() -> None:
    assert slugify("Hello, World!") == "hello-world"
