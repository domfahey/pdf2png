# pdf2png

Convert scanned, multi-page PDFs into lossless, page-numbered PNG images using a lightweight Python CLI.

**Author: Dominic Fahey <domfahey@gmail.com>**

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI Status](https://github.com/yourusername/pdf2png/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/pdf2png/actions)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](https://github.com/yourusername/pdf2png)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Development Workflow](#development-workflow)
- [Project Layout](#project-layout)
- [Contributing](#contributing)
- [License](#license)

## Features
- Extracts the highest-fidelity raster image from each PDF page and saves it losslessly as PNG.
- Preserves page order with zero-padded numbering (e.g., `document_page_001.png`).
- Configurable output directory and file-name prefix, plus overwrite safety checks.
- Ships with linting, formatting, type-checking, and `pytest` coverage for confident changes.

## Prerequisites
- Python 3.13 (installed automatically when using `uv`).
- [`uv`](https://github.com/astral-sh/uv) for environment management and dependency installs.

## Setup
Run the helper script (recommended):
```bash
./scripts/setup.sh
```
The script creates `.venv`, installs dev dependencies, and runs format/lint/type-check/test gates.

Or trigger the same workflow via Make:
```bash
uv run make install
```

Prefer to manage steps manually?
```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements-dev.txt
```

## Usage
Convert every page of a scanned PDF into PNGs:
```bash
uv run pdf2png.py path/to/input.pdf output/pngs --prefix receipts --overwrite
```
- Omit `--prefix` to default to the PDF file name.
- Skip `--overwrite` to guard against clobbering existing PNGs.
- Output files follow `prefix_page_###.png` numbering in the target directory.

Helper script (defaults output to current directory when `--out` is omitted):
```bash
./scripts/convert.sh --pdf path/to/input.pdf --prefix receipts --overwrite
```

Make target:
```bash
uv run make convert path/to/input.pdf PREFIX=receipts OVERWRITE=1
```

## Development Workflow
Run repository automation through `uv`:
```bash
uv run make format    # Apply ruff formatting
uv run make lint      # Run ruff checks
uv run make type-check  # Execute mypy
uv run make test      # Execute pytest suite
```

## Project Layout
```
.
├── pyproject.toml         # Project configuration and dependencies
├── pdf2png.py             # Legacy CLI entry point (imports from src/)
├── src/pdf2png/           # Main package
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Package CLI entry point
│   ├── cli.py             # CLI argument parsing and main logic
│   └── converter.py       # Core conversion utilities
├── tests/                 # pytest suites (e.g., test_pdf2png.py)
├── examples/              # Sample PDF and output files
├── scripts/               # Helper automation scripts
├── .github/workflows/     # GitHub Actions CI configuration
├── Makefile               # Development automation
├── requirements.txt       # Runtime deps (deprecated)
├── CHANGELOG.md           # Version release notes
├── AGENTS.md              # Contributor and agent development guide
├── SECURITY.md            # Security reporting policy
├── LICENSE                # MIT license
├── README.md              # This file
└── .gitignore             # Git ignore patterns
```

## Contributing
- Follow the conventions in `AGENTS.md` for style, testing, and PR etiquette.
- Keep commits concise and imperative (e.g., `Add pytest test target`).
- Include relevant `uv run make …` outputs in PR descriptions to document validation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
