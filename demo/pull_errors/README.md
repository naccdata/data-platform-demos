# Pulling pipeline file errors

This example is a Python script that uses the `error_data.get_error_data` function from the `nacc-common` package to pull error data from a pipeline project.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

```bash
uv run demo/pull_errors/pull_errors.py --adcid 0 --datatype enrollment --pipeline sandbox
```

This will create a file `errors-<project-label>-<date>.csv` in the top level directory.

To run for your center change the `--adcid` argument to the ADCID for your center.

To submit enrollment data, use `--datatype enrollment`.
And, to submit actual data set `--pipeline ingest`.

You can specify a custom output path with `--output`:

```bash
uv run demo/pull_errors/pull_errors.py --adcid 0 --output my-errors.csv
```

## Filtering results

You can narrow the output to specific modules and/or participant IDs using the `--module` (`-m`) and `--ptid` (`-t`) flags.

Filter by a single module:

```bash
uv run demo/pull_errors/pull_errors.py --adcid 0 --module UDS
```

This retrieves errors only for the UDS module. Module names are case-insensitive (they are normalized to uppercase internally). You can specify multiple modules with commas (`--module UDS,LBD`) or by repeating the flag (`--module UDS --module LBD`).

Filter by one or more participant IDs:

```bash
uv run demo/pull_errors/pull_errors.py --adcid 0 --ptid PT001,PT002
```

This retrieves errors only for participants PT001 and PT002. PTID filtering is case-sensitive.

Combine both filters:

```bash
uv run demo/pull_errors/pull_errors.py --adcid 0 --module UDS --ptid PT001
```

This retrieves only UDS errors for participant PT001. Filters can be combined freely.

When filters are active and no `--output` flag is provided, the output filename automatically reflects the active filters (e.g., `errors-UDS-ptid-PT001-<project-label>-<date>.csv`).

## About pulling errors

NACC and Flywheel have agreed upon a standard format for error metadata that is captured when files are processed.
The `error_data.get_error_data()` function gathers this metadata and returns it as a `List[Dict[str,Any]]` object that can be used to write the data as a table.
