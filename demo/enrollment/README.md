# Enrollment Demo

This demo contains two Python scripts for working with enrollment data on the NACC Data Platform:

- **`enroll_upload.py`** — Uploads an enrollment CSV file to the enrollment pipeline project.
- **`enroll_errors.py`** — Pulls enrollment-specific error data from the enrollment pipeline project.

Centers must submit enrollment data before they can submit visit forms. These scripts provide a dedicated workflow for that process, hardcoding `datatype="enrollment"` so you don't need to specify it on the command line.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Uploading enrollment data

```bash
uv run demo/enrollment/enroll_upload.py --adcid 0 --pipeline sandbox data/enrollment-data.csv
```

This uploads `data/enrollment-data.csv` to the sandbox enrollment pipeline project for center 0.

To run for your center change the `--adcid` argument to the ADCID for your center.
To submit actual data set `--pipeline ingest`.

## Pulling enrollment errors

```bash
uv run demo/enrollment/enroll_errors.py --adcid 0 --pipeline sandbox
```

This will create a file `enrollment-errors-<project-label>-<date>.csv` in the top level directory.

To run for your center change the `--adcid` argument to the ADCID for your center.
To pull from the ingest pipeline set `--pipeline ingest`.

You can specify a custom output path with `--output`:

```bash
uv run demo/enrollment/enroll_errors.py --adcid 0 --output my-enrollment-errors.csv
```

## Filtering results

You can narrow the error output to specific modules and/or participant IDs using the `--module` (`-m`) and `--ptid` (`-t`) flags.

Filter by a single module:

```bash
uv run demo/enrollment/enroll_errors.py --adcid 0 --module UDS
```

This retrieves errors only for the UDS module. Module names are case-insensitive (they are normalized to uppercase internally). You can specify multiple modules with commas (`--module UDS,LBD`) or by repeating the flag (`--module UDS --module LBD`).

Filter by one or more participant IDs:

```bash
uv run demo/enrollment/enroll_errors.py --adcid 0 --ptid PT001,PT002
```

This retrieves errors only for participants PT001 and PT002. PTID filtering is case-sensitive. You can also repeat the flag (`--ptid PT001 --ptid PT002`).

Combine both filters:

```bash
uv run demo/enrollment/enroll_errors.py --adcid 0 --module UDS --ptid PT001
```

This retrieves only UDS errors for participant PT001. Filters can be combined freely.

When filters are active and no `--output` flag is provided, the output filename automatically reflects the active filters (e.g., `enrollment-errors-UDS-ptid-PT001-<project-label>-<date>.csv`).

## Expected enrollment CSV format

The upload script expects a standard CSV file with enrollment data. The columns include:

- `module` — The module name for the enrollment record
- `adcid` — The Alzheimer's Disease Center Identifier
- `ptid` — The participant ID

Additional enrollment-specific fields (e.g., `ENRLTYPE`, `PREVENRL`, `NACCIDKWN`) are defined by the NACC Data Platform and validated server-side during pipeline processing.

## Pulling enrollment identifiers

To query enrollment identifiers (participant IDs associated with enrollment records), use the existing [`demo/pull_identifiers/`](../pull_identifiers/) demo with the enrollment pipeline.
