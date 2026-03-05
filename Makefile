VENV := venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python
PIP := $(BIN)/pip

.PHONY: test lint format typecheck check clean

$(VENV):
	python3 -m venv $(VENV)

$(VENV)/.dev-installed: setup.py | $(VENV)
	$(PIP) install -e ".[dev]"
	touch $@

install: $(VENV)
	$(PIP) install -e .

install-dev: $(VENV)/.dev-installed

test: $(VENV)/.dev-installed
	$(BIN)/pytest tests/ -v

lint: $(VENV)/.dev-installed
	$(BIN)/ruff check .

format: $(VENV)/.dev-installed
	$(BIN)/ruff format .

typecheck: $(VENV)/.dev-installed
	$(BIN)/mypy odb_tui/

check: lint typecheck test

clean:
	rm -rf $(VENV) dist build *.egg-info .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
