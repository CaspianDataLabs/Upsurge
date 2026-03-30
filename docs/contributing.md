# Contributing to Upsurge

Thank you for your interest in contributing to Upsurge!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kwierman/upsurge.git
   cd upsurge
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Install development dependencies:
   ```bash
   uv sync --group dev
   ```

## Running Tests

Run the test suite:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=src/upsurge --cov-report=html
```

## Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting:

```bash
uv run ruff check src/
```

Format code:

```bash
uv run ruff format src/
```

## Project Structure

```
upsurge/
├── src/upsurge/           # Main package
│   ├── __init__.py        # Public API and Report class
│   ├── content/           # Content elements
│   │   ├── base.py        # ContentElement base class
│   │   ├── page.py        # Page class
│   │   └── section.py     # Section class
│   └── publishers/       # Output publishers
│       ├── markdown.py    # MarkdownPublisher
│       ├── html.py        # HTMLPublisher
│       └── pdf.py         # PDFPublisher
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/             # Example usage
```

## Building Documentation

```bash
uv run mkdocs serve
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Reporting Issues

Please report issues on the [GitHub issue tracker](https://github.com/kwierman/upsurge/issues).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
