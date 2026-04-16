---
inclusion: always
description: uv commands for running, linting, type checking, and building Docker images
---

# Build, Lint, and Test

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and script execution.

## Common Commands

```bash
# Install/sync dependencies
uv sync

# Run a demo script
uv run demo/pull_errors/pull_errors.py --adcid 0

# Lint all demo scripts
uv run ruff check demo/

# Format all demo scripts
uv run ruff format demo/

# Type check all demo scripts
uv run mypy demo/ --ignore-missing-imports

# Run tests
uv run pytest tests/ -v

# Regenerate the lockfile after changing pyproject.toml
uv lock
```

## Makefile Shortcuts

```bash
make lint      # uv run ruff check demo/
make format    # uv run ruff format demo/
make check     # uv run mypy demo/ --ignore-missing-imports
make test      # uv run pytest tests/ -v
make all       # lint + check
```

## Building Docker Images

```bash
# Python uploader
docker build -f demo/python-uploader/Dockerfile -t naccdata/python-uploader .

# CLI uploader (x86 only, for Flywheel CLI compatibility)
docker build -f demo/fwcli/Dockerfile --platform linux/amd64 -t naccdata/cli-uploader .

# R uploader
docker build -f demo/r-uploader/Dockerfile -t naccdata/r-uploader .
```

Or use the Makefile:

```bash
make build-python-uploader
make build-cli-uploader
make build-r-uploader
```

## Configuration

- `pyproject.toml` — dependencies, ruff config, mypy config
- `uv.lock` — locked dependency versions (committed to repo)
- `requirements.txt` — runtime deps for Docker builds (keep in sync with pyproject.toml)

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on pushes to `main` and PRs:
1. `uv run ruff check demo/` — linting
2. `uv run mypy demo/ --ignore-missing-imports` — type checking

The workflow uses `astral-sh/setup-uv` for fast uv installation.
