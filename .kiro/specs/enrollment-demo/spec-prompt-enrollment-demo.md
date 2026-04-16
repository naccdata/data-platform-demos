# Spec Prompt: Add Enrollment Upload and Pull Demo

## What

Create a new `demo/enrollment/` demo that shows how to upload enrollment data and pull enrollment-specific errors and QC status from the NACC Data Platform.

## Why

The existing demos cover form data uploads (`python-uploader`), form error pulls (`pull_errors`), form status pulls (`pull_status`), and identifier queries (`pull_identifiers`). Enrollment is a distinct datatype in the platform — `nacc_common.pipeline.get_project()` already supports `datatype="enrollment"` — but there's no demo showing the enrollment submission workflow end to end.

Centers need to submit enrollment data before they can submit visit forms. Having a demo for this fills a gap in the onboarding flow.

## Key details

- Follow the same flat layout as existing demos: `demo/enrollment/README.md`, `demo/enrollment/enroll_upload.py`, `demo/enrollment/enroll_errors.py`
- **enroll_upload.py**: Upload an enrollment CSV file to the enrollment pipeline project. Same pattern as `demo/python-uploader/uploader.py` but using `datatype="enrollment"` in the `get_project()` call.
- **enroll_errors.py**: Pull errors from the enrollment pipeline project. Same pattern as `demo/pull_errors/pull_errors.py` but defaulting `--datatype` to `enrollment`. Should include the `--module` and `--ptid` filtering from the other spec if that lands first, but don't block on it.
- Use the shared `demo/common/fw_auth.py` for API key handling.
- Use `nacc_common.center_info.get_center_id` and `nacc_common.pipeline.get_project` — same abstraction pattern as existing demos.
- Include a sample enrollment CSV or document the expected format in the README.
- CLI flags should follow the conventions of existing demos: `-a/--adcid` (required), `-p/--pipeline`, `-s/--studyid`, `-k/--api-key`, `-o/--output`.
- Add `uv run` commands to the README.

## Relevant files

- `demo/python-uploader/uploader.py` — template for the upload script
- `demo/pull_errors/pull_errors.py` — template for the error pull script
- `demo/common/fw_auth.py` — shared auth helper
- `.venv/lib/python3.13/site-packages/nacc_common/pipeline.py` — `get_project()` with `datatype` param
- `.venv/lib/python3.13/site-packages/nacc_common/error_data.py` — `get_error_data()` / `get_status_data()`
- `.venv/lib/python3.13/site-packages/nacc_common/field_names.py` — enrollment-related field names (ENRLTYPE, PREVENRL, NACCIDKWN, etc.)
- `data/form-data-dummyv1.csv` — existing sample data for reference on format conventions
