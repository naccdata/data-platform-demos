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

## About pulling errors

NACC and Flywheel have agreed upon a standard format for error metadata that is captured when files are processed.
The `error_data.get_error_data()` function gathers this metadata and returns it as a `List[Dict[str,Any]]` object that can be used to write the data as a table.
