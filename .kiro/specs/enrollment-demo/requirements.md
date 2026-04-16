# Requirements Document

## Introduction

Create a new `demo/enrollment/` demo that shows how to upload enrollment CSV data and pull enrollment-specific errors from the NACC Data Platform. Enrollment is a distinct datatype in the platform — centers must submit enrollment data before they can submit visit forms. The existing demos cover form data uploads and error pulls but there is no dedicated enrollment demo. This feature fills that gap in the onboarding flow.

## Glossary

- **Enrollment_Uploader**: The `enroll_upload.py` script that uploads an enrollment CSV file to the enrollment pipeline project on the NACC Data Platform.
- **Enrollment_Error_Puller**: The `enroll_errors.py` script that pulls error data from the enrollment pipeline project and writes it to a CSV file.
- **ADCID**: Alzheimer's Disease Center Identifier, a numeric center identifier (0–99) used to look up the Flywheel group for a center.
- **Pipeline_Project**: A Flywheel project resolved via `nacc_common.pipeline.get_project()` using center group ID, datatype, pipeline type, and study ID.
- **Flywheel_Client**: The Flywheel SDK client object used to interact with the NACC Data Platform API.
- **API_Key**: The Flywheel API key resolved by `demo/common/fw_auth.py` using priority order: CLI flag, environment variable, OS keyring, interactive prompt.
- **Enrollment_CSV**: A CSV file containing enrollment data with columns such as `module`, `adcid`, `ptid`, and enrollment-specific fields.
- **Demo_README**: The `demo/enrollment/README.md` file that documents usage, expected CSV format, and `uv run` commands.

## Requirements

### Requirement 1: Enrollment Upload Script

**User Story:** As a center data manager, I want to upload an enrollment CSV file to the NACC Data Platform, so that I can submit enrollment data for my center.

#### Acceptance Criteria

1. WHEN the user invokes `enroll_upload.py` with a valid `--adcid` and a file path, THE Enrollment_Uploader SHALL resolve the API_Key using `demo/common/fw_auth.py`.
2. WHEN the API_Key is resolved, THE Enrollment_Uploader SHALL create a Flywheel_Client and look up the center group ID using `nacc_common.center_info.get_center_id`.
3. WHEN the center group ID is resolved, THE Enrollment_Uploader SHALL call `nacc_common.pipeline.get_project` with `datatype="enrollment"` and the user-supplied pipeline type and study ID to obtain the Pipeline_Project.
4. WHEN a valid Pipeline_Project is obtained and the file exists and is non-empty, THE Enrollment_Uploader SHALL upload the file to the Pipeline_Project and log the file name and byte count.
5. IF the Flywheel_Client cannot be created, THEN THE Enrollment_Uploader SHALL log an error message and exit with code 1.
6. IF `get_center_id` raises a CenterError, THEN THE Enrollment_Uploader SHALL log the error message and exit with code 1.
7. IF no Pipeline_Project is found for the center, THEN THE Enrollment_Uploader SHALL log an error message and exit with code 1.
8. IF the specified file does not exist, THEN THE Enrollment_Uploader SHALL log an error message and exit with code 1.
9. IF the specified file is empty, THEN THE Enrollment_Uploader SHALL log an error message and exit with code 1.

### Requirement 2: Enrollment Upload CLI Interface

**User Story:** As a center data manager, I want clear CLI flags for the enrollment upload script, so that I can run it consistently with other demos.

#### Acceptance Criteria

1. THE Enrollment_Uploader SHALL accept a required `-a`/`--adcid` argument of type integer in the range 0–99.
2. THE Enrollment_Uploader SHALL accept an optional `-p`/`--pipeline` argument with choices `ingest` and `sandbox`, defaulting to `sandbox`.
3. THE Enrollment_Uploader SHALL accept an optional `-s`/`--studyid` argument defaulting to `adrc`.
4. THE Enrollment_Uploader SHALL accept an optional `-k`/`--api-key` argument for the Flywheel API key.
5. THE Enrollment_Uploader SHALL accept a required positional `filepath` argument specifying the path to the CSV file to upload.
6. THE Enrollment_Uploader SHALL use `datatype="enrollment"` when calling `get_project`, without exposing a `--datatype` flag to the user.

### Requirement 3: Enrollment Error Pull Script

**User Story:** As a center data manager, I want to pull enrollment-specific errors from the NACC Data Platform, so that I can identify and fix issues in my enrollment submissions.

#### Acceptance Criteria

