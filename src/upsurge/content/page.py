from __future__ import annotations
from dataclasses import dataclass, field
from .base import ContentElement
from .section import Section


@dataclass
class Page:
    id: str = ""
    title: str = ""
    content: list[ContentElement] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    toc_entry: bool = True

    def add_content(self, element: ContentElement) -> Page:
        self.content.append(element)
        return self

    def add_section(self, section: Section) -> Page:
        self.sections.append(section)
        return self

    def to_markdown(self) -> str:
        lines = []

        if self.title:
            anchor = f"{{#{self.id}}}" if self.id else ""
            lines.append(f"## {self.title}{anchor}")
            lines.append("")

        for element in self.content:
            md = element.to_markdown()
            if md:
                lines.append(md)
                lines.append("")

        for section in self.sections:
            lines.append(section.to_markdown())
            lines.append("")

        return "\n".join(lines)

    def to_html(self) -> str:
        html_parts = []

        if self.title:
            html_parts.append(f'<div class="page-header" id="{self.id}">')
            html_parts.append(f"<h1>{self.title}</h1>")
            html_parts.append("</div>")

        for element in self.content:
            html = element.to_html()
            if html:
                html_parts.append(html)

        for section in self.sections:
            html_parts.append(section.to_html())

        return "\n".join(html_parts)
