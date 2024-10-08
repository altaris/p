SRC_PATH 	= {{ cookiecutter.project_slug }}
DOCS_PATH 	= docs

PDOC		= pdoc -d google --math
PYTHON		= python{{ cookiecutter.python_version }}

RUFF_EXCL   = --exclude '*.ipynb' --exclude 'old/'

.ONESHELL:

all: format typecheck lint

.PHONY: docs
docs:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	PDOC_ALLOW_EXEC=1 uv run $(PDOC) --output-directory $(DOCS_PATH) $(SRC_PATH)

.PHONY: docs-browser
docs-browser:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	PDOC_ALLOW_EXEC=1 uv run $(PDOC) -p 8081 -n $(SRC_PATH)

.PHONY: format
format:
	uvx ruff check --select I --fix $(RUFF_EXCL)
	uvx ruff format $(RUFF_EXCL)

.PHONY: lint
lint:
	uvx ruff check $(RUFF_EXCL)

.PHONY: lint-fix
lint:
	uvx ruff check --fix $(RUFF_EXCL)

.PHONY: typecheck
typecheck:
	uv run mypy -p $(SRC_PATH)