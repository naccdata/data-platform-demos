# Details for Using the CLI Uploader

This example uses a Docker image to illustrate deploying a shell script using the FW CLI to upload a file from disk.
You can use the CLI as a command, but this shows how the CLI could be used in a production setting.

> This demo uses a Linux Docker container running on an x86 platform in order to use the Classic Flywheel CLI.
> The project has been tested on both Apple silicon and Intel Macs.

You will need [Docker](https://www.docker.com) installed to be able to run this demo.

> If you are running the VSCode Dev Container for the repo (see the [top-level README](../../README.md#python-environment)), then Docker is already installed.

## Configuration

The entrypoint script reads the following environment variables (all have defaults):

| Variable   | Default   | Description                          |
|------------|-----------|--------------------------------------|
| `ADCID`    | `0`       | The ADCID for your center (0-99)     |
| `DATATYPE` | `form`    | The datatype (`form`, `enrollment`, `dicom`) |
| `PIPELINE` | `sandbox` | The pipeline type (`sandbox`, `ingest`) |
| `STUDYID`  | `adrc`    | The study ID                         |

To run for your center, pass `--env ADCID=<your-adcid>` to `docker run`.

## Running the demo

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All the commands need to be run with the top-level directory of the repository as the working directory.

1. Build the Docker image:

   ```bash
   docker build -f demo/fwcli/Dockerfile --platform linux/amd64 -t naccdata/cli-uploader .
   ```

2. Run the example:

   ```bash
   docker run --platform linux/amd64 --volume ./data:/wd --env-file .env naccdata/cli-uploader
   ```

   To run for your center, add `--env ADCID=42` (replacing `42` with your ADCID):

   ```bash
   docker run --platform linux/amd64 --volume ./data:/wd --env-file .env --env ADCID=42 naccdata/cli-uploader
   ```

Note this uploads the file `data/form-data-dummyv1.csv`.
The argument `--volume ./data:/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.

The script is hard-coded to read only the `form-data-dummyv1.csv` file from that directory, but you could change it to upload any files it finds there.
