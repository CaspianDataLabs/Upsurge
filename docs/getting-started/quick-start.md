# Quick Start

This guide will walk you through the basics of using Upsurge to create reports.

## Step 1: Create a Report

Create a Python file (e.g., `report.py`) and create a Report instance:

```python
from upsurge import Report, Page, Text
from upsurge.publishers import HTMLPublisher

report = Report(
    title="My Report",
    author="John Doe",
    description="A sample report"
)
```

## Step 2: Add Pages

Create pages and add content to them:

```python
page = Page(id="introduction", title="Introduction")
page.add_content(Text(content="Welcome to my report!"))

report.add_page(page)
```

## Step 3: Add Sections

Organize content into sections:

```python
from upsurge import Section

page2 = Page(id="details", title="Details")

section = Section(title="Background", level=2)
section.add_content(Text(content="Some background information..."))
page2.add_section(section)

report.add_page(page2)
```

## Step 4: Export the Report

Export to your desired format:

```python
# HTML
publisher = HTMLPublisher()
publisher.publish(report, "report.html")

# Markdown
from upsurge import MarkdownPublisher
md_publisher = MarkdownPublisher()
md_publisher.publish(report, "report.md")

# PDF
from upsurge import PDFPublisher
pdf_publisher = PDFPublisher()
pdf_publisher.publish(report, "report.pdf")
```

## Working with Tables

```python
import pandas as pd
from upsurge import Table

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
})

table = Table(
    data=df.values.tolist(),
    headers=list(df.columns),
    caption="Employee List"
)

page.add_content(table)
```

## Working with Plots

```python
import matplotlib.pyplot as plt
from upsurge import Plot

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

plot = Plot(
    figure=fig,
    caption="A quadratic curve"
)

page.add_content(plot)
```

## Adding Links

```python
from upsurge import Link, PageLink

# External link
page.add_content(Link(text="Visit Google", url="https://google.com", new_tab=True))

# Internal link to another page
page.add_content(PageLink(text="Go to Details", page_id="details"))
```

## Adding Images

```python
from upsurge import Image

page.add_content(Image(path="image.png", caption="A sample image"))
```

## Next Steps

- Explore the [API Reference](../api.md) for complete documentation
- Check out the examples in the `examples/` directory for more use cases
