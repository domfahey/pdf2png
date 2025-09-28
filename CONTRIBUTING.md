# Repository Guidelines

## Table of Contents

- [Project Structure & Module Organization](#project-structure--module-organization)
- [Build, Test, and Development Commands](#build-test-and-development-commands)
- [Coding Style & Naming Conventions](#coding-style--naming-conventions)
- [Testing Guidelines](#testing-guidelines)
- [Commit & Pull Request Guidelines](#commit--pull-request-guidelines)

## Project Structure & Module Organization
- `pdf2png.py` contains the CLI entry point and conversion utilities.
- `tests/` holds `pytest` suites (e.g., `tests/test_pdf2png.py`) that synthesize PDFs for regression checks.
- `Makefile` defines common automation shortcuts; `requirements*.txt` pin runtime and dev dependencies.
- Virtual environments are expected in `.venv/` (git-ignored) and should be managed with `uv` for reproducibility.

## Build, Test, and Development Commands
- `uv venv .venv && source .venv/bin/activate` sets up the local environment.
- `uv pip install -r requirements-dev.txt` installs runtime, linting, type-checking, and test dependencies.
- `uv run make format` runs `ruff format` to normalize Python code.
- `uv run make lint` runs `ruff check` for style and quality gates.
- `uv run make type-check` runs `mypy` across the repository.
- `uv run make test` runs the `pytest` suite.
- `uv run make convert path/to/input.pdf [PREFIX=name] [OVERWRITE=1]` wraps the CLI conversion workflow, defaulting output to the current directory.

## Coding Style & Naming Conventions
- Python code targets `ruff` defaults; keep functions short and add comments only when logic is non-obvious.
- Prefer explicit type hints for public helpers; satisfy `mypy` without suppressions when possible.
- Name output artifacts as `prefix_page_###.png` to match CLI expectations; keep module names snake_case.
- Use spaces (4-space indent) and UTF-8/ASCII-safe literals.

## Testing Guidelines
- Write tests under `tests/` named `test_<feature>.py`; prefer fixture-backed temporary paths for file outputs.
- Cover error cases such as missing images or overwritten files.
- Run `make test` before submitting changes; include new tests with any new feature or bug fix.

## Commit & Pull Request Guidelines
- Follow imperative, concise commit messages similar to `Add pytest test target` or `Implement lossless page export`.
- Each PR should summarize functional changes, list validation commands (lint/test/type-check), and link relevant issues.
- Include before/after screenshots only when CLI output changes; otherwise provide sample command invocations.
