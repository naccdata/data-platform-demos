# Data Platform Demonstration Code

Demonstration code for working with the NACC Data Platform.

See the [documentation](https://naccdata.github.io/data-platform-demos) for general guidance.

Keep reading here for details on running the demonstrations.

## Reporting issues

If you run into a problem with the demo, please see the [Issues page](https://github.com/naccdata/data-platform-demos/issues) of this repository and either chime in on an issue or [create a new one](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue).

## About the demos

These demos are meant to provide examples for people who are familiar with developing software.

If you are looking for solutions that run on the command-line, it is possible to use the [Flywheel CLI tool](https://docs.flywheel.io/CLI/) for uploading and downloading data.
There are some tasks (pulling participant identifiers and file upload errors) that cannot be done with the CLI, but are supported by the ADRC portals.
Otherwise, the code here could be adapted to use in Jupyter notebooks or command line scripts.

Please ask for help if something is unclear.

## Setting up demo environment

You'll first need to [clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your computer using Git.

### Python environment

You will need a Python 3.12 interpreter installed.

The simplest approach is to [install Python](https://www.python.org/downloads/).

### Installing uv

This project uses [uv](https://docs.astral.sh/uv/) to manage Python dependencies. Install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the project dependencies:

```bash
uv sync
```

That's it. You can now run any demo script with `uv run`.

### Linting and type checking

```bash
# Lint all demo scripts
uv run ruff check demo/

# Type check all demo scripts
uv run mypy demo/ --ignore-missing-imports
```

Or use the Makefile shortcuts:

```bash
make lint
make check
make all    # both lint and check
```

## API key

You will need an API Key from the Flywheel system of the NACC Data Platform.

### Finding your API key

Each API key is associated with a particular user.
To get the API key, login as the user to the NACC Flywheel instance.

1. Find the "avatar" in the upper right corner (generally a circle with your initials).
2. Click the avatar dropdown, and select "Profile".
3. Under "Flywheel Access" at the bottom of the resulting page, click "Generate API Key".
4. Choose a key name relevant to upload, set the expiration date, and create the API Key.
5. Copy the API Key since you won't be able to access the value later.
6. Keep the key secret

### Storing your API key

The demo scripts look for your API key in this order:

1. **`--api-key` flag** — pass it directly on the command line
2. **`FW_API_KEY` environment variable** — loaded automatically from a `.env` file if present
3. **System keyring** — macOS Keychain, Windows Credential Locker, or Linux Secret Service
4. **Interactive prompt** — if none of the above are found and you're in a terminal, you'll be prompted; the key is then stored in the system keyring for next time

The simplest approach for repeated use is to run a script once and enter your key when prompted. It will be saved in your OS keyring automatically.

Alternatively, create a `.env` file:

```bash
echo "FW_API_KEY=<the value of the API key>" > .env
```

> The `.gitignore` is set to ignore `.env` to prevent the key from being checked into the repository.
> For production use, prefer the system keyring or a dedicated secret manager over plaintext files.

## Demos

- [Python uploader](demo/python-uploader/README.md)
- [R uploader](demo/r-uploader/README.md)
- [CLI uploader](demo/fwcli/README.md)
- [Enrollment upload and errors](demo/enrollment/README.md)
- [Python error puller](demo/pull_errors/README.md)
- [Python status puller](demo/pull_status/README.md)
- [Python identifier puller](demo/pull_identifiers/README.md)
