# Implementation Plan: filter-errors-status

## Overview

Add `--module` (`-m`) and `--ptid` (`-t`) CLI flags to `pull_errors.py` and `pull_status.py` so center data managers can filter results by module name and/or participant ID. Core parsing, filtering, and filename logic lives in a new shared helper module (`demo/common/filter_helpers.py`), and both scripts are updated to use it. READMEs are updated with usage examples.

Automated hooks handle linting (ruff), type checking (mypy), formatting, and test execution after each task — no manual checkpoint tasks are needed.

## Tasks

- [x] 1. Set up test infrastructure and dev dependencies
  - [x] 1.1 Add `hypothesis` and `pytest` to the dev dependency group in `pyproject.toml` and regenerate `uv.lock`
    - Add `"hypothesis"` and `"pytest"` to `[dependency-groups] dev` in `pyproject.toml`
    - Run `uv lock` to regenerate the lockfile
    - Run `uv sync` to install new dependencies
    - _Requirements: Design — Testing Strategy / Dev Dependencies_

  - [x] 1.2 Add a `test` target to the `Makefile`
    - Add `test:` target that runs `uv run pytest tests/ -v`
    - Add `test` to the `.PHONY` list
    - _Requirements: Design — Testing Strategy / Running Tests_

- [x] 2. Create the shared filter helpers module
  - [x] 2.1 Create `demo/common/filter_helpers.py` with all helper functions
    - Implement `add_filter_args(parser)` — adds `--module`/`-m` and `--ptid`/`-t` arguments with `action="append"`
    - Implement `collect_modules(raw)` — splits on commas, strips whitespace, uppercases, returns `set[str] | None`
    - Implement `collect_ptids(raw)` — splits on commas, strips whitespace, preserves case, returns `set[str] | None`
    - Implement `log_active_filters(modules, ptids, logger)` — logs active filter values at INFO level
    - Implement `filter_by_ptids(records, ptids)` — post-filters `list[dict[str, Any]]` by the `ptid` key
    - Implement `build_output_filename(prefix, project_label, modules, ptids)` — generates `<prefix>[-<modules>][-ptid-<ptids>]-<project_label>-<date>.csv`
    - Follow the exact signatures and type annotations from the design document
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2.1, 2.2, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [ ]* 2.2 Write property test for `collect_modules`
    - **Property 1: Module collection preserves all non-empty segments as uppercase**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 2.1, 2.2**
    - Create `tests/test_filter_helpers.py`
    - Use Hypothesis to generate arbitrary lists of comma-separated strings
    - Assert that every non-empty stripped segment appears uppercased in the result set, with no extra values

  - [ ]* 2.3 Write property test for `collect_ptids`
    - **Property 2: PTID collection preserves all non-empty segments verbatim**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4**
    - Add to `tests/test_filter_helpers.py`
    - Use Hypothesis to generate arbitrary lists of comma-separated strings
    - Assert that every non-empty stripped segment appears verbatim (case-preserved) in the result set

  - [x] 2.4 Write property test for `filter_by_ptids`
    - **Property 3: PTID post-filter retains exactly the matching records**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**
    - Add to `tests/test_filter_helpers.py`
    - Use Hypothesis to generate lists of record dicts and optional PTID sets
    - Assert that when ptids is not None, result contains exactly records with matching `ptid` values in original order; when None, all records are returned

  - [x] 2.5 Write property test for `build_output_filename`
    - **Property 4: Output filename includes sorted filter segments**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**
    - Add to `tests/test_filter_helpers.py`
    - Use Hypothesis to generate prefix, project_label, optional module sets, optional PTID sets
    - Assert sorted module names and `ptid-`-prefixed sorted PTIDs appear in the filename; ends with `.csv`; no filter segments when both sets are None

  - [x] 2.6 Write unit tests for filter helpers
    - Create `tests/test_filter_helpers_unit.py`
    - Test `-m` short alias for `--module` via `add_filter_args` (Requirements 1.5, 1.6)
    - Test `-t` short alias for `--ptid` via `add_filter_args` (Requirements 4.5, 4.6)
    - Test `log_active_filters` logs modules at INFO level (Requirements 6.1, 6.3)
    - Test `log_active_filters` logs PTIDs at INFO level (Requirements 6.2, 6.4)
    - Test `log_active_filters` produces no output when no filters active
    - Test `build_output_filename` with no filters produces `<prefix>-<label>-<date>.csv` (Requirements 7.5, 7.6)
    - Test `collect_modules` returns None for empty/whitespace-only input
    - Test `collect_ptids` returns None for empty/whitespace-only input
    - Test `filter_by_ptids` excludes records missing the `ptid` key when filter is active

