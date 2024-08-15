# NACC Data Platform Demos

Purpose: This documentation describes programmatic options for working with the Flywheel system underneath the NACC Data Platform.

## About these demos

The goal of these demos is to provide examples for people who are familiar with developing software.

If you are looking for solutions that run on the command-line, it is possible to use the [Flywheel CLI tool](https://docs.flywheel.io/CLI/) for uploading and downloading data. 
There are some scenarios (pulling participant identifiers, or QC errors) that will still require some scripting.
Please ask for help if something seems unclear or especially complicated.

## About Data Platform pipelines

The NACC Data Platform is built on top of the Flywheel data management system.
Flywheel organizes data by group and project, under which data for individual subjects is stored.
Each center has a group, with a set of pipeline projects for each study to which it contributes.

You can see the group and projects you have access to within Flywheel, by opening the Projects page in the user interface, or by using the Flywheel CLI.
The list of projects you see will depend on your authorizations, but may include `ingest-dicom`, `ingest-enrollment`, and `ingest-form`.
These are the ingest pipeline projects, and are labeled by the datatype each is configured to handle.
You may also see an `accepted` project, which is where data that has passed QC can be accessed.
Each `ingest-` project has a corresponding `sandbox-` project for practice submissions.

You may also have projects that look like `ingest-form-leads`, or if your center was part of the UDSv4 Pilot a project like `ingest-form-udsv4pilot`.
These are pipelines that are dedicated to particular studies (other than the ADRC program) or purposes (such as the pilot).

The group and projects IDs and labels are used in uploading and accessing data within Flywheel.
For instance, the form ingest project in the NACC Sample Center, is referenced as `sample-center/ingest-form`.

The demo code includes utility functions that help build these references.
The function `center_info.get_center_id()` returns the group ID when given a center's ADCID (the numeric ID used on form submissions).
And, `pipeline.get_project()` constructs the project label for a pipeline project.

## NACC-Common package

The `common` directory of the demo repository contains a package of utilities used in the demo code.
Distributions can be accessed via each [release](https://github.com/naccdata/data-platform-demos/releases) on GitHub.


## Scenarios

1. [Uploading form (tabular) data](upload.md)
2. Accessing tabular data views
   - Example: [pulling upload errors](https://github.com/naccdata/data-platform-demos/tree/main/demo/pull_errors)
   - Example: [pulling participant identifiers](https://github.com/naccdata/data-platform-demos/tree/main/demo/pull_identifiers)
   - Example: [pulling flywheel dataviews (in general)](https://github.com/naccdata/data-platform-demos/tree/main/demo/dataviews)

