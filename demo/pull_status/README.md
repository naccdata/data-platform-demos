# Pulling pipeline file QC status

This example is a Python script that uses the `error_data.get_status_data` function from the `nacc_common` package to pull QC status data from a pipeline project.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

The demo can be run using Pants with the command

```bash
pants run demo/pull_status/src/python/pull_status.py -- --adcid 0 --datatype enrollment --pipeline sandbox
```

which will create a file `qc-status-<project-label>-<date>.csv` in the top level directory.

(The Pants run command requires `--` before any command-line parameters.)

To run for your center change the `--adcid` argument to the ADCID for your center.

To submit enrollment data, use `--datatype enrollment`.
And, to submit actual data set `--pipeline ingest`.

## About pulling QC status

NACC and Flywheel have agreed upon a standard format for QC status metadata that is captured when files are processed.
The `error_data.get_status_data()` function gathers this metadata and returns it as a `List[Dict[str,Any]]` object that can be used to write the data as a table.
