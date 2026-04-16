---
inclusion: always
description: Python style, code patterns, shell and Docker conventions, and file organization
---

# Coding Conventions

## Python Style

- **Formatter:** Ruff (configured in `pyproject.toml`, target Python 3.12).
- **Type checking:** MyPy with `check_untyped_defs = True` and `warn_unused_configs = True` (configured in `pyproject.toml`). Flywheel SDK imports are allowed without type stubs (`ignore_missing_imports = True`).
- **Interpreter:** Python 3.12+.

## Code Patterns

Follow the conventions established in the existing demo scripts:

- **Logging:** Use `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")` at module level. Get a logger with `log = logging.getLogger("__main__")`.
- **CLI arguments:** Use `argparse` for command-line interfaces. Include `-k`/`--api-key` for the Flywheel API key.
- **API key resolution:** Use the shared `demo/common/fw_auth.py` helper (`get_api_key()`). Never hardcode credentials. The helper checks: CLI flag > env var (`.env` auto-loaded) > OS keyring > interactive prompt.
- **Error handling:** Use `sys.exit(1)` for fatal errors in scripts. Log errors before exiting.
- **Imports:** Use `nacc_common` utilities (`get_center_id`, `get_project`) for Flywheel center/pipeline lookups rather than hardcoding IDs. Import `fw_auth` via the `sys.path` pattern used in existing scripts.

## Shell Scripts

- Use `#!/bin/bash` shebang.
- Use environment variables with defaults (e.g., `ADCID=${ADCID:-0}`) for configuration.
- Validate required environment variables at the top of the script.
- Use meaningful error messages prefixed with `ERROR:`.
- Exit with non-zero codes on failure.

## Docker

- Base images: `python:3.12` or `python:3.12-slim`.
- Install dependencies with `pip install -r requirements.txt` (not Pex).
- Use `/wd` as the working directory for mounted data.
- Use `ENTRYPOINT` for the command and `CMD` for default arguments (so users can override args).

## File Organization

When adding a new demo:
1. Create `demo/<name>/README.md` with usage instructions.
2. Place the Python script directly in `demo/<name>/`.
3. Place Dockerfile (if needed) in `demo/<name>/`.
4. Use the shared `demo/common/fw_auth.py` for API key handling.
5. Add `uv run` commands to the README.

## Dependencies

- Declare Python dependencies in `pyproject.toml` at the repo root.
- Keep `requirements.txt` in sync for Docker builds.
- Use the `nacc-common` package from GitHub releases (wheel format).
- After changing `pyproject.toml`, regenerate the lockfile: `uv lock`.
- Pin or constrain dependency versions (e.g., `flywheel-sdk>=20.0.0`).
