# Form Upload Demonstrations

Purpose: This documentation describes the demonstrated options for programmatically uploading form data to NACC.

## Programmatic Upload Options

There are two options to upload data to the Flywheel instance on which is the NACC Data Platform is built.
One is to use the [Flywheel Python SDK](https://flywheel-io.gitlab.io/product/backend/sdk/index.html), and the other is to use the [Flywheel CLI tool](https://docs.flywheel.io/CLI_Command_Guides/).
Both are demonstrated.

## About the examples.

We demonstrate both strategies for uploads using three examples in the [GitHub repository](https://github.com/naccdata/form-upload-demo):

1. Using the Python SDK from a Python script.
2. Using the Python SDK from an R script.
3. Using the CLI from a bash script.

Each of the examples follow these basic steps:

1. Create a Flywheel client connection with your API Key
2. Determine the group name for your center
3. Determine the project for your upload
4. Upload the file to the project

And, each requires you to make a few changes before you run the code.

Each example is provided with the ability to build and run a [Docker](https://www.docker.com) container.
Using Docker allows us to define the expected computational environment, and could be used as the basis for deploying scripts.

## Which option should you use?

The CLI tool is software that provides alternatives for transferring data into Flywheel, and is already built and tested.
But it only works if you have files to transfer.
So, if you are writing files to disk (or to cloud storage), the CLI is the better alternative.
This is also a good strategy for initial pilots.

If on the other hand, you are creating a file in memory and then uploading, then using the SDK makes more sense.
An example scenario is having an uploader script that pulls form data as a report from REDCap, which builds the CSV in memory, and then uploads this directly.

## Alternative implementations

All of the examples show transferring a single hard-coded file from disk.

### All the files

A simple alternative is to transfer all the files in the `data` directory.
In each case, the change would be to iterate over all of the files in the directory and upload each separately.

Since we expect files to have the "module" name as the file suffix, it would be a good idea to only upload files that end with the expected suffix (an example would be `data-export-20240412-udsv4.csv`)

### "In memory" data

The Flywheel SDK code for uploading data stored in memory is slightly different than in the example.
In this case, you upload the file by creating a `flywheel.FileSpec` object that references the contents and then using that to upload the file.

If the file contents are in a variable `contents`, then the Python code to upload this data is

```python
file_spec = FileSpec(filename, contents=contents, content_type='text/csv')
upload_project.upload_file(file_spec)
```

And, the R code is

```R
file_spec <- flywheel$FileSpec(filename, contents=contents,content_type='text/csv')
upload_project$upload_file(file_spec)
```

