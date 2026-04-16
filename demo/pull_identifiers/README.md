# Pulling Participant Identifiers

This example is a Python script that pulls participant identifiers from an enrollment ingest project using a NACC created dataview.

> Enrollment projects are associated with a particular study.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

```bash
uv run demo/pull_identifiers/pull_identifiers.py --adcid 0 --pipeline sandbox
```

This will create a file `center-identifiers-<date>.csv` in the top level directory.

To run for your center change the `--adcid` argument to the ADCID for your center.
You can change the pipeline to `--pipeline ingest`.

You can specify a custom output path with `--output`:

```bash
uv run demo/pull_identifiers/pull_identifiers.py --adcid 0 --output my-identifiers.csv
```

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
