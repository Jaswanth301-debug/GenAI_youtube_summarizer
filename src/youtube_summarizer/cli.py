from __future__ import annotations

import argparse
import json
import sys

from .config import load_settings
from .models import VideoInput
from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate summary + article webpage from a YouTube video transcript."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--language", default="en", help="Transcript language (default: en)")
    parser.add_argument(
        "--prefer-manual",
        action="store_true",
        help="Try manually uploaded subtitles first, then generated subtitles.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        settings = load_settings()
        result = run_pipeline(
            VideoInput(
                url=args.url,
                language=args.language,
                prefer_generated=not args.prefer_manual,
            ),
            settings=settings,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    summary = {
        "title": result.summary.title,
        "compact_summary": result.summary.compact_summary,
        "key_points": result.summary.key_points,
        "themes": result.summary.themes,
        "decisions_or_recommendations": result.summary.decisions_or_recommendations,
        "action_items": result.summary.action_items,
        "output_dir": result.output_dir,
        "article_md": result.markdown_path,
        "article_html": result.html_path,
        "result_json": result.json_path,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
