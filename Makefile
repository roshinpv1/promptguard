PYTHON ?= python
VENV ?= .venv

.PHONY: setup test scan

setup:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate; pip install -U pip
	. $(VENV)/bin/activate; pip install -e ".[dev]"

test:
	. $(VENV)/bin/activate; pytest -q

scan:
	. $(VENV)/bin/activate; promptshield scan --config promptshield.yaml --output-dir artifacts