1. WHEN the user invokes `enroll_errors.py` with a valid `--adcid`, THE Enrollment_Error_Puller SHALL resolve the API_Key using `demo/common/fw_auth.py`.
2. WHEN the API_Key is resolved, THE Enrollment_Error_Puller SHALL create a Flywheel_Client and look up the center group ID using `nacc_common.center_info.get_center_id`.
3. WHEN the center group ID is resolved, THE Enrollment_Error_Puller SHALL call `nacc_common.pipeline.get_project` with `datatype="enrollment"` and the user-supplied pipeline type and study ID to obtain the Pipeline_Project.
4. WHEN a valid Pipeline_Project is obtained, THE Enrollment_Error_Puller SHALL call `nacc_common.error_data.get_error_data` on the Pipeline_Project, passing the module filter set when provided.
5. WHEN error data is returned, THE Enrollment_Error_Puller SHALL post-filter records by PTID using `filter_helpers.filter_by_ptids` when a PTID filter is active.
6. WHEN filtered error records exist, THE Enrollment_Error_Puller SHALL write the records to a CSV file using `csv.DictWriter` with `ERROR_HEADER_NAMES` as fieldnames and `unix` dialect.
7. IF the Flywheel_Client cannot be created, THEN THE Enrollment_Error_Puller SHALL log an error message and exit with code 1.
8. IF `get_center_id` raises a CenterError, THEN THE Enrollment_Error_Puller SHALL log the error message and exit with code 1.
9. IF no Pipeline_Project is found for the center, THEN THE Enrollment_Error_Puller SHALL log an error message and exit with code 1.
10. IF no error records exist after retrieval, THEN THE Enrollment_Error_Puller SHALL log an informational message and return without writing a file.
11. IF no error records remain after PTID filtering, THEN THE Enrollment_Error_Puller SHALL log an informational message and return without writing a file.

### Requirement 4: Enrollment Error Pull CLI Interface

**User Story:** As a center data manager, I want clear CLI flags for the enrollment error pull script, so that I can filter and customize error output.

#### Acceptance Criteria

1. THE Enrollment_Error_Puller SHALL accept a required `-a`/`--adcid` argument of type integer in the range 0–99.
2. THE Enrollment_Error_Puller SHALL accept an optional `-p`/`--pipeline` argument with choices `ingest` and `sandbox`, defaulting to `sandbox`.
3. THE Enrollment_Error_Puller SHALL accept an optional `-s`/`--studyid` argument defaulting to `adrc`.
4. THE Enrollment_Error_Puller SHALL accept an optional `-k`/`--api-key` argument for the Flywheel API key.
5. THE Enrollment_Error_Puller SHALL accept optional `-m`/`--module` and `-t`/`--ptid` filter arguments via `filter_helpers.add_filter_args`.
6. THE Enrollment_Error_Puller SHALL accept an optional `-o`/`--output` argument for a custom output file path.
7. WHEN no `--output` is provided, THE Enrollment_Error_Puller SHALL generate a default filename using `filter_helpers.build_output_filename` with prefix `enrollment-errors`, incorporating active module and PTID filters.
8. THE Enrollment_Error_Puller SHALL use `datatype="enrollment"` when calling `get_project`, without exposing a `--datatype` flag to the user.

### Requirement 5: Directory Layout and Shared Imports

**User Story:** As a developer, I want the enrollment demo to follow the same flat layout and import patterns as existing demos, so that the codebase stays consistent.

#### Acceptance Criteria

1. THE Enrollment_Uploader SHALL reside at `demo/enrollment/enroll_upload.py`.
2. THE Enrollment_Error_Puller SHALL reside at `demo/enrollment/enroll_errors.py`.
3. THE Demo_README SHALL reside at `demo/enrollment/README.md`.
4. THE Enrollment_Uploader SHALL import `fw_auth.get_api_key` from `demo/common/` using the `sys.path.insert` pattern established by existing demo scripts.
5. THE Enrollment_Error_Puller SHALL import `fw_auth.get_api_key` and `filter_helpers` from `demo/common/` using the `sys.path.insert` pattern established by existing demo scripts.
6. THE Enrollment_Uploader SHALL use `nacc_common.center_info.get_center_id` and `nacc_common.pipeline.get_project` for center and project lookups.
7. THE Enrollment_Error_Puller SHALL use `nacc_common.center_info.get_center_id`, `nacc_common.pipeline.get_project`, and `nacc_common.error_data.get_error_data` for center, project, and error lookups.

### Requirement 6: README Documentation

**User Story:** As a center data manager, I want a README that documents usage, expected enrollment CSV format, and `uv run` commands, so that I can use the enrollment demo without reading the source code.

#### Acceptance Criteria

1. THE Demo_README SHALL include a description of the enrollment demo purpose.
2. THE Demo_README SHALL include `uv run` commands for running `enroll_upload.py` with example arguments.
3. THE Demo_README SHALL include `uv run` commands for running `enroll_errors.py` with example arguments.
4. THE Demo_README SHALL document the expected enrollment CSV format, listing required columns such as `module`, `adcid`, and `ptid`.
5. THE Demo_README SHALL document the `--module` and `--ptid` filtering options for `enroll_errors.py`, including examples of comma-separated and repeated flag usage.
6. THE Demo_README SHALL include a reference to the top-level README for environment setup.
7. THE Demo_README SHALL note that all commands are run from the repository root directory.

### Requirement 7: Logging Convention

**User Story:** As a developer, I want the enrollment scripts to follow the same logging conventions as other demos, so that log output is consistent across the project.

#### Acceptance Criteria

1. THE Enrollment_Uploader SHALL configure logging with `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")` at module level.
2. THE Enrollment_Error_Puller SHALL configure logging with `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")` at module level.
3. WHEN filter arguments are active, THE Enrollment_Error_Puller SHALL log active filters using `filter_helpers.log_active_filters`.
