SRC_PATH 		= {{ cookiecutter.project_slug }}

BLACK			= python3 -m black --line-length 79 --target-version py{{ cookiecutter.python_version.replace('.', '') }}
MYPY			= python3 -m mypy
PDOC			= python3 -m pdoc -d google --math
PYLINT			= python3 -m pylint

DOCS_PATH 		= docs
VENV_PATH		= venv

.ONESHELL:

all: format typecheck lint

.PHONY: docs
docs:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	$(PDOC) --output-directory $(DOCS_PATH) $(SRC_PATH)

.PHONY: docs-browser
docs-browser:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	$(PDOC) $(SRC_PATH)

.PHONY: format
format:
	$(BLACK) $(SRC_PATH)

.PHONY: lint
lint:
	$(PYLINT) $(SRC_PATH)

.PHONY: typecheck
typecheck:
	$(MYPY) -p $(SRC_PATH)
