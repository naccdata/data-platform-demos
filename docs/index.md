# Form Upload Demonstrations

Purpose: This documentation describes the demonstrated options for programmatically uploading form data to NACC.

## Programmatic Upload Options

There are two options to upload data to the Flywheel instance on which is the NACC Data Platform is built.
One is to use the [Flywheel Python SDK](https://flywheel-io.gitlab.io/product/backend/sdk/index.html), and the other is to use the [Flywheel CLI tool](https://docs.flywheel.io/CLI_Command_Guides/).

If you are writing a file to disk before the upload, the simplest strategy may be to use the CLI tool to do the upload.
Otherwise, if you are building the upload into a system and want to write files created internally, the Python SDK is available.

We provide three examples for demonstration:

1. Using the Python SDK from a Python script.
2. Using the Python SDK from an R script.
3. Using the CLI from a bash script.

Each example is provided with the ability to build and run a [Docker](https://www.docker.com) container.
Using Docker allows us to define the expected computational environment, and could be used as the basis for deploying scripts.

The configuration and code for these are available in this [GitHub repository](https://github.com/naccdata/form-upload-demo).

## Variations on a theme

Each of the approaches follow these basic steps:

1. Create a Flywheel client connection with your API Key
2. Determine the group name for your center
3. Determine the project for your upload
4. Upload the file to the project

And, each requires you to make a few changes before you run the code.

## Alternative Implementations

As mentioned a couple of times, if you want to transfer a file from disk you can just use the Flywheel CLI.
However, if you instead generate the file contents in memory, you can upload the file by creating a `flywheel.FileSpec` object that references the contents and then using that to upload the file.

Assuming file contents are in a variable `contents`, the code to upload this data is
```python
filename = "form-data.csv"
file_type = 'text/csv'
file_spec = FileSpec(filename, contents=contents, content_type=file_type)
if upload_project:
    upload_project.upload_file(file_spec)
```