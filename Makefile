BIKESHED := .venv/bin/bikeshed
PYTHON := .venv/bin/python
PREVIEW_HOST ?= 127.0.0.1
PREVIEW_PORT ?= 8765

.PHONY: all setup build check preview watch clean

all: build

setup:
	uv venv .venv
	uv pip install --python $(PYTHON) -r requirements.txt

build:
	$(BIKESHED) --no-update --die-on=warning spec index.bs index.html

check: build
	$(PYTHON) scripts/validate_examples.py

preview: build
	$(PYTHON) -m http.server $(PREVIEW_PORT) --bind $(PREVIEW_HOST)

watch:
	$(BIKESHED) watch index.bs index.html

clean:
	$(PYTHON) -c 'from pathlib import Path; Path("index.html").unlink(missing_ok=True)'