- [x] 3. Integrate filter helpers into `pull_errors.py`
  - [x] 3.1 Update `demo/pull_errors/pull_errors.py` to use filter helpers
    - Import `filter_helpers` from `demo/common/` using the existing `sys.path` pattern
    - Call `add_filter_args(parser)` after existing argument definitions
    - After obtaining the project, call `collect_modules(args.module)` and `collect_ptids(args.ptid)`
    - Call `log_active_filters(modules, ptids, log)` before requesting data
    - Pass `modules=module_set` to `get_error_data()` only when module_set is not None
    - Call `filter_by_ptids(table, ptid_set)` on the returned data
    - Replace the default filename logic with `build_output_filename("errors", source_project.label, module_set, ptid_set)`
    - Preserve the `--output` flag override behavior
    - _Requirements: 1.1, 1.2, 1.5, 2.1, 3.1, 3.3, 4.1, 4.2, 4.5, 5.1, 5.3, 6.1, 6.2, 7.1, 7.2, 7.5, 7.7, 8.1_

  - [ ]* 3.2 Write integration tests for `pull_errors.py` filter wiring
    - Create `tests/test_scripts_integration.py`
    - Mock `nacc_common` and Flywheel dependencies
    - Test that `--module` values are passed to `get_error_data(project, modules=...)` (Requirement 3.1)
    - Test that without `--module`, `get_error_data` is called without `modules` param (Requirement 3.3)
    - Test backward compatibility — no filter flags produces identical behavior (Requirement 8.1)

- [x] 4. Integrate filter helpers into `pull_status.py`
  - [x] 4.1 Update `demo/pull_status/pull_status.py` to use filter helpers
    - Import `filter_helpers` from `demo/common/` using the existing `sys.path` pattern
    - Call `add_filter_args(parser)` after existing argument definitions
    - After obtaining the project, call `collect_modules(args.module)` and `collect_ptids(args.ptid)`
    - Call `log_active_filters(modules, ptids, log)` before requesting data
    - Pass `modules=module_set` to `get_status_data()` only when module_set is not None
    - Call `filter_by_ptids(table, ptid_set)` on the returned data
    - Replace the default filename logic with `build_output_filename("qc-status", source_project.label, module_set, ptid_set)`
    - Preserve the `--output` flag override behavior
    - _Requirements: 1.3, 1.4, 1.6, 2.2, 3.2, 3.4, 4.3, 4.4, 4.6, 5.2, 5.4, 6.3, 6.4, 7.3, 7.4, 7.6, 7.8, 8.2_

  - [ ]* 4.2 Write integration tests for `pull_status.py` filter wiring
    - Add to `tests/test_scripts_integration.py`
    - Mock `nacc_common` and Flywheel dependencies
    - Test that `--module` values are passed to `get_status_data(project, modules=...)` (Requirement 3.2)
    - Test that without `--module`, `get_status_data` is called without `modules` param (Requirement 3.4)
    - Test backward compatibility — no filter flags produces identical behavior (Requirement 8.2)

- [x] 5. Update README documentation
  - [x] 5.1 Update `demo/pull_errors/README.md` with filter usage examples
    - Add a "Filtering results" section after existing usage instructions
    - Include example with `--module` flag for a single module (Requirement 9.1)
    - Include example with `--ptid` flag for one or more participant IDs (Requirement 9.2)
    - Include example combining `--module` and `--ptid` flags (Requirement 9.3)
    - _Requirements: 9.1, 9.2, 9.3_

  - [x] 5.2 Update `demo/pull_status/README.md` with filter usage examples
    - Add a "Filtering results" section after existing usage instructions
    - Include example with `--module` flag for a single module (Requirement 9.4)
    - Include example with `--ptid` flag for one or more participant IDs (Requirement 9.5)
    - Include example combining `--module` and `--ptid` flags (Requirement 9.6)
    - _Requirements: 9.4, 9.5, 9.6_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Automated hooks handle linting, type checking, formatting, and test execution after each task
- Property tests validate universal correctness properties from the design document
- Unit and integration tests validate specific examples, edge cases, and script wiring
