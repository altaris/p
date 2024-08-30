SRC_PATH 	= {{ cookiecutter.project_slug }}
VENV_PATH	= venv
DOCS_PATH 	= docs

PDOC		= pdoc -d google --math
PYTHON		= python{{ cookiecutter.python_version }}

.ONESHELL:

all: format typecheck lint

.PHONY: docs
docs:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	$(PYTHON) -m $(PDOC) --output-directory $(DOCS_PATH) $(SRC_PATH)

.PHONY: docs-browser
docs-browser:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	$(PYTHON) -m $(PDOC) -h 0.0.0.0 -p 8081 -n $(SRC_PATH)

.PHONY: format
format:
	$(PYTHON) -m isort $(SRC_PATH)
	$(PYTHON) -m black $(SRC_PATH)

.PHONY: lint
lint:
	$(PYTHON) -m pylint $(SRC_PATH)

.PHONY: typecheck
typecheck:
	$(PYTHON) -m mypy -p $(SRC_PATH)
