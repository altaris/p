---
description:
  Review only the code you wrote this session for logic/correctness, run make,
  fix, loop until clean, then commit
argument-hint: [optional scope or commit-message hint]
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

Review, verify, and commit **only the code you authored in this session**. The
working tree may also hold edits by the user or other agents — never touch
those.

## 1. Establish scope

Reconstruct from this conversation the files and hunks you created or edited,
then reconcile against `git status`, `git diff`, and `git diff --staged`.

**Exclude** anything else: hunks flagged in the conversation as user- or
linter-modified, other agents' work, and pre-existing uncommitted changes. If
you are unsure whether a hunk is yours, it is **not** yours — leave it alone and
ask before including it.

If `$ARGUMENTS` is non-empty, use it as a hint for the scope and/or the commit
message.

State the scope explicitly before proceeding: list the files (and specific
hunks, when a file mixes your work with others'). If nothing is in scope, say so
and stop — do not commit.

## 2. Review logic & correctness

For the in-scope code only — this is the point of the command, not a rubber
stamp:

- Trace the logic: edge cases, off-by-one, tensor shapes/dtypes, `None`/empty
  handling, error paths, resource cleanup, silent truncation.
- Confirm it does what the instructions that produced it asked for.
- Confirm it follows the conventions in `CLAUDE.md` — including the
  Lightning-free-core boundary, relative imports inside the package, loguru
  brace-style logging, and the docstring markup rules.
- Look for what breaks at **runtime**, not just at type-check time.

Fix every issue you find, editing only in-scope code.

## 3. Verify with checks (loop)

Run the `CLAUDE.md` checks for the files you touched: **`make`** for code under
`milx_gbg/`, the per-file `uvx ruff` / `uvx mypy` commands for standalone
scripts, `shellcheck` for shell scripts. Never standalone `ruff`/`mypy` on
package code.

Fix complaints **in your code** and re-run. **Loop** review → fix → checks until
clean. If a failure is in code you did **not** author, do not modify it — stop
and report rather than committing on top of a broken tree.

## 4. Commit

Once the review is clean and the checks pass (invoking this command authorizes
this one commit):

- Stage **only your in-scope files** by explicit path (`git add <path> …`) —
  never `git add -A`, and never stage others' work or untracked files you
  weren't asked to.
- Follow the `CLAUDE.md` commit policy: conventional-commit subject
  (`feat(scope): …` / `fix(scope): …` / bare `scope: …`), imperative mood, no
  trailing period, ≤ 70 chars; body explaining _why_ only when not self-evident;
  end with the required `Co-Authored-By` trailer.
- Report the commit hash, and list what was left uncommitted and why.
