# R Uploader

This example uses a Docker image to illustrate deploying a R script calling Python to upload a file from disk. 
As mentioned above, if uploading from disk is your scenario, you should consider using the Flywheel CLI instead of writing your own script.

> This demo uses the [reticulate](https://rstudio.github.io/reticulate/) package to use the Flywheel Python SDK within R.

You will need [Docker](https://www.docker.com) installed to be able to run this demo.

>If you are running the VSCode Dev Container for the repo (see the [top-level README](../../README.md#python-environment)), then Docker is already installed.

## Setting the center and pipeline

Before you can run this demo, you need to make a couple of changes in the file `demo/r-uploader/src/r/uploader/uploader.R`.

### To set the center

In the line

```R
adcid <- '0'
```

change the value to the ADCID for your center.
(Make sure the number is still in quotes.)

### To set the pipeline

The line

```R
pipeline$get_project(client=client, group_id=group_id, datatype='form', pipeline_type='sandbox', study_id='adrc')
```

gets the `sandbox-form` pipeline as the upload destination.
To submit enrollment form data instead, set the datatype argument `datatype='enrollment'` in the parenthesis.

> To submit actual data, set the pipeline argument `pipeline_type='ingest'`.

## Running Demo

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All the commands need to be run with the top-level directory of the repository as the working directory.

1. First, build the Docker image with

```bash
pants package demo/r-uploader/src/docker::
```

1. Second, run the example using the command

```bash
docker run --volume "./data":/wd --env-file .env naccdata/r-uploader
```

Note this uploads the file `data/form-data-dummyv1.csv`.
The argument `--volume "./data":/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.
The script is hard coded to read only the `form-data-dummyv1.csv` file from that directory, but you could change it to upload any files it finds there.
