# Pulling pipeline file errors

This demo shows how to pull file errors from a pipeline project.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

The demo can be run using Pants with the command

```bash
pants run demo/pull_errors/src/python/pull_errors.py -- --adcid 0 --datatype enrollment --pipeline sandbox
```

which will create a file `errors-sandbox-enrollment-<date>.csv` in the top level directory.

(The Pants run command requires `--` before any command-line parameters.)

To run for your center change the `--adcid` argument to the ADCID for your center.

To submit enrollment data, use `--datatype enrollment`.
And, to submit actual data set `--pipeline ingest`.

## About pulling errors

NACC and Flywheel have agreed upon a standard format for error metadata that is captured when files are processed.
The `error_data.get_error_data()` function gathers this metadata and returns it as a `List[Dict[str,Any]]` object that can be used to write the data as a table.
