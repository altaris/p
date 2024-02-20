SRC_PATH 	= {{ cookiecutter.project_slug }}
VENV_PATH	= venv
DOCS_PATH 	= docs

BLACK		= $(PYTHON) -m black --line-length 79 --target-version py{{ cookiecutter.python_version.replace('.', '') }}
ISORT		= $(PYTHON) -m isort --line-length 79 --python-version {{ cookiecutter.python_version.replace('.', '') }} --multi-line VERTICAL_HANGING_INDENT
MYPY		= $(PYTHON) -m mypy
PDOC		= $(PYTHON) -m pdoc -d google --math
PYLINT		= $(PYTHON) -m pylint
PYTHON		= python{{ cookiecutter.python_version }}

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
	$(ISORT) $(SRC_PATH)
	$(BLACK) $(SRC_PATH)

.PHONY: lint
lint:
	$(PYLINT) $(SRC_PATH)

.PHONY: typecheck
typecheck:
	$(MYPY) -p $(SRC_PATH)
