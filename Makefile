PYTHON ?= .venv/bin/python

.PHONY: lint
lint:
	$(PYTHON) -m ruff check .
