"""Tests for publishers."""

import tempfile
import os
from pathlib import Path
from upsurge import Report, Page
from upsurge.publishers import MarkdownPublisher, HTMLPublisher, PDFPublisher


class TestMarkdownPublisher:
    def test_publish_to_file(self):
        report = Report(title="Test Report")
        report.add_page(Page(id="intro", title="Introduction"))

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.md")
            publisher = MarkdownPublisher()
            publisher.publish(report, output_path)

            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            assert "Test Report" in content

    def test_render_without_toc(self):
        report = Report(title="Test")
        report.add_page(Page(id="p1", title="Page 1"))

        publisher = MarkdownPublisher(include_toc=False)
        content = publisher.render(report)

        assert "Table of Contents" not in content


class TestHTMLPublisher:
    def test_publish_to_file(self):
        report = Report(title="Test Report")
        report.add_page(Page(id="intro", title="Introduction"))

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.html")
            publisher = HTMLPublisher()
            publisher.publish(report, output_path)

            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            assert "<!DOCTYPE html>" in content
            assert "Test Report" in content

    def test_custom_css(self):
        report = Report(title="Test")
        report.add_page(Page(id="p1", title="Page 1"))

        custom_css = "body { background: red; }"
        publisher = HTMLPublisher(css=custom_css)
        content = publisher.render(report)

        assert custom_css in content

    def test_render_without_toc(self):
        report = Report(title="Test")
        report.add_page(Page(id="p1", title="Page 1"))

        publisher = HTMLPublisher(include_toc=False)
        content = publisher.render(report)

        assert "Table of Contents" not in content


class TestPDFPublisher:
    def test_publish_to_file(self):
        report = Report(title="Test Report")
        report.add_page(Page(id="intro", title="Introduction"))

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.pdf")
            publisher = PDFPublisher()
            publisher.publish(report, output_path)

            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size > 0
