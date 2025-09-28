.PHONY: install convert lint format test type-check coverage

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
	uv run pytest

coverage:
	uv run pytest --cov=src/pdf2png --cov-report=term-missing

type-check:
	uv run mypy

check: lint type-check test coverage

clean:
	rm -rf .venv dist *.egg-info

build:
	uv build

publish:
	uv build
	uv publish
