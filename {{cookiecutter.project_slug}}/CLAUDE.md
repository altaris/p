# General Coding Philosophy

- **Language**: English for code, comments, and documentation
- **Modify only what's relevant**: only change code related to the task, even if
  you spot other potential improvements
- **Readable over clever**: prefer clear code to ultra-concise code
- **Understand the task**: distinguish prompts calling for code from prompts
  calling for explanation
- **Reread notebooks before editing**: reread the whole notebook's code cells
  first — the user edits cells directly between turns, so a stale in-context
  copy clobbers their work

# Project Layout

Package `{{ cookiecutter.project_slug }}/`, Python `{{ cookiecutter.python_version }}`,
managed with **uv**.

- **`{{ cookiecutter.project_slug }}/`**: the package itself.
  `__main__.py` (Click CLI root), `logging.py` (loguru setup).
- **`debug.py`**: root-level debugging entrypoint that calls the CLI directly.
- **`tests/`**: pytest suite, run with `make tests`.
- **Standalone scripts** (e.g. a `scripts/` directory), when present: run as
  `uv run scripts/<name>.py` and import the package absolutely.

# Critical Developer Workflows

## Development Commands

- `make` / `make all`: format (Ruff) → typecheck (mypy) → lint-fix → lint
- `make tests`: run the pytest suite
- `make docs-serve`: build & serve pdoc docs at http://localhost:8081 (Google
  style, math enabled)
- `make install-ipykernel`: register the venv as a Jupyter kernel
  `{{ cookiecutter.project_slug }}`
- `uv sync --frozen --all-groups`: install all dependencies

Ruff and mypy run through `uvx` (see the `Makefile`); Ruff excludes `*.ipynb`
and `old/`.

## After Editing Code

Run the checks through **`make`** after every edit — never standalone `ruff` /
`mypy`.

- Files under **`{{ cookiecutter.project_slug }}/`**: `make`. Granular targets:
  `make format`, `make typecheck`, `make lint` / `make lint-fix`.
- **Standalone scripts**, per file: `uvx ruff check --select I --fix`,
  `uvx ruff format`, `uvx ruff check`, `uvx mypy`.
- **Shell scripts**: `shellcheck FILE` (or `make shellcheck`).

Always fix the errors before considering the task done. Do not rely on Ruff
alone.

# Repo Workflow

- Single long-lived branch **`master`** on `origin` (GitHub). Committing
  directly to `master` is the norm — no mandatory feature-branch / PR flow.
- Merge commits are fine when a branch is used; linear history is not required.
- Commit and push only when explicitly asked (see Commit Policy).

# Commit Policy

**You are NOT allowed to create commits unless EXPLICITLY instructed to do so.**
Never commit at the end of a task on your own initiative — wait for a direct
instruction. Never amend an existing commit unless explicitly asked.

A composite instruction like "commit X, then do Y" authorizes the commit for X
only. Y still needs its own explicit commit instruction.

## Subject line

Conventional commits, two flavors:

- `feat(scope): subject` for new features, `fix(scope): subject` for bug fixes
- `scope: subject` (bare scope, no `refactor`/`chore`/etc.) for refactors,
  cleanups, renames, deletions, doc tweaks — the dominant style

`scope` is the affected subpackage or filename (multi-word is fine); omit it
only for genuinely project-wide changes. Imperative mood, no trailing period, ≤
70 characters when possible.

## Body

Optional — omit when the subject is self-explanatory (e.g. "drop unused X").
When present, explain _why_; the diff already shows _what_. Present tense, no
markdown headers, wrap around 72 characters.

## Splitting work into logical commits

When asked for "commits" (plural) or "logical commits", split the working tree
into one focused commit per concern. Each commit should touch a single
subpackage or concept and be independently revertible. Files sharing a purpose
belong together — a "move X from A to B" commit spans A, B, and its callers.
Deletions, moves, and refactors are usually separate commits even when they sit
in the same working tree.

## Staging

- Leave unrelated modifications you didn't make alone — they're someone else's
  in-progress work
- Never stage untracked files (notebooks, secrets, generated archives,
  hand-edited one-off scripts) unless explicitly asked
- Auto-formatting from `make` on a file you touched is fine to include; don't
  sweep formatting churn from unrelated files into your commit

# Code Conventions

Ruff runs the **`ALL`** ruleset with a curated ignore list in `pyproject.toml`;
mypy runs with `disallow_untyped_defs`. Line length **79**, double quotes, space
indent. Those mechanical rules are enforced by `make` — the sections below
capture the judgment calls the toolchain can't.

## Python Style

