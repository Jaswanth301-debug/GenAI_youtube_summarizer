from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VideoInput:
    url: str
    language: str = "en"
    prefer_generated: bool = True


@dataclass
class VideoMetadata:
    video_id: str
    url: str
    title: str | None = None
    author_name: str | None = None
    thumbnail_url: str | None = None


@dataclass
class SummaryPayload:
    title: str
    compact_summary: str
    key_points: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    decisions_or_recommendations: list[str] = field(default_factory=list)
    action_items: list[str] = field(default_factory=list)
    confidence_notes: str = ""
    raw_model_output: dict[str, Any] = field(default_factory=dict)


@dataclass
class ArticlePayload:
    article_title: str
    markdown: str
    seo_description: str
    tags: list[str] = field(default_factory=list)
    raw_model_output: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineOutput:
    metadata: VideoMetadata
    transcript_text: str
    transcript_chunks: list[str]
    summary: SummaryPayload
    article: ArticlePayload
    output_dir: str
    json_path: str
    markdown_path: str
    html_path: str
