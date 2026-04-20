from __future__ import annotations

import json
from pathlib import Path

from .config import Settings
from .models import ArticlePayload, PipelineOutput, SummaryPayload, VideoInput
from .prompts import article_prompt, chunk_summary_prompt, final_summary_prompt
from .rendering import markdown_to_html, render_full_page
from .storage import create_run_dir, write_artifacts
from .text_utils import clean_transcript_text, split_by_words
from .youtube import extract_video_id, fetch_transcript_text, fetch_video_metadata


def _list_str(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(v).strip() for v in value if str(v).strip()]


def _build_summary_payload(raw: dict) -> SummaryPayload:
    return SummaryPayload(
        title=str(raw.get("title", "Video Summary")).strip() or "Video Summary",
        compact_summary=str(raw.get("compact_summary", "")).strip(),
        key_points=_list_str(raw.get("key_points", [])),
        themes=_list_str(raw.get("themes", [])),
        decisions_or_recommendations=_list_str(raw.get("decisions_or_recommendations", [])),
        action_items=_list_str(raw.get("action_items", [])),
        confidence_notes=str(raw.get("confidence_notes", "")).strip(),
        raw_model_output=raw,
    )


def _build_article_payload(raw: dict) -> ArticlePayload:
    return ArticlePayload(
        article_title=str(raw.get("article_title", "Generated Article")).strip()
        or "Generated Article",
        markdown=str(raw.get("markdown", "")).strip(),
        seo_description=str(raw.get("seo_description", "")).strip(),
        tags=_list_str(raw.get("tags", [])),
        raw_model_output=raw,
    )


def run_pipeline(video: VideoInput, settings: Settings) -> PipelineOutput:
    from .llm import GeminiClient

    video_id = extract_video_id(video.url)
    metadata = fetch_video_metadata(video_id)

    transcript = fetch_transcript_text(
        video_id=video_id,
        language=video.language,
        prefer_generated=video.prefer_generated,
    )
    transcript = clean_transcript_text(transcript)
    chunks = split_by_words(transcript, max_words=settings.max_words_per_chunk)
    if not chunks:
        raise ValueError("Transcript is empty after preprocessing.")

    llm = GeminiClient(
        api_key=settings.google_gemini_key,
        model_name=settings.model_name,
        temperature=settings.temperature,
    )

    chunk_summaries: list[dict] = []
    for i, chunk in enumerate(chunks, start=1):
        prompt = chunk_summary_prompt(chunk=chunk, chunk_index=i, chunk_count=len(chunks))
        chunk_summaries.append(llm.generate_json(prompt))

    summary_prompt = final_summary_prompt(json.dumps(chunk_summaries, ensure_ascii=True, indent=2))
    summary_raw = llm.generate_json(summary_prompt)
    summary = _build_summary_payload(summary_raw)

    article_req_prompt = article_prompt(
        summary_json=json.dumps(summary.raw_model_output, ensure_ascii=True, indent=2),
        source_url=video.url,
    )
    article_raw = llm.generate_json(article_req_prompt)
    article = _build_article_payload(article_raw)
    if not article.markdown:
        raise ValueError("Article generation returned empty markdown.")

    template_dir = Path(__file__).resolve().parent / "templates"
    body_html = markdown_to_html(article.markdown)
    full_html = render_full_page(
        template_dir=template_dir,
        article_title=article.article_title,
        seo_description=article.seo_description,
        body_html=body_html,
        source_url=video.url,
    )

    title_hint = metadata.title or summary.title or "youtube-summary"
    run_dir = create_run_dir(settings.output_root, title_hint)
    json_path, md_path, html_path = write_artifacts(
        run_dir=run_dir,
        metadata=metadata,
        transcript_text=transcript,
        summary=summary,
        article=article,
        full_html=full_html,
    )

    return PipelineOutput(
        metadata=metadata,
        transcript_text=transcript,
        transcript_chunks=chunks,
        summary=summary,
        article=article,
        output_dir=str(run_dir),
        json_path=str(json_path),
        markdown_path=str(md_path),
        html_path=str(html_path),
    )
