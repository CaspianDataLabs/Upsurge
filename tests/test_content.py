"""Tests for content elements."""

from upsurge.content.base import (
    Text,
    Image,
    Table,
    Link,
    PageLink,
)
from upsurge.content.section import Section
from upsurge.content.page import Page
from upsurge import Report


class TestText:
    def test_text_plain(self):
        text = Text(content="Hello, World!")
        assert text.to_markdown() == "Hello, World!"
        assert "Hello, World!" in text.to_html()

    def test_text_bold(self):
        text = Text(content="Bold text", style="bold")
        assert text.to_markdown() == "**Bold text**"
        assert "<strong>" in text.to_html()

    def test_text_italic(self):
        text = Text(content="Italic text", style="italic")
        assert text.to_markdown() == "*Italic text*"
        assert "<em>" in text.to_html()

    def test_text_code(self):
        text = Text(content="code", style="code")
        assert text.to_markdown() == "`code`"
        assert "<code>" in text.to_html()


class TestImage:
    def test_image_with_path(self):
        img = Image(path="image.png", alt="Test image")
        md = img.to_markdown()
        assert "image.png" in md
        assert "Test image" in md
        assert "img" in img.to_html()

    def test_image_with_url(self):
        img = Image(url="https://example.com/image.png", alt="Remote image")
        md = img.to_markdown()
        assert "https://example.com/image.png" in md

    def test_image_with_caption(self):
        img = Image(path="image.png", alt="Test", caption="A test image")
        md = img.to_markdown()
        assert "A test image" in md
        html = img.to_html()
        assert "caption" in html


class TestTable:
    def test_table_basic(self):
        table = Table(
            data=[["A", "B"], ["C", "D"]],
            headers=["Col1", "Col2"],
        )
        md = table.to_markdown()
        assert "Col1" in md
        assert "Col2" in md
        assert "A" in md
        assert "<table>" in table.to_html()

    def test_table_with_caption(self):
        table = Table(
            data=[["A"]],
            caption="Test caption",
        )
        md = table.to_markdown()
        assert "Test caption" in md

    def test_table_with_alignment(self):
        table = Table(
            data=[["A", "B"]],
            headers=["Col1", "Col2"],
            column_align=["left", "right"],
        )
        md = table.to_markdown()
        assert ":" in md


class TestLink:
    def test_link_basic(self):
        link = Link(text="Click here", url="https://example.com")
        assert "[Click here](https://example.com)" in link.to_markdown()
        assert '<a href="https://example.com">' in link.to_html()

    def test_link_new_tab(self):
        link = Link(text="External", url="https://example.com", new_tab=True)
        html = link.to_html()
        assert 'target="_blank"' in html


class TestPageLink:
    def test_pagelink_basic(self):
        link = PageLink(text="Go to intro", page_id="intro")
        assert "[Go to intro](#intro)" in link.to_markdown()
        assert 'href="#intro"' in link.to_html()


class TestSection:
    def test_section_basic(self):
        section = Section(title="My Section", level=2)
        section.add_content(Text(content="Section content"))
        md = section.to_markdown()
        assert "## My Section" in md
        assert "Section content" in md

    def test_section_with_subsection(self):
        section = Section(title="Parent")
        subsection = Section(title="Child")
        section.add_subsection(subsection)
        md = section.to_markdown()
        assert "# Parent" in md
        assert "## Child" in md

    def test_section_to_html(self):
        section = Section(title="Test", id="test-section")
        html = section.to_html()
        assert "<h1" in html
        assert 'id="test-section"' in html


class TestPage:
    def test_page_basic(self):
        page = Page(id="page1", title="Page One")
        page.add_content(Text(content="Page content"))
        md = page.to_markdown()
        assert "## Page One" in md
        assert "Page content" in md

    def test_page_with_section(self):
        page = Page(id="page1", title="Test Page")
        section = Section(title="Section")
        page.add_section(section)
        html = page.to_html()
        assert "Section" in html


class TestReport:
    def test_report_basic(self):
        report = Report(title="Test Report")
        report.add_page(Page(id="page1", title="Page 1"))

        md = report.to_markdown()
        assert "# Test Report" in md
        assert "Page 1" in md

    def test_report_with_author(self):
        report = Report(title="Test", author="John Doe")
        md = report.to_markdown()
        assert "John Doe" in md

    def test_report_with_description(self):
        report = Report(title="Test", description="A test report")
        md = report.to_markdown()
        assert "A test report" in md

    def test_report_toc(self):
        report = Report(title="Test")
        report.add_page(Page(id="p1", title="Page 1"))
        report.add_page(Page(id="p2", title="Page 2"))

        md = report.to_markdown()
        assert "Table of Contents" in md
        assert "Page 1" in md
        assert "Page 2" in md

    def test_report_get_page(self):
        report = Report(title="Test")
        page = Page(id="intro", title="Introduction")
        report.add_page(page)

        found = report.get_page("intro")
        assert found is not None
        assert found.title == "Introduction"

    def test_report_html(self):
        report = Report(title="Test Report")
        report.add_page(Page(id="page1", title="Page 1"))

        html = report.to_html()
        assert "<!DOCTYPE html>" in html
        assert "Test Report" in html
        assert "<nav class='toc'>" in html
