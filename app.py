from __future__ import annotations

import json

import streamlit as st

from src.youtube_summarizer.config import load_settings
from src.youtube_summarizer.models import VideoInput
from src.youtube_summarizer.pipeline import run_pipeline


st.set_page_config(page_title="YouTube Summarizer", page_icon="📝", layout="wide")

st.title("YouTube Summarizer + Article Generator")
st.caption("Generate concise summaries and publishable article pages from YouTube transcripts.")

with st.sidebar:
    st.header("Options")
    language = st.text_input("Transcript language", value="en")
    prefer_manual = st.checkbox("Prefer manual subtitles first", value=False)

url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
run = st.button("Generate", type="primary")

if run:
    if not url.strip():
        st.error("Please enter a YouTube URL.")
        st.stop()

    try:
        settings = load_settings()
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    with st.spinner("Processing transcript, summary, and article..."):
        try:
            result = run_pipeline(
                VideoInput(
                    url=url.strip(),
                    language=language.strip() or "en",
                    prefer_generated=not prefer_manual,
                ),
                settings=settings,
            )
        except Exception as exc:
            st.error(f"Pipeline failed: {exc}")
            st.stop()

    st.success("Done. Artifacts were generated successfully.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Compact Summary")
        st.markdown(f"### {result.summary.title}")
        st.write(result.summary.compact_summary)
        st.markdown("#### Key Points")
        st.write(result.summary.key_points)
        st.markdown("#### Themes")
        st.write(result.summary.themes)
        st.markdown("#### Action Items")
        st.write(result.summary.action_items)

    with col2:
        st.subheader("Article (Markdown)")
        st.markdown(result.article.markdown)

    st.subheader("Artifacts")
    artifact_data = {
        "output_dir": result.output_dir,
        "json_path": result.json_path,
        "markdown_path": result.markdown_path,
        "html_path": result.html_path,
    }
    st.code(json.dumps(artifact_data, indent=2), language="json")
