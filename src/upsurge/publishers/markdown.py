from __future__ import annotations
from pathlib import Path
from ..content.base import ContentElement
from ..content.page import Page


class MarkdownPublisher:
    def __init__(self, include_toc: bool = True, toc_title: str = "Table of Contents"):
        self.include_toc = include_toc
        self.toc_title = toc_title

    def publish(self, report, output_path: str) -> None:
        content = self.render(report)
        Path(output_path).write_text(content, encoding="utf-8")

    def render(self, report) -> str:
        lines = []

        lines.append(f"# {report.title}")
        lines.append("")

        if report.author:
            lines.append(f"*Author: {report.author}*")
            lines.append("")
        if report.description:
            lines.append(f"*{report.description}*")
            lines.append("")

        if self.include_toc:
            lines.append(f"## {self.toc_title}")
            lines.append("")
            for i, page in enumerate(report.pages):
                if page.toc_entry:
                    page_ref = f"#{page.id}" if page.id else f"#page-{i + 1}"
                    lines.append(f"- [{page.title}]({page_ref})")
            lines.append("")
            lines.append("---")
            lines.append("")

        for i, page in enumerate(report.pages):
            lines.append(self._render_page(page, i))
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def _render_page(self, page: Page, index: int) -> str:
        lines = []

        if page.id:
            lines.append(f"<a id='{page.id}'></a>")
        lines.append(f"## {page.title}")
        lines.append("")

        for element in page.content:
            md = self._render_element(element)
            if md:
                lines.append(md)
                lines.append("")

        for section in page.sections:
            lines.append(section.to_markdown())
            lines.append("")

        return "\n".join(lines)

    def _render_element(self, element: ContentElement) -> str:
        if hasattr(element, "to_markdown"):
            return element.to_markdown()
        return str(element)
