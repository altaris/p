PROJECT_NAME	= {{ cookiecutter.project_slug }}
SRC_PATH 		= {{ cookiecutter.project_slug }}
DOCS_PATH 		= docs

UV_RUN			= uv run --frozen
PDOC			= pdoc -d google --math
RUFF_EXCL   	= --exclude '*.ipynb' --exclude 'old/'

.ONESHELL:

all: format typecheck lint-fix lint

.PHONY: docs
docs:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	PDOC_ALLOW_EXEC=1 $(UV_RUN) $(PDOC) --output-directory $(DOCS_PATH) $(SRC_PATH)

.PHONY: docs-serve
docs-serve:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	PDOC_ALLOW_EXEC=1 $(UV_RUN) $(PDOC) -h 0.0.0.0 -p 8081 -n $(SRC_PATH)

.PHONY: docs-serve-static
docs-serve-static: docs
	$(UV_RUN) python -m http.server -d docs 8081

.PHONY: format
format:
	uvx ruff check --select I --fix $(RUFF_EXCL)
	uvx ruff format $(RUFF_EXCL)

.PHONY: install-ipykernel
install-ipykernel:
	uv add --group dev ipykernel
	$(UV_RUN) python -m ipykernel install --user --name $(PROJECT_NAME)

.PHONY: lint
lint:
	uvx ruff check $(RUFF_EXCL)

.PHONY: lint-fix
lint-fix:
	uvx ruff check --fix $(RUFF_EXCL)

.PHONY: shellcheck
shellcheck:
	shellcheck *.sh
	shellcheck **/*.sh

.PHONY: tests
tests:
	PYTHONPATH=. uv run pytest -vv tests

.PHONY: typecheck
typecheck:
	uvx mypy -p $(SRC_PATH)
