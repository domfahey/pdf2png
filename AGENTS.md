# AI Agent Guidelines for pdf2png Project

## Overview

This document provides comprehensive guidelines for AI-powered coding agents working on the pdf2png project. The agents are expected to maintain high-quality software engineering practices while efficiently contributing to the codebase.

## Agent Capabilities

### Core Skills Required
- **Python Development**: Expert knowledge of Python 3.13, async patterns, and modern best practices
- **CLI Tool Development**: Experience with argument parsing, error handling, and cross-platform compatibility
- **Testing Frameworks**: Proficiency with pytest, mocking, and coverage analysis
- **Code Quality**: Mastery of linting (Ruff), type checking (MyPy), formatting, and documentation
- **Package Management**: Expertise with UV, pyproject.toml, and dependency management

### Specialized Knowledge
- **PDF Processing**: Understanding of Pikepdf library and image extraction from PDFs
- **Image Processing**: Familiarity with PIL/Pillow for image manipulation and lossless PNG output
- **File System Operations**: Secure handling of file paths, directories, and overwrites

## Communication Protocols

### Command Execution
All commands must be executed safely with proper approval for destructive operations. Output should be captured and analyzed for success/failure indicators.

### File Modifications
- Use search_replace for targeted edits with exact matching
- Always check file contents before and after modifications
- Never modify files without clear justification
- Preserve existing code structure and comments

### Task Reporting
- Provide clear, technical summaries of completed work
- Use TODO lists for complex multi-step tasks
- Indicate progress and any blockers encountered

## Environment and Integration

### Development Environment Setup
```bash
# Install dependencies
uv sync --dev

# Run full quality checks
make check

# Execute test suite
make test
```

### Workflow Integration
- **Continuous Integration**: GitHub Actions workflow automatically validates all commits
- **Pre-commit Hooks**: Configured for automatic quality checks
- **Automated Testing**: 88% code coverage requirement
- **Type Checking**: Strict MyPy validation in CI

## Guidelines and Rules

### Code Standards
- **Type Hints**: All public functions must have complete type annotations
- **Docstrings**: Google-style docstrings with Args, Returns, Raises sections
- **Line Length**: 88 characters maximum (Ruff default)
- **Import Organization**: Strict import sorting and grouping

### Security Rules
- **Never Commit Secrets**: Use .gitignore patterns to exclude sensitive files
- **Environment Variables**: For configuration requiring sensitive data
- **Input Validation**: All file inputs must be validated for existence and type
- **Error Handling**: Comprehensive exception handling with informative messages

### Testing Requirements
- **Test Coverage**: Maintain 85%+ coverage across all modules
- **Edge Cases**: Test error conditions, edge cases, and failure scenarios
- **Mocking**: Proper use of pytest fixtures and mocking for external dependencies
- **Performance**: Include realistic test durations and resource usage

## Project Structure & Module Organization

### Current Architecture
```
├── pdf2png.py              # Legacy CLI entry point (imports from src/)
├── src/pdf2png/            # Main package (PEP 420 namespace)
│   ├── __init__.py         # Package exports
│   ├── __main__.py         # CLI module for `python -m` execution
│   ├── converter.py        # Core PDF to PNG conversion logic
├── tests/                  # pytest test suite
├── examples/               # Sample files for testing
├── .github/workflows/      # CI/CD configuration
├── scripts/                # Automation scripts
├── pyproject.toml          # Modern Python configuration
├── Makefile                # Development workflow automation
└── AGENTS.md               # This file - AI agent guidelines
```

### Key Design Patterns
- **Exception Handling**: Custom errors with clear messaging
- **Configuration**: Argument parsing with sensible defaults
- **Path Management**: Robust pathlib usage throughout
- **Type Safety**: Comprehensive type hints and strict validation

## Development Commands

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

## Security Guidelines

- **Never commit secrets or sensitive data** to the repository. Use environment variables or secure credential management instead of hardcoding keys, passwords, or tokens
- Check `.gitignore` for comprehensive patterns that should exclude sensitive files
- If you accidentally commit sensitive data, revoke and rotate the affected credentials immediately
- Be cautious when adding new dependencies - review for security vulnerabilities

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
