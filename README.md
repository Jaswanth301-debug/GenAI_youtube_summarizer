# YouTube Summarizer + Article Generator

A complete Generative-AI pipeline that:

1. Parses a YouTube URL
2. Pulls transcript text
3. Summarizes transcript into structured insights
4. Converts summary into a publication-ready article
5. Exports artifacts as JSON, Markdown, and standalone HTML page

## Why this project

This project addresses information overload from long-form YouTube content by turning raw transcripts into concise summaries and reusable article-style webpages. It is practical for marketing, documentation, and knowledge-reuse workflows.

## Features

- Transcript extraction using `youtube-transcript-api`
- Chunked summarization for long videos
- Structured summary output (`key points`, `themes`, `action items`)
- Article generation in Markdown with sectioned narrative flow
- HTML rendering using Jinja2 template
- CLI mode and Streamlit UI mode
- Artifact persistence per run

## Project structure

```text
.
|-- app.py
|-- main.py
|-- utils.py
|-- requirements.txt
|-- .env
|-- src/
|   `-- youtube_summarizer/
|       |-- config.py
|       |-- llm.py
|       |-- models.py
|       |-- pipeline.py
|       |-- prompts.py
|       |-- rendering.py
|       |-- storage.py
|       |-- text_utils.py
|       |-- youtube.py
|       `-- templates/article_page.html
`-- tests/
```

## Setup

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` and set key:

```env
GOOGLE_GEMINI_KEY=your_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash-lite
```

## Run (CLI)

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Optional flags:

- `--language en`
- `--prefer-manual`

## Run (Streamlit)

```bash
streamlit run app.py
```

## Outputs

Each run writes a timestamped folder under `outputs/`:

- `result.json` (structured output)
- `article.md` (markdown article)
- `article.html` (ready webpage)

## Tests

```bash
pytest -q
```

## Notes

- Some videos do not provide transcripts; the pipeline raises a clear error in that case.
- For reliable production behavior, pin a model via `GEMINI_MODEL_NAME`.
