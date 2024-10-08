# Data Platform Demonstration Code

Demonstration code for working with the NACC Data Platform.

See the [documenation](https://naccdata.github.io/data-platform-demos) for general guidance.

Keep reading here for details on running the demonstrations.

## Reporting issues

If you run into a problem with the demo, please see the [Issues page](https://github.com/naccdata/data-platform-demos/issues) of this repository and either chime in on an issue or[create a new one](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue).

## About the demos

These demos are meant to provide examples for people who are familiar with developing software.

If you are looking for solutions that run on the command-line, it is possible to use the [Flywheel CLI tool](https://docs.flywheel.io/CLI/) for uploading and downloading data. 
There are some tasks (pulling participant identifiers and file upload errors) that cannot be done with the CLI, but are supported by the ADRC portals.
Otherwise, the code here could be adapted to use in Jupyter notebooks or command line scripts.

Please ask for help if something is unclear.


## Setting up demo environment

> This demo uses the [Pants build system](pantsbuild.org), and assumes a Unix/Linux environment. 
> Windows can use [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install).
> See the [pants requirements](https://www.pantsbuild.org/2.21/docs/getting-started/prerequisites).

You'll first need to [clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your computer using Git.

### Python environment

You will need a Python 3.11 interpreter installed.

The simplest approach may to be to [install Python](https://www.python.org/downloads/).

But, the repository is setup to use a VSCode Dev Container for Python.
Getting this going from scratch requires installing [VSCode](https://code.visualstudio.com), [Docker](https://www.docker.com) and setting up [Dev Containers](https://code.visualstudio.com/docs/devcontainers/tutorial).
This approach is not suggested unless you want to use the same environment we are using.

Incidentally, when you open the repository with VSCode, it will prompt you to install and run the Dev Containers extension, which will in turn prompt you to install [Docker](https://www.docker.com).
After Docker is installed you will have to start the Docker Desktop from your operating system.
Once Docker is started, in VSCode click the green bar at the bottom left and choose "Reopen in Container".

### Using Pants

Once you have a Python 3.11 environment, install the [Pants build system](pantsbuild.org) by running the command

   ```bash
   bash get-pants.sh
   ```

The full installation will occur the first time you run a pants command.

Pants is used because it makes managing dependencies easier, however, it does only run in [Unix/Linux environments](https://www.pantsbuild.org/2.21/docs/getting-started/prerequisites).

If you don't want to use Pants, keep in mind that it may be sufficient for you to look at the code, and adapt it to your environment.
And, of course, you are welcome to change your copy of the repository.

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

### Storing your API key

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

## Demos

- [Python uploader](demo/python-uploader/README.md).
- [R uploader](demo/r-uploader/README.md).
- [CLI uploader](demo/fwcli/README.md).
- [Python error puller](demo/pull_errors/README.md)
- [Python identifier puller](demo/pull_identifiers/README.md)

## Developer guide

### Setup

This repository is setup to use [pants](pantsbuild.org) for developing and building the distributions.

Install pants with the command

```bash
bash get-pants.sh
```

You will need to make sure that you have a Python version compatible with the interpreter set in the `pants.toml` file.

The repo has a VSCode devcontainer configuration that ensures a compatible Python is available.
You need [Docker](https://www.docker.com) installed, and [VSCode](https://code.visualstudio.com) with Dev Containers enabled.
For this follow the [Dev Containers tutorial](https://code.visualstudio.com/docs/devcontainers/tutorial) to the point of "Check Installation".

### Building a distribution

Once pants is installed, the command 

```bash
pants package common::
```

will then build sdist and wheel distributions in the `dist` directory.

> The version number on the distribution files is set in the `common/src/python/BUILD` file.

### Upload distribution

1. Format the code in the respository with

   ```bash
   pants fix ::
   ```

   and commit any changes.

2. Create and push the tag

   ```bash
   VERSION="v<current-version>"
   git tag -a "$VERSION" -m "Data Platform demos $VERSION"
   git push --tags
   ```

3. Create release and upload distribution files
   [This should be automated by github action] 
