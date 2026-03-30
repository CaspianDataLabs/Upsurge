# Installation

## Requirements

- Python 3.10 or higher
- pip or uv package manager

## Install with pip

```bash
pip install upsurge
```

## Install with uv

```bash
uv add upsurge
```

## Install for Development

```bash
pip install upsurge[dev]
```

## Verify Installation

After installation, verify that Upsurge is installed correctly:

```bash
python -c "import upsurge; print(upsurge.__version__)"
```

## Dependencies

Upsurge depends on:

- **markdown-it-py** (>=3.0.0) - For Markdown parsing
- **jinja2** (>=3.1.0) - For templating
- **weasyprint** (>=60.0) - For PDF generation
- **matplotlib** (>=3.7.0) - For plot rendering
- **pandas** (>=2.0.0) - For table handling

These are installed automatically with Upsurge.

## Next Steps

Proceed to the [Quick Start](quick-start.md) guide to learn how to use Upsurge.
