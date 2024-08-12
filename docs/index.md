# Form Upload Demonstrations

Purpose: This documentation describes the demonstrated options for uploading form data to NACC directly from center data systems.

To manually upload files from the command line of your computer, please see the [Flywheel CLI](https://docs.naccdata.org/edc/data-uploads-and-quality-checks/uploads-to-nacc/programmatic-uploads#flywheel-cli) in the NACC Documentation pages.

## Programmatic Upload Options

There are two options to upload data to the Flywheel instance on which the NACC Data Platform is built.
One is to use the [Flywheel Python SDK](https://flywheel-io.gitlab.io/product/backend/sdk/index.html), and the other is to use a Flywheel CLI tool.
There are two CLI tools, the [Classic Flywheel CLI tool](https://docs.flywheel.io/CLI/), and the [Beta Flywheel CLI tool](https://flywheel-io.gitlab.io/tools/app/cli/fw-beta/).

The CLI tools are software for transferring data into Flywheel that are already built and tested.
The Beta Flywheel is newer, but is limited to transferring data from external storage such as AWS S3, and cannot be used to upload from a local disk.

Because of this limitation, only the SDK and the classic CLI tool are demonstrated.

## About the examples

We demonstrate both strategies for uploads using three examples in the [GitHub repository](https://github.com/naccdata/form-upload-demo):

1. Using the [Python SDK from a Python script](https://github.com/naccdata/form-upload-demo/tree/main/demo/python-uploader).
2. Using the [Python SDK from an R script](https://github.com/naccdata/form-upload-demo/tree/main/demo/r-uploader).
3. Using the [CLI from a bash script](https://github.com/naccdata/form-upload-demo/tree/main/demo/fwcli).

Each of the examples follow these basic steps:

1. Create a Flywheel client connection with your API Key
2. Determine the group name for your center
3. Determine the project for your upload
4. Upload the file to the project

And, each requires you to make a few changes before you run the code.

Each example is provided with the ability to build and run a [Docker](https://www.docker.com) container.
Using Docker allows us to define the expected computational environment, and could be used as the basis for deploying scripts.

## Which option should you use?

Generally, we suggest using software that you don't have to maintain, which means using one of the CLI tools.
But these are only applicable if you are uploading files on disk or from cloud storage.
If you are generating files stored to disk, the only choice is the classic Flywheel CLI.
If instead you have files on cloud storage such as AWS S3, then you would use the Beta CLI.
We suggest using the classic CLI for initial pilots.

However, using the SDK makes more sense if you are creating a file in memory and then uploading.
An example scenario is having an uploader script that pulls form data as a report from REDCap, which builds the CSV in memory, and then uploads this directly.

## Alternative implementations

All of the examples show transferring a single hard-coded file from disk.
The following are alternative scenarios that may be useful.

### All the files

A simple alternative is to transfer all the files in the `data` directory.
In each case, the change would be to iterate over all of the files in the directory and upload each separately.

Since we expect files to have the "module" name as the file suffix, it would be a good idea to only upload files that end with the expected suffix (an example would be `data-export-20240412-udsv4.csv`).
These suffixes will correspond to the `module` value in each DED and REDCap project.

### "In memory" data

The Flywheel SDK code for uploading data stored in memory is slightly different than in the example.
In this case, you upload the file by creating a `flywheel.FileSpec` object that references the contents and then uses that to upload the file.

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

## An aside: data formats

In this demo, we use the example file [`form-data-dummyv1.csv`](https://github.com/naccdata/form-upload-demo/blob/main/data/form-data-dummyv1.csv).

Please don't read too much into the format of this file, it is an example for you to practice uploading with.

However, there are a couple of points to make about this file:

1. The file name ends in a suffix which is also the value of `module` in each line of the file.
   If this weren't a made up example, the suffix `dummyv1` would be the designator for the data dictionary that determines the expected columns and their datatype for the file.
   These data dictionaries are determined by the REDCap project for the forms.

   Incidentally, the reason we ask for the module designator in the file name and in the file is that the first allows us to take advantage of general purpose tools, and avoids building new software that could have it's own bugs.

2. The dialect of CSV file should not matter.

Initially, no pipeline components will be in place to check the data formats, but once new forms are finalized and QC checks defined, these will be enabled for test submissions.
