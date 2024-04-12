# Form Upload Demonstration Code

Demonstration code for uploading form data to the NACC Data Platform.

These projects demonstrate using the Flywheel SDK or the Flywheel CLI tool to connect to the Flywheel instance using code that uploads a file from disk.

Keep reading here for details on running the demonstrations.
See the [documenation](https://naccdata.github.io/form-upload-demo) for general guidance on options.

## Setting up demo environment

1. Install [Docker](https://www.docker.com) installed to run the demo examples.

2. We recommend running the demo within a VSCode devcontainer to avoid dependency issues.
   This repo setup to be run within a devcontainer with Python 3.11 and Docker.
   You'll need [VSCode](https://code.visualstudio.com) with Dev Containers enabled.
   For this follow the [Dev Containers tutorial](https://code.visualstudio.com/docs/devcontainers/tutorial) to the point of "Check Installation".

   Technically this is not necessary, but the repo is configured to support the demos and can avoid issues.

3. With the devcontainer running, open a terminal pane in VSCode using the key combination ctrl-\`.  
   (The key for \` is usually immediately to the left of the 1 key on a US Keyboard.)

4. The repo also uses the [Pants build system](pantsbuild.org).
   Pants is used because it makes managing dependencies easier.

   To install pants, run the command

   ```bash
   bash get-pants.sh
   ```

   The full installation will occur the first time you run a pants command.


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

and then edit the file to add your key in a line like

```bash
FW_API_KEY=<the value of the API key>
```

> The `.env` file is included in the `.gitignore` file intentionally to prevent inclusion of the API token in a Git repository.

## Python uploader

The Python uploader is defined in the directory `demo/python-uploader`.

This example uses a Docker image to illustrate deploying a Python script to upload a file from disk. As mentioned above, if this is your scenario, you should consider using the Flywheel CLI instead of writing your own script.

Details on this example are given in [`demo/python-uploader/README.md`](demo/python-uploader/README.md).


## R uploader

The R uploader is defined in the directory `demo/r-uploader`.

This example uses a Docker image to illustrate deploying a R script calling Python to upload a file from disk. 
As mentioned above, if uploading from disk is your scenario, you should consider using the Flywheel CLI instead of writing your own script.

Details on this example are given in [`demo/r-uploader/README.md`](demo/r-uploader/README.md).


## CLI uploader

The CLI uploader is defined in the directory `demo/fwcli-uploader`.

This example uses a Docker image to illustrate deploying a shell script using the FW CLI to upload a file from disk. 
You can use the CLI as a command, but this shows how the CLI could be used in a production setting.

Details for running this example are given in [`demo/fwcli/README.md`](demo/fwcli/README.md).


