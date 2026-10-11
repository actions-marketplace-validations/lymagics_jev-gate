PYTHON ?= .venv/Scripts/python

.DEFAULT_GOAL := help
.PHONY: help unit e2e black flake8 ruff

help:
	@echo "Usage: make <target> [PYTHON=path/to/python]"
	@echo ""
	@echo "Tests:"
	@echo "  unit     Run the fast tests and fail if coverage drops below 90%"
	@echo "  e2e      Run the deep tests that start the tool as a real process"
	@echo ""
	@echo "Code style:"
	@echo "  black    Reformat jev_gate and tests in place"
	@echo "  flake8   Check jev_gate and tests with flake8"
	@echo "  ruff     Check jev_gate and tests with ruff"
	@echo ""
	@echo "PYTHON defaults to $(PYTHON)"

unit:
	$(PYTHON) -m pytest -m "not deep and not online" --cov --cov-report=term-missing --cov-fail-under=90

e2e:
	$(PYTHON) -m pytest -m deep

black:
	$(PYTHON) -m black jev_gate tests

flake8:
	$(PYTHON) -m flake8 jev_gate tests

ruff:
	$(PYTHON) -m ruff check jev_gate tests
