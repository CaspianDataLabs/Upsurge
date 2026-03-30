#!/usr/bin/env python3
"""Example demonstrating Upsurge report generation capabilities."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from upsurge import (
    Report,
    Page,
    Section,
    Text,
    Plot,
    Table,
    Link,
    PageLink,
)
from upsurge.publishers import MarkdownPublisher, HTMLPublisher, PDFPublisher


def create_sample_report() -> Report:
    report = Report(
        title="Sample Technical Report",
        author="John Doe",
        description="A demonstration of Upsurge report generation capabilities",
    )

    intro_page = Page(
        id="introduction",
        title="Introduction",
    )
    intro_page.add_content(
        Text(
            content="Welcome to the Upsurge Report Generation Library. "
            "This library allows you to create beautiful reports using Python objects.",
            style="plain",
        )
    )
    intro_page.add_content(Text(content="Features include:", style="bold"))

    features_section = Section(title="Key Features", level=2)
    features_section.add_content(Text(content="- Multi-page support with internal links"))
    features_section.add_content(
        Text(content="- Rich content elements: text, images, plots, tables")
    )
    features_section.add_content(Text(content="- Multiple export formats: Markdown, HTML, PDF"))
    intro_page.add_section(features_section)

    report.add_page(intro_page)

    data_page = Page(
        id="data-analysis",
        title="Data Analysis",
    )

    df = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Sales": [1200, 1900, 3000, 5000, 2300, 3100],
            "Expenses": [800, 1200, 1800, 2500, 1500, 2100],
        }
    )

    table_section = Section(title="Sales Data", level=2)
    table_section.add_content(
        Table(
            data=df.values.tolist(),
            headers=list(df.columns),
            caption="Monthly Sales and Expenses for 2024",
            column_align=["left", "right", "right"],
        )
    )
    data_page.add_section(table_section)

    plot_section = Section(title="Visualization", level=2)

    fig, ax = plt.subplots(figsize=(10, 6))
    months = df["Month"]
    sales = df["Sales"]
    expenses = df["Expenses"]

    x = np.arange(len(months))
    width = 0.35

    ax.bar(x - width / 2, sales, width, label="Sales", color="#3498db")
    ax.bar(x + width / 2, expenses, width, label="Expenses", color="#e74c3c")

    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Monthly Sales vs Expenses")
    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plot_section.add_content(
        Plot(
            figure=fig,
            caption="Sales and Expenses Comparison",
            width=800,
            height=400,
        )
    )
    data_page.add_section(plot_section)

    report.add_page(data_page)

    links_page = Page(
        id="navigation",
        title="Navigation & Links",
    )

    links_page.add_content(
        Text(
            content="This page demonstrates linking between pages and external resources.",
        )
    )

    links_section = Section(title="External Links", level=2)
    links_section.add_content(
        Link(
            text="Visit Python.org",
            url="https://www.python.org",
            new_tab=True,
        )
    )
    links_page.add_section(links_section)

    toc_section = Section(title="Quick Navigation", level=2)
    toc_section.add_content(Text(content="Jump to other sections:"))
    toc_section.add_content(
        PageLink(
            text="Go to Introduction",
            page_id="introduction",
        )
    )
    toc_section.add_content(
        PageLink(
            text="Go to Data Analysis",
            page_id="data-analysis",
        )
    )
    links_page.add_section(toc_section)

    report.add_page(links_page)

    return report


def main():
    report = create_sample_report()

    md_publisher = MarkdownPublisher()
    md_publisher.publish(report, "example_report.md")
    print("Generated: example_report.md")

    html_publisher = HTMLPublisher()
    html_publisher.publish(report, "example_report.html")
    print("Generated: example_report.html")

    try:
        pdf_publisher = PDFPublisher()
        pdf_publisher.publish(report, "example_report.pdf")
        print("Generated: example_report.pdf")
    except Exception as e:
        print(f"PDF generation skipped: {e}")

    print("\nAll reports generated successfully!")


if __name__ == "__main__":
    main()
