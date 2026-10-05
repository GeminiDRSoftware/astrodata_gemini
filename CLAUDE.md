# CLAUDE.md

## Python Environment (REQUIRED)

This project uses a dedicated virtual environment located at **`.adgemini_venv/`** in the project root.
All Python work in this session MUST use this venv. Never use the system Python, a global `pip`,
conda, pyenv shims, or any other virtual environment.

The venv may or may not already be active, depending on how this session was started:

- **Terminal:** the user may have activated `.adgemini_venv` before running `claude`.
  In that case, use plain commands (`python`, `pip`, `pytest`).
- **Desktop app:** the venv cannot be activated beforehand, so use explicit paths
  (`.adgemini_venv/bin/python ...`).

### Step 1: Detect the mode at the start of the session

Before any Python work, run this check once:

```bash
echo "VIRTUAL_ENV=${VIRTUAL_ENV:-<unset>}"; command -v python; python -c "import sys; print(sys.prefix)" 2>/dev/null
```

The venv counts as **ACTIVE** only if all of these are true:

- `VIRTUAL_ENV` is set and ends with `/.adgemini_venv`
- `command -v python` resolves to a path inside `.adgemini_venv`
- `sys.prefix` points inside `.adgemini_venv`

If any of these is false, treat the venv as **NOT ACTIVE**. If `VIRTUAL_ENV` points to a
*different* venv, treat it as NOT ACTIVE and mention this to the user.

State which mode you detected in one short line, then follow the matching rules below for the
rest of the session. Re-run the check if a command behaves unexpectedly.

### Step 2a: Venv ACTIVE (started from an activated terminal)

First, check if PYTHONPATH is set.  If it is set, unset it.

Use the normal commands; they already resolve to the venv:

| Task              | Command                     |
|-------------------|-----------------------------|
| Run Python        | `python script.py`          |
| Install a package | `python -m pip install X`   |
| Run tests         | `python -m nox`             |
| Run a module/tool | `python -m <module>`        |

Do not prefix commands with `.adgemini_venv/bin/` and do not re-activate the venv.

### Step 2b: Venv NOT ACTIVE (e.g. Desktop app)

Call the venv's interpreter by explicit path for every command. Do not rely on
`source activate` carrying over between commands, since shell state may not persist.

| Task              | Command                                       |
|-------------------|-----------------------------------------------|
| Run Python        | `.adgemini_venv/bin/python script.py`         |
| Install a package | `.adgemini_venv/bin/python -m pip install X`  |
| Run tests         | `.adgemini_venv/bin/python -m nox`            |
| Run a module/tool | `.adgemini_venv/bin/python -m <module>`       |

On Windows, replace `.adgemini_venv/bin/` with `.adgemini_venv\Scripts\`.

In this mode, never use bare `python`, `python3`, `pip`, `nox`, or `pytest`.

### Running tests (both modes)

Tests are run through **nox**, which then calls pytest. Use the mode's `python -m nox` form from
the tables above, not pytest directly.

- List available sessions: `python -m nox --list` (or the explicit-path form)
- Run one session: `python -m nox -s <session>`
- Pass arguments through to pytest after `--`, e.g. `python -m nox -s <session> -- -k test_name -x`
- Reuse existing session environments to save time: add `-R` (or `--reuse-existing-virtualenvs`)

nox itself must be installed in `.adgemini_venv`; nox then builds and manages its own session
environments under `.nox/`. Don't install test-only dependencies into `.adgemini_venv` to make
tests pass; they belong in `noxfile.py`. Don't modify or delete `.nox/`.

Only run `pytest` directly (via the venv's interpreter) if the user asks for it, or for a quick
single-test check when nox is clearly unnecessary, and say that you're doing so.

### Rules for both modes

1. **If `.adgemini_venv` is missing or broken**, do NOT create a new venv or fall back to system
   Python. Report the problem to the user and wait for instructions.
2. **Installing dependencies:** only install into `.adgemini_venv`, and mention any new package
   you install. If the project tracks a `requirements.txt`, keep it updated.
3. **Do not modify, delete, or recreate** the `.adgemini_venv/` directory, and do not commit it to git.

## Project Notes

<!-- Add project-specific context below: purpose, key commands, structure, conventions. -->

- **Project:** `astrodata_gemini` is an `astrodata`
  (https://geminidrsoftware.github.io/astrodata/) plugin for accessing data 
  from the Gemini Observatory instruments through the `astrodata` uniform interface.
- **Usage:** @README.md
- **Tests:** nox (see "Running tests" above); main sessions: unit-tests
- **Lint/format:** ruff check ; ruff format --diff
