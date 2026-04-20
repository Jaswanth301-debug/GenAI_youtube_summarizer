from __future__ import annotations


def chunk_summary_prompt(chunk: str, chunk_index: int, chunk_count: int) -> str:
    return f"""
You are an expert analyst.
Summarize transcript chunk {chunk_index}/{chunk_count}.

Rules:
- Keep facts tied to transcript only.
- Ignore filler and repeated phrases.
- Return strict JSON only.

Schema:
{{
  "chunk_summary": "string",
  "key_points": ["string", "..."],
  "themes": ["string", "..."]
}}

Transcript chunk:
{chunk}
""".strip()


def final_summary_prompt(chunk_summaries: str) -> str:
    return f"""
You are creating a compact executive summary from multiple transcript chunk summaries.
Return strict JSON only.

Schema:
{{
  "title": "string",
  "compact_summary": "2-4 short paragraphs",
  "key_points": ["string", "..."],
  "themes": ["string", "..."],
  "decisions_or_recommendations": ["string", "..."],
  "action_items": ["string", "..."],
  "confidence_notes": "mention uncertainty if any"
}}

Chunk summaries:
{chunk_summaries}
""".strip()


def article_prompt(summary_json: str, source_url: str) -> str:
    return f"""
Transform the structured summary into an article that is publication-ready.
The audience is marketing and content teams.
Use clear narrative flow and practical takeaways.
Do not hallucinate facts.
Return strict JSON only.

Schema:
{{
  "article_title": "string",
  "seo_description": "max 160 chars",
  "tags": ["string", "..."],
  "markdown": "full markdown article with H1/H2/H3 and bullet lists where useful"
}}

Must include:
- A concise introduction
- 3 to 6 topical sections
- A section called "Practical Applications for Marketing Teams"
- A short conclusion
- Reference line for source URL at the end

Source URL: {source_url}
Summary JSON:
{summary_json}
""".strip()
