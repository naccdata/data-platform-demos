# Requirements Document

## Introduction

The `pull_errors.py` and `pull_status.py` demo scripts currently pull all error and QC-status data for an entire pipeline project. Centers working with a single module (e.g., UDS) or investigating a specific participant must download everything and filter manually. This feature adds `--module` and `--ptid` command-line flags to both scripts so users can request only the data they need, and updates the default output filenames to reflect active filters.

## Glossary

- **Pull_Errors_Script**: The Python CLI script at `demo/pull_errors/pull_errors.py` that retrieves file-processing error data from a pipeline project.
- **Pull_Status_Script**: The Python CLI script at `demo/pull_status/pull_status.py` that retrieves QC-status data from a pipeline project.
- **Module**: A data-collection module identifier used by the NACC Data Platform (e.g., UDS, LBD, FTLD, NP). Module names are case-insensitive and stored in uppercase.
- **PTID**: A participant identifier string used to associate data files with individual research participants.
- **Filter_Set**: The combined set of zero or more module names and zero or more PTIDs supplied via CLI flags for a single invocation.
- **Default_Output_Filename**: The automatically generated CSV filename used when the user does not supply the `--output` flag.

## Requirements

### Requirement 1: Module filter flag

**User Story:** As a center data manager, I want to specify one or more module names on the command line, so that I only retrieve errors or status records for the modules I care about.

#### Acceptance Criteria

1. WHEN the `--module` flag is provided with one or more comma-separated module names, THE Pull_Errors_Script SHALL split the value on commas and collect each name into a module Filter_Set.
2. WHEN the `--module` flag is provided multiple times, THE Pull_Errors_Script SHALL merge all supplied values into a single module Filter_Set.
3. WHEN the `--module` flag is provided with one or more comma-separated module names, THE Pull_Status_Script SHALL split the value on commas and collect each name into a module Filter_Set.
4. WHEN the `--module` flag is provided multiple times, THE Pull_Status_Script SHALL merge all supplied values into a single module Filter_Set.
5. THE Pull_Errors_Script SHALL accept `-m` as a short alias for `--module`.
6. THE Pull_Status_Script SHALL accept `-m` as a short alias for `--module`.

### Requirement 2: Module name normalization

**User Story:** As a center data manager, I want module names to be treated case-insensitively, so that I do not have to remember the exact casing.

#### Acceptance Criteria

1. WHEN a module name is received from the command line, THE Pull_Errors_Script SHALL normalize the module name to uppercase before using it for filtering.
2. WHEN a module name is received from the command line, THE Pull_Status_Script SHALL normalize the module name to uppercase before using it for filtering.

### Requirement 3: Module filtering via nacc-common

**User Story:** As a center data manager, I want module filtering to use the upstream `modules` parameter, so that only matching data is fetched from the platform.

#### Acceptance Criteria

1. WHEN a module Filter_Set is active, THE Pull_Errors_Script SHALL pass the normalized module set to `get_error_data(project, modules=<set>)`.
2. WHEN a module Filter_Set is active, THE Pull_Status_Script SHALL pass the normalized module set to `get_status_data(project, modules=<set>)`.
3. WHEN no `--module` flag is provided, THE Pull_Errors_Script SHALL call `get_error_data` without the `modules` parameter.
4. WHEN no `--module` flag is provided, THE Pull_Status_Script SHALL call `get_status_data` without the `modules` parameter.

### Requirement 4: PTID filter flag

**User Story:** As a center data manager, I want to specify one or more participant IDs on the command line, so that I only see errors or status records for specific participants.

#### Acceptance Criteria

1. WHEN the `--ptid` flag is provided with one or more comma-separated participant IDs, THE Pull_Errors_Script SHALL split the value on commas and collect each ID into a PTID Filter_Set.
2. WHEN the `--ptid` flag is provided multiple times, THE Pull_Errors_Script SHALL merge all supplied values into a single PTID Filter_Set.
3. WHEN the `--ptid` flag is provided with one or more comma-separated participant IDs, THE Pull_Status_Script SHALL split the value on commas and collect each ID into a PTID Filter_Set.
4. WHEN the `--ptid` flag is provided multiple times, THE Pull_Status_Script SHALL merge all supplied values into a single PTID Filter_Set.
5. THE Pull_Errors_Script SHALL accept `-t` as a short alias for `--ptid`.
6. THE Pull_Status_Script SHALL accept `-t` as a short alias for `--ptid`.

