.PHONY: help doctor install convert lint format test type-check coverage check clean build publish

.DEFAULT_GOAL := help

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

doctor: check

install:
	uv sync --dev

convert:
	@if [ -z "$(PDF)" ]; then \
		echo "Usage: make convert PDF=path/to/file.pdf [PREFIX=name] [OVERWRITE=1]"; \
		exit 1; \
	fi; \
	uv run pdf2png "$(PDF)" . --prefix "$(or $(PREFIX),$(basename $(PDF)))" $(if $(filter 1 true yes,$(OVERWRITE)),--overwrite)

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

test:
	PYTHONPATH=src uv run pytest tests/

coverage:
	PYTHONPATH=src uv run pytest --cov=src/pdf2png --cov-report=term-missing

type-check:
	uv run mypy src/

check: lint type-check test coverage

clean:
	rm -rf .venv dist *.egg-info

build:
	uv build

publish:
	uv build
	uv publish
