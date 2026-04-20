from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import ArticlePayload, SummaryPayload, VideoMetadata
from .text_utils import slugify


def create_run_dir(output_root: str, title_hint: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = slugify(title_hint)[:80]
    run_dir = Path(output_root) / f"{ts}_{slug}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def write_artifacts(
    run_dir: Path,
    metadata: VideoMetadata,
    transcript_text: str,
    summary: SummaryPayload,
    article: ArticlePayload,
    full_html: str,
) -> tuple[Path, Path, Path]:
    payload = {
        "metadata": {
            "video_id": metadata.video_id,
            "url": metadata.url,
            "title": metadata.title,
            "author_name": metadata.author_name,
            "thumbnail_url": metadata.thumbnail_url,
        },
        "summary": {
            "title": summary.title,
            "compact_summary": summary.compact_summary,
            "key_points": summary.key_points,
            "themes": summary.themes,
            "decisions_or_recommendations": summary.decisions_or_recommendations,
            "action_items": summary.action_items,
            "confidence_notes": summary.confidence_notes,
        },
        "article": {
            "article_title": article.article_title,
            "seo_description": article.seo_description,
            "tags": article.tags,
            "markdown": article.markdown,
        },
        "transcript_word_count": len(transcript_text.split()),
    }

    json_path = run_dir / "result.json"
    md_path = run_dir / "article.md"
    html_path = run_dir / "article.html"

    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    md_path.write_text(article.markdown, encoding="utf-8")
    html_path.write_text(full_html, encoding="utf-8")
    return json_path, md_path, html_path