### Requirement 5: PTID post-filtering

**User Story:** As a center data manager, I want PTID filtering applied to the returned data, so that I get only the participants I requested even though the upstream API does not yet support PTID filtering.

#### Acceptance Criteria

1. WHEN a PTID Filter_Set is active, THE Pull_Errors_Script SHALL remove every record from the result list whose `ptid` value is not in the PTID Filter_Set.
2. WHEN a PTID Filter_Set is active, THE Pull_Status_Script SHALL remove every record from the result list whose `ptid` value is not in the PTID Filter_Set.
3. WHEN no `--ptid` flag is provided, THE Pull_Errors_Script SHALL retain all records regardless of PTID.
4. WHEN no `--ptid` flag is provided, THE Pull_Status_Script SHALL retain all records regardless of PTID.

### Requirement 6: Filter logging

**User Story:** As a center data manager, I want to see which filters are active in the log output, so that I can confirm the script is using the filters I intended.

#### Acceptance Criteria

1. WHEN a module Filter_Set is active, THE Pull_Errors_Script SHALL log the active module names at INFO level before requesting data.
2. WHEN a PTID Filter_Set is active, THE Pull_Errors_Script SHALL log the active PTIDs at INFO level before requesting data.
3. WHEN a module Filter_Set is active, THE Pull_Status_Script SHALL log the active module names at INFO level before requesting data.
4. WHEN a PTID Filter_Set is active, THE Pull_Status_Script SHALL log the active PTIDs at INFO level before requesting data.

### Requirement 7: Filtered output filename

**User Story:** As a center data manager, I want the default output filename to reflect active filters, so that filtered and unfiltered outputs do not overwrite each other.

#### Acceptance Criteria

1. WHEN a module Filter_Set is active and no `--output` flag is provided, THE Pull_Errors_Script SHALL include the sorted, hyphen-joined module names in the Default_Output_Filename.
2. WHEN a PTID Filter_Set is active and no `--output` flag is provided, THE Pull_Errors_Script SHALL include the sorted, hyphen-joined PTIDs in the Default_Output_Filename.
3. WHEN a module Filter_Set is active and no `--output` flag is provided, THE Pull_Status_Script SHALL include the sorted, hyphen-joined module names in the Default_Output_Filename.
4. WHEN a PTID Filter_Set is active and no `--output` flag is provided, THE Pull_Status_Script SHALL include the sorted, hyphen-joined PTIDs in the Default_Output_Filename.
5. WHEN no filters are active and no `--output` flag is provided, THE Pull_Errors_Script SHALL use the existing filename pattern `errors-<project-label>-<date>.csv`.
6. WHEN no filters are active and no `--output` flag is provided, THE Pull_Status_Script SHALL use the existing filename pattern `qc-status-<project-label>-<date>.csv`.
7. WHEN the `--output` flag is provided, THE Pull_Errors_Script SHALL use the user-supplied path regardless of active filters.
8. WHEN the `--output` flag is provided, THE Pull_Status_Script SHALL use the user-supplied path regardless of active filters.

### Requirement 8: Backward compatibility

**User Story:** As an existing user, I want the scripts to behave identically to the current versions when no filter flags are provided, so that my existing workflows are not disrupted.

#### Acceptance Criteria

1. WHEN no `--module` flag and no `--ptid` flag are provided, THE Pull_Errors_Script SHALL produce output identical to the current unfiltered behavior.
2. WHEN no `--module` flag and no `--ptid` flag are provided, THE Pull_Status_Script SHALL produce output identical to the current unfiltered behavior.

### Requirement 9: README documentation

**User Story:** As a center developer, I want the README files updated with filter usage examples, so that I can learn how to use the new flags.

#### Acceptance Criteria

1. THE Pull_Errors_Script README SHALL include a usage example showing the `--module` flag with a single module name.
2. THE Pull_Errors_Script README SHALL include a usage example showing the `--ptid` flag with one or more participant IDs.
3. THE Pull_Errors_Script README SHALL include a usage example showing both `--module` and `--ptid` flags combined.
4. THE Pull_Status_Script README SHALL include a usage example showing the `--module` flag with a single module name.
5. THE Pull_Status_Script README SHALL include a usage example showing the `--ptid` flag with one or more participant IDs.
6. THE Pull_Status_Script README SHALL include a usage example showing both `--module` and `--ptid` flags combined.
