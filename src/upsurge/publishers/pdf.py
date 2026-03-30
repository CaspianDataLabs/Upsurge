from __future__ import annotations
from typing import Optional
from .html import HTMLPublisher


class PDFPublisher:
    def __init__(self, css: Optional[str] = None):
        self.css = css

    def publish(self, report, output_path: str) -> None:
        from weasyprint import HTML

        html_publisher = HTMLPublisher(css=self.css)
        html_content = html_publisher.render(report)

        html_doc = HTML(string=html_content)
        html_doc.write_pdf(output_path)

    def render(self, report) -> bytes:
        from weasyprint import HTML

        html_publisher = HTMLPublisher(css=self.css)
        html_content = html_publisher.render(report)

        html_doc = HTML(string=html_content)
        return html_doc.write_pdf()
