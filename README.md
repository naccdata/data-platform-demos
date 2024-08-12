# Form Upload Demonstration Code

Demonstration code for uploading form data to the NACC Data Platform.

These projects demonstrate using the Flywheel SDK or the Flywheel CLI tool to connect to the Flywheel instance using code that uploads a file from disk.

Keep reading here for details on running the demonstrations.
See the [documenation](https://naccdata.github.io/form-upload-demo) for general guidance on options.

## Reporting issues

If you run into a problem with the demo, please see the [Issues page](https://github.com/naccdata/form-upload-demo/issues) of this repository and either chime in on an issue or[create a new one](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue).

## Setting up demo environment

> This demo does assume a Unix/Linux environment. Windows users should see [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/)

You'll first need to [clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your computer using Git.

The most straightforward way to get started is install [VSCode](https://code.visualstudio.com), and then use it to open the repository directory.
VSCode will then prompt you to install and run the Dev Containers extension, which will in turn prompt you to install [Docker](https://www.docker.com).
After Docker is installed you will have to start the Docker Desktop from your operating system.
Once Docker is started, in VSCode click the green bar at the bottom left and choose "Reopen in Container".

Alternatively, you can 

1. Install [Docker](https://www.docker.com)
2. Install [VSCode](https://code.visualstudio.com)
3. Follow the [Dev Containers tutorial](https://code.visualstudio.com/docs/devcontainers/tutorial) to the point of "Check Installation".

which will get you to the same place as above.

Once the Dev Container is running:

1. Open a terminal pane in VSCode using the key combination ctrl-\`.  
   (The key for \` is usually immediately to the left of the 1 key on a US Keyboard.)

2. Install the [Pants build system](pantsbuild.org) by running the command

   ```bash
   bash get-pants.sh
   ```

   The full installation will occur the first time you run a pants command.

   Pants is used because it makes managing dependencies easier.   


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
