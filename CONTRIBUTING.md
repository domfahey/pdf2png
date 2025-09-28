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

## Development Setup

1. **Prerequisites**: Ensure you have Python 3.13+ and `uv` installed.
2. **Clone the repository**: `git clone https://github.com/yourusername/pdf2png.git && cd pdf2png`
3. **Install dependencies**: `uv sync --dev`
4. **Set up pre-commit hooks**: `uv run pre-commit install`
5. **Verify setup**: Run `make check` to ensure everything is working

## Testing Guidelines

- Write tests under `tests/` named `test_<feature>.py`
- Prefer fixture-backed temporary paths for file outputs
- Cover error cases such as missing images or fileoverwrite issues
- Run `uv run pytest` or `make test` before submitting changes
- Include new tests with any new feature or bug fix

## Coding Standards

- Use `ruff` formatting and linting (see `pyproject.toml`)
- Write type-hinted Python with `mypy` compliance
- Follow Google-style docstrings for functions and modules
- Use descriptive variable names and maintain consistency
- Keep functions focused on single responsibilities

## Pull Request Template

When creating a pull request, include:

- **Description**: What changes does this PR introduce?
- **Testing**: How have you tested these changes?
- **Checklist**: Ensure the following are met:
  - [ ] Tests pass (`make test`)
  - [ ] Code style checks pass (`make lint`)
  - [ ] Typing checks pass (`make type-check`)
  - [ ] No security issues introduced
  - [ ] Documentation updated if needed

## Commit Message Guidelines

- Follow imperative, concise messages like `Add pytest test target` or `Fix page processing error`
- Use conventional commit prefixes when applicable:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for code restructuring
  - `test:` for test additions

## Commit & Pull Request Guidelines
- Each PR should summarize functional changes, provide validation command outputs, and link related issues
- Include before/after examples for CLI changes
- Keep PR scope focused on a single concern when possible
- Request reviews from maintainers before merging
