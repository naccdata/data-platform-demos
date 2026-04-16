# Python Uploader

This example illustrates a Python script to upload a file from disk.
*If you are uploading from disk, you should consider using the Flywheel CLI instead of writing your own script.*

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All commands need to be run with the top-level directory of the repository as the working directory.

## Running the demo script

```bash
uv run demo/python-uploader/uploader.py --adcid 0 --datatype form --pipeline sandbox data/form-data-dummyv1.csv
```

This will upload the file `data/form-data-dummyv1.csv` to `sample-center/sandbox-form`.

To run for your center change the `--adcid` argument to the ADCID for your center.

To submit enrollment data, use `--datatype enrollment`.
And, to submit actual data set `--pipeline ingest`.

## Running the demo within Docker

The Dockerfile can be used to run the upload script in a container.
This approach is useful for building system components because you can define the execution environment independently from that of other components.

1. Build the Docker image:

   ```bash
   docker build -f demo/python-uploader/Dockerfile -t naccdata/python-uploader .
   ```

2. Run the example:

   ```bash
   docker run --volume "./data":/wd --env-file .env naccdata/python-uploader
   ```

   The Dockerfile provides default arguments (`--adcid 0 --datatype form --pipeline sandbox form-data-dummyv1.csv`) via `CMD`, so you can override them at runtime:

   ```bash
   docker run --volume "./data":/wd --env-file .env naccdata/python-uploader --adcid 42 --datatype form --pipeline sandbox form-data-dummyv1.csv
   ```

The argument `--volume "./data":/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.
