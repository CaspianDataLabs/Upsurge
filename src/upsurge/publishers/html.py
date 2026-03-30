from __future__ import annotations
from pathlib import Path
from typing import Optional
from ..content.base import ContentElement
from ..content.page import Page


class HTMLPublisher:
    def __init__(
        self,
        css: Optional[str] = None,
        template: Optional[str] = None,
        include_toc: bool = True,
    ):
        self.css = css
        self.template = template
        self.include_toc = include_toc

    def publish(self, report, output_path: str) -> None:
        content = self.render(report)
        Path(output_path).write_text(content, encoding="utf-8")

    def render(self, report) -> str:
        html_parts = []

        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html lang='en'>")
        html_parts.append("<head>")
        html_parts.append(f"<title>{report.title}</title>")
        html_parts.append("<meta charset='UTF-8'>")
        html_parts.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_parts.append("<style>")
        if self.css:
            html_parts.append(self.css)
        else:
            html_parts.append(self._get_default_css())
        html_parts.append("</style>")
        html_parts.append("</head>")
        html_parts.append("<body>")

        html_parts.append("<header>")
        html_parts.append(f"<h1>{report.title}</h1>")
        if report.author:
            html_parts.append(f"<p class='author'>By {report.author}</p>")
        if report.description:
            html_parts.append(f"<p class='description'>{report.description}</p>")
        html_parts.append("</header>")

        if self.include_toc:
            html_parts.append(self._render_toc(report))

        html_parts.append("<main>")
        for i, page in enumerate(report.pages):
            html_parts.append(self._render_page(page, i))
        html_parts.append("</main>")

        html_parts.append("<footer>")
        html_parts.append("<p>Generated with Upsurge</p>")
        html_parts.append("</footer>")

        html_parts.append("</body>")
        html_parts.append("</html>")

        return "\n".join(html_parts)

    def _render_toc(self, report) -> str:
        html = ["<nav class='toc'>"]
        html.append("<h2>Table of Contents</h2>")
        html.append("<ul>")
        for i, page in enumerate(report.pages):
            if page.toc_entry:
                page_ref = f"#{page.id}" if page.id else f"#page-{i + 1}"
                html.append(f'<li><a href="{page_ref}">{page.title}</a></li>')
        html.append("</ul>")
        html.append("</nav>")
        return "\n".join(html)

    def _render_page(self, page: Page, index: int) -> str:
        html = [f'<article id="{page.id or f"page-{index + 1}"}" class="page">']

        if page.title:
            html.append('<div class="page-header">')
            html.append(f"<h2>{page.title}</h2>")
            html.append("</div>")

        for element in page.content:
            html.append(self._render_element(element))

        for section in page.sections:
            html.append(section.to_html())

        html.append("</article>")
        return "\n".join(html)

    def _render_element(self, element: ContentElement) -> str:
        if hasattr(element, "to_html"):
            return element.to_html()
        return f"<p>{element}</p>"

    def _get_default_css(self) -> str:
        return """
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    color: #333;
}
header {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #eee;
}
h1 { color: #2c3e50; }
h2, h3, h4 { color: #34495e; }
.author { font-style: italic; color: #7f8c8d; }
.description { color: #95a5a6; }
.toc {
    background: #f8f9fa;
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 5px;
}
.toc ul { list-style: none; padding-left: 0; }
.toc li { margin: 5px 0; }
.toc a { text-decoration: none; color: #3498db; }
.toc a:hover { text-decoration: underline; }
.page { margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
.page-header h2 { margin-top: 0; }
img { max-width: 100%; height: auto; }
table { border-collapse: collapse; width: 100%; margin: 20px 0; }
th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
th { background-color: #f8f9fa; }
.caption { font-style: italic; color: #7f8c8d; text-align: center; }
footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #7f8c8d; }
"""
