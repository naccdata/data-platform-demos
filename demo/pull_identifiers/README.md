# Pulling Participant Identifiers

This demo shows how to pull participant identifiers from an enrollment pipeline project.

>Enrollment projects are associated with a particular study.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

The demo can be run using Pants with the command

```bash
pants run demo/pull_identifiers/src/python/pull_identifiers.py -- --adcid 0 --pipeline sandbox
```

which will create a file `errors-sandbox-enrollment-<date>.csv` in the top level directory.

(The Pants run command requires `--` before any command-line parameters.)

To run for your center change the `--adcid` argument to the ADCID for your center.
You can change the pipeline to `--pipeline ingest`.

## About Dataviews

The identifiers are accessed as a dataview, which can be used in many cases in Flywheel to pull tabular data.

To use a dataview, you have to first find the ID for the dataview.
(Here we use a function `pipeline.get_published_view()` that gets the ID for a NACC published dataview by label.)
And, then you can pull the data in one of these ways:

1. get the data as JSON
2. write the data to a file
3. get the data as a Pandas dataframe

The demo writes the data to a file.
For the other approaches, see the Flywheel [Data Views documentation](https://flywheel-io.gitlab.io/product/backend/sdk/tags/18.3.0/python/data_views.html#).
