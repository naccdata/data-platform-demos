# Details for Using the CLI Uploader

> This demo uses a Linux Docker container running on an x86 platform in order to use the Classic Flywheel CLI.
> The project has been tested on both Apple silicon and Intel Macs.

You will need [Docker](https://www.docker.com) installed to be able to run this demo.

>If you are running the VSCode Dev Container for the repo (see the [top-level README](../../README.md#python-environment)), then Docker is already installed.

## Setting the center and pipeline in the entrypoint script

Before you can run this demo, you need to make a couple of changes in the file `demo/fwcli/src/docker/entrypoint.sh`.

### To set the center

In the line

```bash
CENTER=`center_lookup 0`
```

change the value `0` to the ADCID for your center.

### To set the pipeline

The line

```bash
PIPELINE=`pipeline_lookup -c ${CENTER} -d form -p sandbox -s adrc`
```

sets the pipeline name to `sandbox-form` after confirming the pipeline project exists for your center.
In fact, you can remove the arguments following the center to get this using the defaults.
To submit enrollment form data instead, change `-d form` to `-d enrollment`.

> To submit actual data, change `-p sandbox` to `-p ingest`.

## Running the demo

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All the commands need to be run with the top-level directory of the repository as the working directory.

1. First, build the Docker image with

```bash
pants package demo/fwcli/src/docker::
```

1. Second, run the example using the command

```bash
docker run --platform linux/amd64 --volume ./data:/wd --env-file .env naccdata/cli-uploader
```

Note this uploads the file `data/form-data-dummyv1.csv`.
The argument `--volume ./data:/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.

The script is hard-coded to read only the `form-data-dummyv1.csv` file from that directory, but you could change it to upload any files it finds there.
