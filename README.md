# pdf2png

Convert scanned, multi-page PDFs into lossless, page-numbered PNG images using a lightweight Python CLI.

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

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
├── pdf2png.py            # CLI entry point and conversion logic
├── tests/                # pytest suites (e.g., synthetic PDF regression tests)
├── Makefile              # Developer automation (lint, format, test, type-check)
├── requirements.txt      # Runtime dependencies (pikepdf, Pillow)
├── requirements-dev.txt  # Development tooling requirements
├── scripts/              # Helper automation (setup + conversion wrappers)
└── AGENTS.md             # Contributor guide for agents and maintainers
```

## Contributing
- Follow the conventions in `AGENTS.md` for style, testing, and PR etiquette.
- Keep commits concise and imperative (e.g., `Add pytest test target`).
- Include relevant `uv run make …` outputs in PR descriptions to document validation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
