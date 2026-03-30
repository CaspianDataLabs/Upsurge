from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
import io
import base64


@dataclass
class ContentElement(ABC):
    id: Optional[str] = None

    @abstractmethod
    def to_markdown(self) -> str:
        pass

    @abstractmethod
    def to_html(self) -> str:
        pass


@dataclass
class Text(ContentElement):
    content: str = ""
    format: str = "plain"
    style: Optional[str] = None

    def to_markdown(self) -> str:
        if self.style == "bold":
            return f"**{self.content}**"
        elif self.style == "italic":
            return f"*{self.content}*"
        elif self.style == "code":
            return f"`{self.content}`"
        return self.content

    def to_html(self) -> str:
        if self.style == "bold":
            return f"<strong>{self.content}</strong>"
        elif self.style == "italic":
            return f"<em>{self.content}</em>"
        elif self.style == "code":
            return f"<code>{self.content}</code>"
        return f"<p>{self.content}</p>"


@dataclass
class Image(ContentElement):
    path: Optional[str] = None
    url: Optional[str] = None
    alt: str = ""
    width: Optional[str] = None
    height: Optional[str] = None
    caption: Optional[str] = None

    def to_markdown(self) -> str:
        src = self.url or self.path or ""
        attrs = f' alt="{self.alt}"' if self.alt else ""
        if self.width:
            attrs += f' width="{self.width}"'
        if self.height:
            attrs += f' height="{self.height}"'

        md = f"![{self.alt}]({src})"
        if self.caption:
            md += f"\n\n*{self.caption}*"
        return md

    def to_html(self) -> str:
        src = self.url or self.path or ""
        attrs = f' alt="{self.alt}"'
        if self.width:
            attrs += f' width="{self.width}"'
        if self.height:
            attrs += f' height="{self.height}"'

        html = f'<img src="{src}"{attrs} />'
        if self.caption:
            html += f'<p class="caption">{self.caption}</p>'
        return html


@dataclass
class Plot(ContentElement):
    figure: Any = None
    caption: Optional[str] = None
    format: str = "png"
    width: Optional[int] = None
    height: Optional[int] = None

    def __post_init__(self):
        if self.figure is None:
            import matplotlib.pyplot as plt

            self.figure = plt.figure()

    def to_markdown(self) -> str:
        buf = io.BytesIO()
        self.figure.savefig(buf, format=self.format, bbox_inches="tight")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()

        src = f"data:image/{self.format};base64,{img_base64}"
        attrs = f' alt="{self.caption or "plot"}"'
        if self.width:
            attrs += f' width="{self.width}"'
        if self.height:
            attrs += f' height="{self.height}"'

        md = f"![{self.caption or 'plot'}]({src})"
        if self.caption:
            md += f"\n\n*{self.caption}*"
        return md

    def to_html(self) -> str:
        buf = io.BytesIO()
        self.figure.savefig(buf, format=self.format, bbox_inches="tight")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()

        src = f"data:image/{self.format};base64,{img_base64}"
        attrs = f' alt="{self.caption or "plot"}"'
        if self.width:
            attrs += f' width="{self.width}"'
        if self.height:
            attrs += f' height="{self.height}"'

        html = f'<img src="{src}"{attrs} />'
        if self.caption:
            html += f'<p class="caption">{self.caption}</p>'
        return html


@dataclass
class Table(ContentElement):
    data: list[list[Any]] = field(default_factory=list)
    headers: Optional[list[str]] = None
    caption: Optional[str] = None
    column_align: Optional[list[str]] = None

    def to_markdown(self) -> str:
        if not self.data:
            return ""

        lines = []

        if self.headers:
            header_line = "| " + " | ".join(str(h) for h in self.headers) + " |"
            lines.append(header_line)

            if self.column_align:
                align_parts = []
                for a in self.column_align:
                    if a == "center":
                        align_parts.append(":-:")
                    elif a == "left":
                        align_parts.append(":--")
                    elif a == "right":
                        align_parts.append("--:")
                    else:
                        align_parts.append("---")
                align_str = " | ".join(align_parts)
            else:
                align_str = " | ".join("---" for _ in self.headers)
            lines.append(f"| {align_str} |")
        else:
            first_row = self.data[0] if self.data else []
            lines.append("| " + " | ".join("---" for _ in first_row) + " |")

        for row in self.data:
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

        result = "\n".join(lines)
        if self.caption:
            result += f"\n\n*{self.caption}*"
        return result

    def to_html(self) -> str:
        if not self.data:
            return ""

        html = "<table>"
        if self.caption:
            html += f"<caption>{self.caption}</caption>"

        if self.headers:
            html += "<thead><tr>"
            for i, header in enumerate(self.headers):
                align = (
                    self.column_align[i]
                    if self.column_align and i < len(self.column_align)
                    else "left"
                )
                html += f'<th align="{align}">{header}</th>'
            html += "</tr></thead>"

        html += "<tbody>"
        for row in self.data:
            html += "<tr>"
            for i, cell in enumerate(row):
                align = (
                    self.column_align[i]
                    if self.column_align and i < len(self.column_align)
                    else "left"
                )
                html += f'<td align="{align}">{cell}</td>'
            html += "</tr>"
        html += "</tbody></table>"

        return html


@dataclass
class Link(ContentElement):
    text: str = ""
    url: str = ""
    new_tab: bool = False

    def to_markdown(self) -> str:
        return f"[{self.text}]({self.url})"

    def to_html(self) -> str:
        target = ' target="_blank"' if self.new_tab else ""
        return f'<a href="{self.url}"{target}>{self.text}</a>'


@dataclass
class PageLink(ContentElement):
    text: str = ""
    page_id: str = ""
    page_title: Optional[str] = None

    def to_markdown(self) -> str:
        if self.page_id:
            return f"[{self.text}](#{self.page_id})"
        return f"[{self.text}](#{self.page_title.lower().replace(' ', '-') if self.page_title else self.text})"

    def to_html(self) -> str:
        href = (
            f"#{self.page_id}"
            if self.page_id
            else f"#{self.page_title.lower().replace(' ', '-') if self.page_title else self.text.lower().replace(' ', '-')}"
        )
        return f'<a href="{href}">{self.text}</a>'
