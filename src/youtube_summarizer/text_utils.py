from __future__ import annotations

import json
import re
from typing import Any


def clean_transcript_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(" [Music] ", " ")
    return text


def split_by_words(text: str, max_words: int) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i : i + max_words]))
    return chunks


def slugify(value: str) -> str:
    lowered = value.lower().strip()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-") or "untitled"


def extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()

    first = text.find("{")
    last = text.rfind("}")
    if first == -1 or last == -1 or last <= first:
        raise ValueError("Model output does not contain a JSON object.")

    candidate = text[first : last + 1]
    return json.loads(candidate)
