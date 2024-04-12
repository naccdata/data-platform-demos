# Details for Using the CLI Uploader

## Setting the center and pipeline in the entrypoint script

Before you can run this demo, you need to set the variables `CENTER` and `PIPELINE` in the script `demo/fwcli/src/docker/entrypoint.sh`.

### To determine the value of `CENTER`:

1. Login to naccdata.flywheel.org.
2. On the Projects page, type `nacc` into the `Group` field.
3. Click on the NACC `metadata` project.
4. Click on the `Information` tab
5. Under custom centers click the `^` button next to `centers`
6. You should now see a list of NACC assigned ADCIDs. Find yours and click the corresponding `^` button.
7. Edit the entrypoint script, and set `CENTER` to the value listed for `group`.

A slightly quicker way, is to select a project for your center on the Projects page. 
Then look for a reference of the form `fw://<center-name>/<project-name>` at the top of the page, and use the `<center-name>` in the script.

### To determine the value for `PIPELINE`:

1. For practice submissions of form data, use `sandbox-form`.
2. For practice submissions of enrollment (aka, NACCID) form data, use `sandbox-enrollment`.

For submission of actual data, replace `sandbox` with `ingest` in the pipeline name.

## Running the demo

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

> All the commands need to be run with the top-level directory of the repository as the working directory.

1. First, build the Docker image with
```bash
pants package demo/fwcli-uploader/src/docker::
```

2. Second, run the example using the command
```bash
docker run --volume ./data:/wd --env-file .env naccdata/cli-uploader
```
Note this uploads the file `data/form-data-dummyv1.csv`.
The argument `--volume ./data:/wd` indicates to Docker that you want `/wd` within the container to reference the `data` directory.

The script is hard-coded to read only the `form-data-dummyv1.csv` file from that directory, but you could change it to upload any files it finds there.