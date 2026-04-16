# Pulling pipeline file QC status

This example is a Python script that uses the `error_data.get_status_data` function from the `nacc_common` package to pull QC status data from a pipeline project.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

```bash
uv run demo/pull_status/pull_status.py --adcid 0 --datatype enrollment --pipeline sandbox
```

This will create a file `qc-status-<project-label>-<date>.csv` in the top level directory.

To run for your center change the `--adcid` argument to the ADCID for your center.

To submit enrollment data, use `--datatype enrollment`.
And, to submit actual data set `--pipeline ingest`.

You can specify a custom output path with `--output`:

```bash
uv run demo/pull_status/pull_status.py --adcid 0 --output my-status.csv
```

## Filtering results

You can narrow the results by module name, participant ID, or both.

**Filter by module** (`--module` or `-m`):

```bash
uv run demo/pull_status/pull_status.py --adcid 0 --module UDS
```

This retrieves QC status records for the UDS module only. Module names are case-insensitive and normalized to uppercase, so `--module uds` works the same way. You can specify multiple modules with commas (`--module UDS,LBD`) or by repeating the flag (`--module UDS --module LBD`).

**Filter by participant ID** (`--ptid` or `-t`):

```bash
uv run demo/pull_status/pull_status.py --adcid 0 --ptid PT001,PT002
```

This retrieves QC status records for participants PT001 and PT002 only. PTID filtering is case-sensitive. You can also repeat the flag (`--ptid PT001 --ptid PT002`).

**Combine filters**:

```bash
uv run demo/pull_status/pull_status.py --adcid 0 --module UDS --ptid PT001
```

This retrieves only UDS records for participant PT001. Filters can be combined freely.

When filters are active and no `--output` path is given, the output filename automatically reflects the active filters (e.g., `qc-status-UDS-ptid-PT001-<project-label>-<date>.csv`).

## About pulling QC status

NACC and Flywheel have agreed upon a standard format for QC status metadata that is captured when files are processed.
The `error_data.get_status_data()` function gathers this metadata and returns it as a `List[Dict[str,Any]]` object that can be used to write the data as a table.
