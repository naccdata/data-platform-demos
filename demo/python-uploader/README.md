# Python Uploader

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

The demo can be run using Pants with the command

```bash
pants run demo/python-uploader/src/python/uploader/uploader.py -- --adcid 0 --datatype form --pipeline sandbox data/form-data-dummyv1.csv
```

which will upload the file `data/form-data-dummyv1.csv` to `sample-center/sandbox-form`.

(The Pants run command requires `--` before any command-line parameters.)

To run for your center change the `--adcid` argument to the ADCID for your center.

To submit enrollment data, use `--datatype enrollment`.
And, to submit actual data set `--pipeline ingest`.

> If you want to run without Pants, you will need to manage dependencies and setting environment variables.

## Running the demo within Docker

The `docker` subdirectory includes a configuration for a Docker image that can be used to run the upload script.
This approach is useful for building system components because you can define the execution environment independently from that of other components.

1. First, build the Docker image with

```bash
pants package demo/python-uploader/src/docker::
```

1. Second, run the example using the command

```bash
docker run --volume "./data":/wd --env-file .env naccdata/python-uploader
```

Note this uploads the file `data/form-data-dummyv1.csv`.

The argument `--volume "./data":/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.
The Dockerfile is hard-coded to use the script to read only the `form-data-dummyv1.csv` file from that directory, but the script could be changed to upload any files it finds there.

## Apple Silicon issues

The Pants BUILD file (`demo/python-uploader/src/python/uploader/BUILD`) is set to create an executable Pex files for x86 execution environments.
This is should allow the Docker demo to run even on Apple silicon Macs because the Docker images used are also for x86.

However, if you want to use have a Pex file specific to Apple silicon, you need to edit the BUILD file to remove the line

```python
           complete_platforms=["//:linux_x86_py311"],
```

from the `pex_binary()` configuration.

