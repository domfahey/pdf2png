# Makefile for pdf2png project development workflow
# This file provides automation for common development, testing, and deployment tasks
# Uses UV for Python dependency management and modern CLI tools

# Default target - show help when running 'make' without arguments
.DEFAULT_GOAL := help

# Declare all phony targets (don't create files with these names)
.PHONY: help doctor install convert lint format test type-check coverage check clean build publish

# Display this help message
help:
	@echo "Available targets:"
	@echo "  install      Install development dependencies"
	@echo "  convert      Convert PDF to PNG (usage: make convert PDF=path/to/file.pdf [PREFIX=name] [OVERWRITE=1])"
	@echo "  lint         Run Ruff linting and auto-fix"
	@echo "  format       Run Ruff code formatting"
	@echo "  test         Run pytest test suite"
	@echo "  type-check   Run MyPy type checking"
	@echo "  coverage     Run tests with coverage report"
	@echo "  check        Run lint, type-check, test, and coverage"
	@echo "  doctor       Alias for check - verify project health"
	@echo "  clean        Clean up build artifacts and virtual environment"
	@echo "  build        Build distribution packages"
	@echo "  publish      Build and publish to PyPI"

# Run full health check (lint + type-check + test + coverage)
doctor: check

# Install development dependencies using UV
install:
	uv sync --dev

# Convert PDF to PNG with validation and optional parameters
# Requires PDF=path/to/file.pdf (mandatory), supports PREFIX and OVERWRITE
convert:
	@if [ -z "$(PDF)" ]; then \
		echo "Usage: make convert PDF=path/to/file.pdf [PREFIX=name] [OVERWRITE=1]"; \
		exit 1; \
	fi; \
	uv run pdf2png "$(PDF)" . --prefix "$(or $(PREFIX),$(basename $(PDF)))" $(if $(filter 1 true yes,$(OVERWRITE)),--overwrite)

# Run Ruff linting with automatic fixes
lint:
	uv run ruff check . --fix

# Run Ruff code formatting
format:
	uv run ruff format .

# Run pytest test suite with Python path set for src/ layout
test:
	PYTHONPATH=src uv run pytest tests/

# Run tests with coverage reporting
coverage:
	PYTHONPATH=src uv run pytest --cov=src/pdf2png --cov-report=term-missing

# Run MyPy type checking on source code
type-check:
	uv run mypy src/

# Run full quality check pipeline
check: lint type-check test coverage

# Clean up build artifacts and virtual environments
clean:
	rm -rf .venv dist *.egg-info

# Build distribution packages
build:
	uv build

# Build and publish to PyPI
publish:
	uv build
	uv publish
