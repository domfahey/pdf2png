PYTHON ?= .venv/bin/python

ifneq ($(filter convert,$(MAKECMDGOALS)),)
CONVERT_ARGS := $(filter-out convert,$(MAKECMDGOALS))
ifndef PDF
PDF := $(firstword $(CONVERT_ARGS))
endif
ifeq ($(strip $(PDF)),)
$(error PDF argument required. Usage: make convert sample.pdf or make convert PDF=sample.pdf)
endif
EXTRA_CONVERT_GOALS := $(filter-out $(PDF),$(CONVERT_ARGS))
ifneq ($(strip $(CONVERT_ARGS)),)
.PHONY: $(CONVERT_ARGS)
$(CONVERT_ARGS):
	@:
endif
endif

CONVERT_PREFIX :=
ifneq ($(strip $(PREFIX)),)
  CONVERT_PREFIX := --prefix "$(PREFIX)"
endif

CONVERT_OVERWRITE :=
ifneq ($(filter 1 true yes,$(OVERWRITE)),)
  CONVERT_OVERWRITE := --overwrite
endif

.PHONY: install convert lint format test type-check

install:
	./scripts/setup.sh

convert:
	./scripts/convert.sh --pdf "$(PDF)" $(CONVERT_PREFIX) $(CONVERT_OVERWRITE)
lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

test:
	$(PYTHON) -m pytest

type-check:
	$(PYTHON) -m mypy .