- **Target modern Python** (`{{ cookiecutter.python_version }}`): builtin
  generics (`list[str]`), PEP 604 unions (`str | None`), `collections.abc` ABCs
  (`Sequence`, `Callable`), `pathlib.Path` over `os.path`. Never `typing.List` /
  `Optional[...]`. `Any` is banned in call signatures (ANN401) — annotate
  concretely there and keep `Any` / `cast` for genuinely dynamic values;
  `Literal` for string-enum parameters
- **Naming**: `snake_case` (lowercase only); avoid ambiguous single chars like
  `l`. Short names OK when clear
- **Symbol organization**: group top-level symbols by kind (constants,
  functions, classes), alphabetize each group, classes last; keep `__all__`
  alphabetized. No separator comments like `# ----- CLASSES`
- **Class attributes**: declare each instance attribute as a class-level
  annotation (no value) before `__init__`, alphabetized; private (`_foo`) in a
  separate block after the public ones
- **Shape comments**: annotate tensor ops inline, e.g. `# (B, C, H, W)`
- **`pathlib.Path`** for all filesystem paths and I/O. Name file context
  managers `fp`: `with open(path, "rt", encoding="utf8") as fp:`
- **Relative imports** — IMPORTANT: inside `{{ cookiecutter.project_slug }}/`,
  always `from .module import symbol`, never
  `from {{ cookiecutter.project_slug }}.module import symbol`. Scripts outside
  the package import it absolutely
- **Import aliases**: `np`, `Path`, `Image` (PIL), `nx`, `tqdm` (`tqdm.auto`),
  `sns`, `nn` / `nnf` (`torch.nn` / `torch.nn.functional`), `tr`
  (`torchvision.transforms.functional`), `pl` (`lightning`). No single-letter
  aliases (no `torch.nn.functional as F`)
- **Lazy imports**: import inside a function/method when both hold: the import
  is heavy (torch, datasets, lightning), and it's used in few enough places that
  the repetition stays minimal. A heavy import needed across many methods goes
  at module level instead
- **Walrus operator**: the user likes `:=` — use it whenever it avoids
  repeating an expression or an extra line, e.g.
  ```python
  if (match := pattern.search(line)) is not None:  # ✅
      ...
  while (chunk := fp.read(4096)):  # ✅
      ...
  ```
- **Same-line assignment and unpacking**: the user likes these — group related
  initializations on one line rather than stacking them, and unpack in one go:
  ```python
  list1, list2, n = [], [], 0  # ✅
  width, height = image.size  # ✅
  ```
  Keep it to genuinely related variables, and split when the line would exceed
  79 characters or the grouping stops being obvious

## Docstrings

Google style, rendered by **pdoc**. Sections: `Args:` / `Returns:` / `Raises:` /
`Examples:` (doctests go in `Examples:`); omit `Returns:` when self-explanatory.
Multi-line docstrings put the summary on the opening `"""` line (D212).

- **Markup**: single backticks for symbols pdoc should cross-link
  (`` `{{ cookiecutter.project_slug }}.logging.setup_logging` ``); double
  backticks for literals, values, and shell/CLI text (` ``"hub"`` `,
  ` ``uv run scripts/train.py`` `). Tensor shapes in backticks:
  `` `(B, C, H, W)` ``. LaTeX for math
- **Module docstrings carry the design rationale** — what the module is for, how
  it composes with the rest of the package, and what the caller is expected to
  build themselves

## Logging (loguru)

- IMPORTANT: always `from loguru import logger as logging` — never stdlib
  `logging`
- Brace-style with argument binding, never f-strings:
  ```python
  logging.info("Processed {} items in {}", count, elapsed)  # ✅
  logging.info(f"Processed {count} items")  # ❌
  ```
- `logging.success(...)` for completion messages
- `@logging.catch` on the top-level CLI entrypoint
- Central `setup_logging` lives in `{{ cookiecutter.project_slug }}/logging.py`
  (rank-zero filter for DDP, tqdm-compatible sink) — call it rather than
  reconfiguring loguru ad hoc

## CLI (Click)

- One Click **group per subpackage** in `<subpackage>/cli.py`, registered on the
  root group in `__main__.py` via `main.add_command(...)`
- **Lazy imports**: import heavy implementations inside the command body, not at
  module top, so `{{ cookiecutter.project_slug }}` stays fast to import
- Options: `click.Path(..., path_type=Path)` with `exists=` / `file_okay=`
  flags; `show_default=True` and a helpful `help=` on every option;
  `multiple=True` for repeatable options (param typed `tuple[str, ...]`);
  `is_flag=True` (or `--x/--no-x`) for booleans
- Parse structured option values in a module-private `_parse_*` callback that
  re-raises failures as `click.BadParameter`
