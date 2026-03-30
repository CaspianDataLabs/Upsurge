# Getting Started

## Installation

Install Upsurge using pip:

```bash
pip install upsurge
```

For development installation:

```bash
pip install upsurge[dev]
```

## Basic Usage

Creating a report with Upsurge is straightforward:

```python
from upsurge import Report, Page, Text, Section

# Create a report
report = Report(
    title="My Report",
    author="John Doe",
    description="A sample report"
)

# Add a page
page = Page(
    id="introduction",
    title="Introduction"
)

# Add content
page.add_content(Text(content="Welcome to my report!"))

# Add sections
section = Section(title="Background", level=2)
section.add_content(Text(content="Some background information..."))
page.add_section(section)

# Add page to report
report.add_page(page)
```

## Exporting Reports

Upsurge supports multiple export formats:

### Markdown

```python
from upsurge.publishers import MarkdownPublisher

publisher = MarkdownPublisher()
publisher.publish(report, "report.md")
```

### HTML

```python
from upsurge.publishers import HTMLPublisher

publisher = HTMLPublisher()
publisher.publish(report, "report.html")
```

### PDF

```python
from upsurge.publishers import PDFPublisher

publisher = PDFPublisher()
publisher.publish(report, "report.pdf")
```

## Advanced Usage

### Working with Tables

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
    caption="Employee List",
    column_align=["left", "center"]
)
```

### Working with Plots

```python
import matplotlib.pyplot as plt
from upsurge import Plot

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_title("Sample Plot")

plot = Plot(
    figure=fig,
    caption="A quadratic curve",
    width=600,
    height=400
)
```

### Internal Links

```python
from upsurge import PageLink, Link

# Link to another page
page_link = PageLink(
    text="Go to Introduction",
    page_id="introduction"
)

# External link
external_link = Link(
    text="Visit Python.org",
    url="https://www.python.org",
    new_tab=True
)
```

### Custom CSS

```python
custom_css = """
body {
    font-family: 'Georgia', serif;
    background-color: #f5f5f5;
}
h1 {
    color: #2c3e50;
}
"""

publisher = HTMLPublisher(css=custom_css)
publisher.publish(report, "custom_report.html")
```
