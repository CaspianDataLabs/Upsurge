# API Reference

This page documents the public API for Upsurge.

## Classes

### Report

The main container for a report with multiple pages.

```python
@dataclass
class Report:
    title: str = "Untitled Report"
    author: Optional[str] = None
    description: Optional[str] = None
    pages: list[Page] = field(default_factory=list)
```

**Methods:**

- `add_page(page: Page) -> Report` - Add a page to the report
- `get_page(page_id: str) -> Optional[Page]` - Get a page by ID
- `to_markdown() -> str` - Convert report to Markdown string
- `to_html() -> str` - Convert report to HTML string
- `save_markdown(path: str) -> None` - Save report as Markdown file
- `save_html(path: str) -> None` - Save report as HTML file
- `save_pdf(path: str) -> None` - Save report as PDF file

---

### Page

A single page in a report.

```python
@dataclass
class Page:
    id: str = ""
    title: str = ""
    content: list[ContentElement] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    toc_entry: bool = True
```

**Methods:**

- `add_content(element: ContentElement) -> Page` - Add content to the page
- `add_section(section: Section) -> Page` - Add a section to the page
- `to_markdown() -> str` - Convert page to Markdown
- `to_html() -> str` - Convert page to HTML

---

### Section

A section within a page for organizing content.

```python
@dataclass
class Section:
    title: str = ""
    level: int = 1
    id: Optional[str] = None
    content: list[ContentElement] = field(default_factory=list)
    subsections: list[Section] = field(default_factory=list)
```

**Methods:**

- `add_content(element: ContentElement) -> Section` - Add content to the section
- `add_subsection(section: Section) -> Section` - Add a subsection
- `to_markdown(base_level: int = 1) -> str` - Convert section to Markdown
- `to_html() -> str` - Convert section to HTML
- `find_by_id(section_id: str) -> Optional[Section]` - Find a section by ID

---

## Content Elements

All content elements inherit from `ContentElement` and implement `to_markdown()` and `to_html()` methods.

### Text

Plain text with optional styling.

```python
@dataclass
class Text(ContentElement):
    content: str = ""
    format: str = "plain"
    style: Optional[str] = None  # "bold", "italic", "code"
```

---

### Image

An image from a file path or URL.

```python
@dataclass
class Image(ContentElement):
    path: Optional[str] = None
    url: Optional[str] = None
    alt: str = ""
    width: Optional[str] = None
    height: Optional[str] = None
    caption: Optional[str] = None
```

---

### Plot

A matplotlib figure embedded in the report.

```python
@dataclass
class Plot(ContentElement):
    figure: Any = None
    caption: Optional[str] = None
    format: str = "png"
    width: Optional[int] = None
    height: Optional[int] = None
```

---

### Table

A table with headers and data rows.

```python
@dataclass
class Table(ContentElement):
    data: list[list[Any]] = field(default_factory=list)
    headers: Optional[list[str]] = None
    caption: Optional[str] = None
    column_align: Optional[list[str]] = None  # "left", "center", "right"
```

---

### Link

An external hyperlink.

```python
@dataclass
class Link(ContentElement):
    text: str = ""
    url: str = ""
    new_tab: bool = False
```

---

### PageLink

An internal link to another page in the report.

```python
@dataclass
class PageLink(ContentElement):
    text: str = ""
    page_id: str = ""
    page_title: Optional[str] = None
```

---

## Publishers

Publishers convert a Report to a specific format.

### MarkdownPublisher

```python
class MarkdownPublisher:
    def publish(self, report: Report, path: str) -> None
```

### HTMLPublisher

```python
class HTMLPublisher:
    def publish(self, report: Report, path: str) -> None
```

### PDFPublisher

```python
class PDFPublisher:
    def publish(self, report: Report, path: str) -> None
```
