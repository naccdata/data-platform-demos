---
inclusion: always
description: NACC Data Platform demos repository structure, dependencies, and environment
---

# Project Overview

This repository contains demonstration code for the **NACC Data Platform**, which is built on top of the Flywheel data management system. The demos show how to programmatically upload data, pull errors, pull QC status, and pull participant identifiers.

## Repository Structure

The repo uses [uv](https://docs.astral.sh/uv/) for dependency management with a single root `pyproject.toml`. Demo modules live under `demo/`:

- `demo/python-uploader/` — Python script for uploading CSV form data
- `demo/fwcli/` — Shell-based uploader using the Flywheel CLI (Docker)
- `demo/r-uploader/` — R script uploader using reticulate (Docker)
- `demo/pull_errors/` — Python script to pull file upload errors (supports `--module` and `--ptid` filtering)
- `demo/pull_status/` — Python script to pull QC status (supports `--module` and `--ptid` filtering)
- `demo/pull_identifiers/` — Python script to pull participant identifiers
- `demo/enrollment/` — Python scripts for enrollment CSV upload and enrollment error retrieval
- `demo/common/` — Shared helper modules (`fw_auth.py` for API key resolution, `filter_helpers.py` for `--module`/`--ptid` CLI filtering)

Each demo follows a flat layout:
```
demo/<name>/
  README.md
  <script>.py       # Main script
  Dockerfile         # Optional, for Docker-based demos
  entrypoint.sh      # Optional, for shell-based demos
```

## Key Dependencies

- **flywheel-sdk** (>=20.0.0) — Flywheel API client
- **nacc-common** (v3.0.0) — NACC utility library for center/pipeline lookups, installed from GitHub release wheel
- **keyring** (>=25.0.0) — OS keyring integration for API key storage
- **python-dotenv** (>=1.0.0) — Auto-loads `.env` files
- Dependencies are declared in `pyproject.toml` and locked via `uv.lock`
- A `requirements.txt` is maintained for Docker builds

## Environment

- **Python >=3.12**
- API key resolution: `--api-key` flag > `FW_API_KEY` env var (`.env` auto-loaded) > OS keyring > interactive prompt
- Scripts are run with `uv run demo/<name>/<script>.py`
