.. Upsurge documentation master file

Welcome to Upsurge's documentation!
=====================================

Upsurge is a Python library for creating multi-format reports with support for
sections, text, images, plots, tables, and multiple pages with internal links.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   api

Features
--------

- **Multi-page Reports**: Create reports with multiple pages and navigation
- **Rich Content**: Support for text, images, matplotlib plots, and pandas tables
- **Multiple Formats**: Export to Markdown, HTML, and PDF
- **Internal Linking**: Link between pages within your report
- **Customizable**: Extensible design with custom CSS support

Quick Start
-----------

Install the package:

.. code-block:: bash

    pip install upsurge

Create a simple report:

.. code-block:: python

    from upsurge import Report, Page, Text
    
    report = Report(title="My Report")
    report.add_page(
        Page(
            id="intro",
            title="Introduction",
        ).add_content(Text(content="Hello, World!"))
    )
    
    report.save_html("my_report.html")

For more examples, see the `examples <https://github.com/kwierman/upsurge/tree/main/examples>`_ directory.

Indices and tables
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
