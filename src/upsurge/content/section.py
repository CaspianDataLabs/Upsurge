from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .base import ContentElement


@dataclass
class Section:
    title: str = ""
    level: int = 1
    id: Optional[str] = None
    content: list[ContentElement] = field(default_factory=list)
    subsections: list[Section] = field(default_factory=list)

    def add_content(self, element: ContentElement) -> Section:
        self.content.append(element)
        return self

    def add_subsection(self, section: Section) -> Section:
        section.level = self.level + 1
        self.subsections.append(section)
        return self

    def to_markdown(self, base_level: int = 1) -> str:
        lines = []

        if self.title:
            prefix = "#" * min(self.level, 6)
            section_id = f" {{#{self.id}}}" if self.id else ""
            lines.append(f"{prefix} {self.title}{section_id}")
            lines.append("")

        for element in self.content:
            md = element.to_markdown()
            if md:
                lines.append(md)
                lines.append("")

        for subsection in self.subsections:
            lines.append(subsection.to_markdown(base_level))

        return "\n".join(lines)

    def to_html(self) -> str:
        lines = []

        if self.title:
            tag = f"h{min(self.level, 6)}"
            id_attr = f' id="{self.id}"' if self.id else ""
            lines.append(f"<{tag}{id_attr}>{self.title}</{tag}>")

        for element in self.content:
            html = element.to_html()
            if html:
                lines.append(html)

        if self.subsections:
            lines.append("<div class='subsections'>")
            for subsection in self.subsections:
                lines.append(subsection.to_html())
            lines.append("</div>")

        return "\n".join(lines)

    def find_by_id(self, section_id: str) -> Optional[Section]:
        if self.id == section_id:
            return self
        for subsection in self.subsections:
            found = subsection.find_by_id(section_id)
            if found:
                return found
        return None


@dataclass
class ReportSection(Section):
    pass
