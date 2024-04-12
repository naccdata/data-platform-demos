# R Uploader

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
pipeline$get_project(client=client, group_id=group_id)
```

uses defaults to get the `sandbox-form` pipeline as the upload destination.
To submit enrollment form data instead, add the argument `datatype='enrollment'` in the parenthesis.

> To submit actual data, add the argument `pipeline_type='ingest'`.


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
Note this uploads the file `data/form-data.csv`.
The argument `--volume "./data":/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.
The script is hard coded to read only the `form-data.csv` file from that directory, but you could change it to upload any files it finds there.