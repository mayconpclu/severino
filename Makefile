VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python
MYPY = $(VENV)/bin/mypy
PYTEST = $(VENV)/bin/pytest

all:
	$(PYTHON) source/main.py
setup:
	python -m venv $(VENV)
	$(PIP) install install -e .
mypy:
	$(MYPY) source tests --config-file configs/mypy.ini
pytest:
	$(PYTEST) --cov-report term-missing:skip-covered --cov=source
