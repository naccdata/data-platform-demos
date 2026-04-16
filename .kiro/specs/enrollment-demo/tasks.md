# Implementation Plan: Enrollment Demo Scripts

## Overview

Create a `demo/enrollment/` directory with two CLI scripts (`enroll_upload.py` and `enroll_errors.py`) and a `README.md`. Both scripts mirror existing demos but hardcode `datatype="enrollment"` instead of exposing a `--datatype` flag. All shared helpers (`fw_auth`, `filter_helpers`, `nacc_common`) are reused without modification.

## Tasks

- [x] 1. Create `demo/enrollment/enroll_upload.py`
  - [x] 1.1 Scaffold `enroll_upload.py` with imports and logging setup
    - Create `demo/enrollment/enroll_upload.py`
    - Add module docstring describing the script purpose
    - Add `sys.path.insert(0, ...)` pattern pointing to `demo/common/` (same as `uploader.py`)
    - Import `fw_auth.get_api_key`, `nacc_common.center_info.get_center_id`, `CenterError`, `flywheel.Client`, `nacc_common.pipeline.get_project`
    - Configure `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")` and `log = logging.getLogger("__main__")`
    - _Requirements: 5.1, 5.4, 5.6, 7.1_

  - [x] 1.2 Implement argparse CLI for enrollment upload
    - Add `argparse.ArgumentParser` with description `"Upload enrollment CSV file"`
    - Add required `-a`/`--adcid` (int, choices 0–99)
    - Add optional `-p`/`--pipeline` (choices `ingest`/`sandbox`, default `sandbox`)
    - Add optional `-s`/`--studyid` (default `adrc`)
    - Add optional `-k`/`--api-key`
    - Add required positional `filepath` argument
    - Do NOT add a `--datatype` flag
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x] 1.3 Implement the upload main function
    - Resolve API key via `get_api_key(args.api_key)`
    - Create `flywheel.Client(api_key)` with connection check; log error and `sys.exit(1)` on failure
    - Look up center group ID via `get_center_id(client=client, adcid=str(args.adcid))`; catch `CenterError`, log, and `sys.exit(1)`
    - Call `get_project(client=client, group_id=group_id, datatype="enrollment", pipeline_type=args.pipeline, study_id=args.studyid)` — hardcode `datatype="enrollment"`
    - Exit with error if no project found
    - Validate file exists (`os.path.exists`) and is non-empty (`os.path.getsize > 0`); log and exit on failure
    - Upload via `upload_project.upload_file(args.filepath)` and log filename and byte count
    - Add `if __name__ == "__main__": main()` guard
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9_

- [x] 2. Create `demo/enrollment/enroll_errors.py`
  - [x] 2.1 Scaffold `enroll_errors.py` with imports and logging setup
    - Create `demo/enrollment/enroll_errors.py`
    - Add module docstring describing the script purpose
    - Add `sys.path.insert(0, ...)` pattern pointing to `demo/common/`
    - Import `filter_helpers`, `fw_auth.get_api_key`, `nacc_common.center_info.get_center_id`, `CenterError`, `nacc_common.error_data.ERROR_HEADER_NAMES`, `nacc_common.error_data.get_error_data`, `flywheel.Client`, `nacc_common.pipeline.get_project`
    - Import `csv.DictWriter`
    - Configure `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")` and `log = logging.getLogger("__main__")`
    - _Requirements: 5.2, 5.5, 5.7, 7.2_

  - [x] 2.2 Implement argparse CLI for enrollment error pull
    - Add `argparse.ArgumentParser` with description `"Pull enrollment errors from pipeline project"`
    - Add required `-a`/`--adcid` (int, choices 0–99)
    - Add optional `-p`/`--pipeline` (choices `ingest`/`sandbox`, default `sandbox`)
    - Add optional `-s`/`--studyid` (default `adrc`)
    - Add optional `-k`/`--api-key`
    - Add optional `-o`/`--output` (default `None`)
    - Call `filter_helpers.add_filter_args(parser)` for `-m`/`--module` and `-t`/`--ptid`
    - Do NOT add a `--datatype` flag
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.8_

  - [x] 2.3 Implement the error pull main function
    - Resolve API key via `get_api_key(args.api_key)`
    - Create `flywheel.Client(api_key)` with connection check; log error and `sys.exit(1)` on failure
    - Look up center group ID via `get_center_id(client=client, adcid=str(args.adcid))`; catch `CenterError`, log, and `sys.exit(1)`
    - Call `get_project(client=client, group_id=group_id, datatype="enrollment", pipeline_type=args.pipeline, study_id=args.studyid)` — hardcode `datatype="enrollment"`
    - Exit with error if no project found
    - Collect filter sets: `filter_helpers.collect_modules(args.module)` and `filter_helpers.collect_ptids(args.ptid)`
    - Log active filters via `filter_helpers.log_active_filters(module_set, ptid_set, log)`
    - Build `error_kwargs` dict, pass module filter to `get_error_data(source_project, **error_kwargs)`
    - If no error records, log info and return
    - Post-filter by PTID via `filter_helpers.filter_by_ptids(table, ptid_set)`
    - If no records after filtering, log info and return
    - Generate output path using `filter_helpers.build_output_filename("enrollment-errors", source_project.label, module_set, ptid_set)` when `--output` not provided
    - Write CSV with `DictWriter(out_file, fieldnames=ERROR_HEADER_NAMES, dialect="unix")`
    - Add `if __name__ == "__main__": main()` guard
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 4.7, 7.3_

- [x] 3. Create `demo/enrollment/README.md`
  - Write the enrollment demo README with the following sections:
    - Title and purpose/overview of the enrollment demo
    - Link to the top-level README for environment setup prerequisites
    - Note that all commands are run from the repository root directory
    - Upload usage section with `uv run demo/enrollment/enroll_upload.py` examples (including `--adcid`, `--pipeline`, and filepath arguments)
    - Error pull usage section with `uv run demo/enrollment/enroll_errors.py` examples
    - Document `--module` and `--ptid` filtering options with examples of comma-separated and repeated flag usage
    - Expected enrollment CSV format section listing columns (`module`, `adcid`, `ptid`, plus enrollment-specific fields)
    - Reference to `demo/pull_identifiers/` for enrollment identifier queries
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_

- [x] 4. Lint and type-check the new scripts
  - Run `uv run ruff check demo/enrollment/` and fix any issues
  - Run `uv run mypy demo/enrollment/ --ignore-missing-imports` and fix any issues
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

## Notes

- Both scripts hardcode `datatype="enrollment"` — no `--datatype` flag is exposed
- The default output filename prefix for error pull is `enrollment-errors` (not `errors`)
- No new shared libraries or data models are introduced; all existing helpers are reused as-is
- Each task references specific acceptance criteria from the requirements document for traceability
