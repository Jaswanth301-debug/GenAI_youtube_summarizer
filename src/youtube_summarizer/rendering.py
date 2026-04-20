from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    import markdown as md_lib
except ModuleNotFoundError:
    md_lib = None


def markdown_to_html(markdown_text: str) -> str:
    if md_lib is not None:
        return md_lib.markdown(
            markdown_text,
            extensions=["extra", "sane_lists", "toc"],
            output_format="html5",
        )

    lines = markdown_text.splitlines()
    html_parts: list[str] = []
    in_list = False
    for line in lines:
        striped = line.strip()
        if striped.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h3>{striped[4:]}</h3>")
        elif striped.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h2>{striped[3:]}</h2>")
        elif striped.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h1>{striped[2:]}</h1>")
        elif striped.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{striped[2:]}</li>")
        elif striped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<p>{striped}</p>")
    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def render_full_page(
    template_dir: Path,
    article_title: str,
    seo_description: str,
    body_html: str,
    source_url: str,
) -> str:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(enabled_extensions=("html",)),
    )
    template = env.get_template("article_page.html")
    return template.render(
        article_title=article_title,
        seo_description=seo_description,
        body_html=body_html,
        source_url=source_url,
    )
