from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    google_gemini_key: str
    model_name: str = "gemini-2.5-flash-lite"
    output_root: str = "outputs"
    max_words_per_chunk: int = 1800
    temperature: float = 0.3


def load_settings() -> Settings:
    load_dotenv()

    api_key = os.getenv("GOOGLE_GEMINI_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "Missing GOOGLE_GEMINI_KEY in environment. Add it to .env before running."
        )

    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite").strip()
    output_root = os.getenv("OUTPUT_ROOT", "outputs").strip() or "outputs"
    max_words_per_chunk = int(os.getenv("MAX_WORDS_PER_CHUNK", "1800"))
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))

    return Settings(
        google_gemini_key=api_key,
        model_name=model_name,
        output_root=output_root,
        max_words_per_chunk=max_words_per_chunk,
        temperature=temperature,
    )
