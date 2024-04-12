# Form Upload Demo Code

Demo code for uploading form data to the NACC Data Platform.

> Note: these projects demonstrate using the Flywheel SDK to connect to the Flywheel instance using code that uploads a file from disk.
> If you plan to upload files this way, you don't need to write your own code, and can instead use the [Flywheel CLI utility](https://docs.flywheel.io/CLI_Command_Guides/)


## Setting up demo environment

1. This repo is setup to be run within a VSCode devcontainer with Python 3.11 and Docker.
   To use this environment, install VSCode, enable dev containers, and open the repository as a container.

   If you choose not to run in this environment, you will need to make sure these are set up within your environment.

2. The repo also uses the [Pants build system](pantsbuild.org).
   Pants is used because it makes managing dependencies easier.

   To install pants, run the script `bash get-path.sh`

## API key

You will need an API Key from the Flywheel system of the NACC Data Platform.

### Finding your API key

Each API key is associated with a particular user. 
To get the API key, login as the user to the NACC Flywheel instance.

1. Find the "avatar" in the upper right corner (generally a circle with your initials).
2. Click the avatar dropdown, and select "Profile".
3. Under "Flywheel Access" at the bottom of the resulting page, click "Generate API Key".
4. Choose a key name relevant to upload, set the expiration date, and create the API Key.
5. Copy the API Key since you wont be able to access the value later.
6. Keep the key secret  

## Storing your API key

For this particular demo, we are storing the API key in a `.env` file.

>Note: The `.gitignore` is set to ignore this file, which helps prevent the key value from being checked into the repository.
> Take care to protect your key like any other secret in your work environment.
> A deployment should use more robust secret management to ensure the secret is not easily accessible.

Run the command 

```bash
touch .env
```

and then edit the file to add your key.

## Python uploader

The Python uploader is defined in the directory `demo/python-uploader`.

This example uses a Docker image to illustrate deploying a Python script to upload a file from disk. As mentioned above, if this is your scenario, you should consider using the Flywheel CLI instead of writing your own script.

The Python script is in the directory `demo/python-uploader/src/python/uploader`.
It uses helper functions defined in `common/src/python`.
The Dockerfile is in the directory `demo/python-uploader/src/docker`
See the comments in the `uploader.py` and `Dockerfile` in these directories for more details.


## R uploader

The R uploader is defined in the directory `demo/r-uploader`.

This example uses a Docker image to illustrate deploying a R script calling Python to upload a file from disk. 
As mentioned above, if uploading from disk is your scenario, you should consider using the Flywheel CLI instead of writing your own script.

The R script is in the directory `demo/python-uploader/src/python/uploader`.
It uses the Reticulate package to call functions in the Flywheel-SDK and helper functions in `common/src/python`.
The Dockerfile is in the directory `demo/python-uploader/src/docker`
See the comments in the `uploader.R` and `Dockerfile` in these directories for more details.


## CLI uploader

The CLI uploader is defined in the directory `demo/fwcli-uploader`.

This example uses a Docker image to illustrate deploying a shell script using the FW CLI to upload a file from disk. 
You can use the CLI as a command, but this shows how the CLI could be used in a production setting.

The Python script is in the directory `demo/fwcli-uploader/src/python/uploader`.
The Dockerfile is in the directory `demo/fwcli-uploader/src/docker`
See the comments in the `uploader.py` and `Dockerfile` in these directories for more details.


