# Upsurge

Welcome to the **Upsurge** documentation! Upsurge is a Python library for creating multi-format reports with support for sections, text, images, plots, tables, and multiple pages with internal links.

## What is Upsurge?

Upsurge provides a simple, powerful way to generate reports:

- **Multi-page Reports**: Create reports with multiple pages and navigation
- **Rich Content**: Support for text, images, matplotlib plots, and pandas tables
- **Multiple Formats**: Export to Markdown, HTML, and PDF
- **Internal Linking**: Link between pages within your report

## Features

- **Type-safe** - Built with Python type hints
- **Extensible** - Add custom content elements and styling
- **Multiple Export Formats** - Markdown, HTML, and PDF support
- **Automatic Table of Contents** - Generated for multi-page reports

## Quick Example

```python
from upsurge import Report, Page, Text, Section
from upsurge.publishers import HTMLPublisher

report = Report(
    title="My Report",
    author="John Doe",
    description="A sample report"
)

page = Page(id="introduction", title="Introduction")
page.add_content(Text(content="Welcome to my report!"))

section = Section(title="Background", level=2)
section.add_content(Text(content="Some background information..."))
page.add_section(section)

report.add_page(page)

publisher = HTMLPublisher()
publisher.publish(report, "my_report.html")
```

## Navigation

- [Getting Started](getting-started/installation.md) - Install and set up Upsurge
- [Quick Start](getting-started/quick-start.md) - Build your first report
- [API Reference](api.md) - Complete API documentation

## License

Upsurge is released under the MIT License.
