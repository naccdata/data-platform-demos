# Spec Prompt: Add Module and PTID Filtering to pull_errors and pull_status

## What

Add `--module` and `--ptid` command-line flags to the existing `demo/pull_errors/pull_errors.py` and `demo/pull_status/pull_status.py` scripts so users can filter results by module name(s) and/or participant ID(s).

## Why

The `nacc_common.error_data.get_error_data()` and `get_status_data()` functions already accept an optional `modules` parameter that filters by module name (UDS, LBD, FTLD, NP, etc.), but the demo scripts don't expose it. Centers pulling errors for a single module currently get the entire project's errors and have to filter manually.

PTID filtering is supported internally by `ProjectReportVisitor` but not yet exposed through the public functions in `nacc-common` v3.0.0. A request to add it upstream is documented in `docs/nacc-common-v4-prompt.md`. In the meantime, post-filtering on the returned dicts is a reasonable stopgap.

## Key details

- `--module` / `-m`: one or more module names, comma-separated or repeated. Case-insensitive (normalize to uppercase). Passed to `get_error_data(project, modules=set)` / `get_status_data(project, modules=set)`.
- `--ptid` / `-t`: one or more participant IDs, comma-separated or repeated. Since `nacc-common` v3.0.0 doesn't expose ptid filtering publicly, post-filter the returned result dicts by matching the `ptid` key.
- When filters are active, reflect them in the default output filename so filtered and unfiltered outputs don't collide.
- Log active filters at INFO level before pulling data.
- When no filter flags are provided, behavior must be identical to current scripts.
- Update the README files for both demos with usage examples.

## Relevant files

- `demo/pull_errors/pull_errors.py` — existing error pull script
- `demo/pull_status/pull_status.py` — existing status pull script
- `demo/pull_errors/README.md` — error pull docs
- `demo/pull_status/README.md` — status pull docs
- `.venv/lib/python3.13/site-packages/nacc_common/error_data.py` — `get_error_data` / `get_status_data` signatures (modules param already exists)
- `docs/nacc-common-v4-prompt.md` — upstream request for ptid filtering in nacc-common
