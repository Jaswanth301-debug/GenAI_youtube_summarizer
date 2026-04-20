from __future__ import annotations

import google.generativeai as genai

from .text_utils import extract_json_object


class GeminiClient:
    def __init__(self, api_key: str, model_name: str, temperature: float = 0.3) -> None:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={"temperature": temperature},
        )

    def generate_json(self, prompt: str) -> dict:
        response = self.model.generate_content(prompt)
        text = (response.text or "").strip()
        return extract_json_object(text)
