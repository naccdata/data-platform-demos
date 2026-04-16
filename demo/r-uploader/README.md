# R Uploader

This example uses a Docker image to illustrate deploying an R script calling Python to upload a file from disk.
If uploading from disk is your scenario, you should consider using the Flywheel CLI instead of writing your own script.

> This demo uses the [reticulate](https://rstudio.github.io/reticulate/) package to use the Flywheel Python SDK within R.

You will need [Docker](https://www.docker.com) installed to be able to run this demo.

> If you are running the VSCode Dev Container for the repo (see the [top-level README](../../README.md#python-environment)), then Docker is already installed.

## Configuration

The R script reads the following environment variables (all have defaults):

| Variable   | Default   | Description                          |
|------------|-----------|--------------------------------------|
| `ADCID`    | `0`       | The ADCID for your center (0-99)     |
| `DATATYPE` | `form`    | The datatype (`form`, `enrollment`, `dicom`) |
| `PIPELINE` | `sandbox` | The pipeline type (`sandbox`, `ingest`) |
| `STUDYID`  | `adrc`    | The study ID                         |

To run for your center, pass `--env ADCID=<your-adcid>` to `docker run`.

## Running Demo

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All the commands need to be run with the top-level directory of the repository as the working directory.

1. First, build the Docker image with

   ```bash
   pants package demo/r-uploader/src/docker::
   ```

2. Second, run the example using the command

   ```bash
   docker run --volume "./data":/wd --env-file .env naccdata/r-uploader
   ```

   To run for your center, add `--env ADCID=42` (replacing `42` with your ADCID):

   ```bash
   docker run --volume "./data":/wd --env-file .env --env ADCID=42 naccdata/r-uploader
   ```

Note this uploads the file `data/form-data-dummyv1.csv`.
The argument `--volume "./data":/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.
The script reads only the `form-data-dummyv1.csv` file from that directory, but you could change it to upload any files it finds there.
