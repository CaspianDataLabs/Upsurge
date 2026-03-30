from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .content.base import (
    ContentElement,
    Text,
    Image,
    Plot,
    Table,
    Link,
    PageLink,
)
from .content.section import Section
from .content.page import Page
from .publishers import MarkdownPublisher, HTMLPublisher, PDFPublisher


@dataclass
class Report:
    title: str = "Untitled Report"
    author: Optional[str] = None
    description: Optional[str] = None
    pages: list[Page] = field(default_factory=list)
    _page_map: dict[str, Page] = field(default_factory=dict, repr=False)

    def add_page(self, page: Page) -> Report:
        if page.id:
            self._page_map[page.id] = page
        self.pages.append(page)
        return self

    def get_page(self, page_id: str) -> Optional[Page]:
        return self._page_map.get(page_id)

    def to_markdown(self) -> str:
        lines = []
        lines.append(f"# {self.title}")
        lines.append("")

        if self.author:
            lines.append(f"*Author: {self.author}*")
            lines.append("")
        if self.description:
            lines.append(f"*{self.description}*")
            lines.append("")

        lines.append("## Table of Contents")
        lines.append("")
        for i, page in enumerate(self.pages):
            if page.toc_entry:
                page_ref = f"#{page.id}" if page.id else f"#page-{i + 1}"
                lines.append(f"- [{page.title}]({page_ref})")
        lines.append("")
        lines.append("---")
        lines.append("")

        for i, page in enumerate(self.pages):
            if page.id:
                lines.append(f"## {{#{page.id}}}")
            lines.append(f"# {page.title}")
            lines.append("")
            lines.append(page.to_markdown())
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def to_html(self) -> str:
        html_parts = []

        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html lang='en'>")
        html_parts.append("<head>")
        html_parts.append(f"<title>{self.title}</title>")
        html_parts.append("<meta charset='UTF-8'>")
        html_parts.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_parts.append("<style>")
        html_parts.append(self._get_default_css())
        html_parts.append("</style>")
        html_parts.append("</head>")
        html_parts.append("<body>")

        html_parts.append("<header>")
        html_parts.append(f"<h1>{self.title}</h1>")
        if self.author:
            html_parts.append(f"<p class='author'>By {self.author}</p>")
        if self.description:
            html_parts.append(f"<p class='description'>{self.description}</p>")
        html_parts.append("</header>")

        html_parts.append("<nav class='toc'>")
        html_parts.append("<h2>Table of Contents</h2>")
        html_parts.append("<ul>")
        for i, page in enumerate(self.pages):
            if page.toc_entry:
                page_ref = f"#{page.id}" if page.id else f"#page-{i + 1}"
                html_parts.append(f'<li><a href="{page_ref}">{page.title}</a></li>')
        html_parts.append("</ul>")
        html_parts.append("</nav>")

        html_parts.append("<main>")
        for i, page in enumerate(self.pages):
            html_parts.append(f'<article id="{page.id or f"page-{i + 1}"}" class="page">')
            html_parts.append(page.to_html())
            html_parts.append("</article>")
        html_parts.append("</main>")

        html_parts.append("<footer>")
        html_parts.append("<p>Generated with Upsurge</p>")
        html_parts.append("</footer>")

        html_parts.append("</body>")
        html_parts.append("</html>")

        return "\n".join(html_parts)

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
.page-header h1 { margin-top: 0; }
img { max-width: 100%; height: auto; }
table { border-collapse: collapse; width: 100%; margin: 20px 0; }
th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
th { background-color: #f8f9fa; }
.caption { font-style: italic; color: #7f8c8d; text-align: center; }
footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #7f8c8d; }
"""

    def save_markdown(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_markdown())

    def save_html(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_html())

    def save_pdf(self, path: str) -> None:
        pdf_publisher = PDFPublisher()
        pdf_publisher.publish(self, path)


def main() -> None:
    print("Upsurge - Report Generation Library")


__all__ = [
    "Report",
    "Page",
    "Section",
    "ContentElement",
    "Text",
    "Image",
    "Plot",
    "Table",
    "Link",
    "PageLink",
    "MarkdownPublisher",
    "HTMLPublisher",
    "PDFPublisher",
]
