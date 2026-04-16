# Dev Container and Setup Scripts

Helper scripts for managing the development container and setting up the local environment.

## Prerequisites

Install the devcontainer CLI:

```bash
npm install -g @devcontainers/cli
```

## Scripts

### `set-venv.sh`

Set up the Python virtual environment for local development.

```bash
./bin/set-venv.sh
```

This script:
1. Configures `PYTHONPATH` in `.env` (preserving existing variables like `FW_API_KEY`)
2. Generates the Pants lockfile if it doesn't exist
3. Exports a symlinked immutable virtualenv to `dist/export/python/virtualenvs/python-default`
4. Creates a `.venv` symlink pointing to the exported virtualenv

### `build-container.sh`

Build the dev container image.

```bash
./bin/build-container.sh
```

This reads the `.devcontainer/devcontainer.json` configuration and builds the container image with all specified features and dependencies.

### `start-devcontainer.sh`

Start the dev container.

```bash
./bin/start-devcontainer.sh
```

Starts the container and runs the `postCreateCommand` if it's the first time starting. The workspace folder is mounted at `/workspaces/<workspace-name>`.

### `stop-devcontainer.sh`

Stop and remove the running dev container.

```bash
./bin/stop-devcontainer.sh
```

Stops the container and cleans up resources.

### `terminal.sh`

Open an interactive shell in the running dev container.

```bash
./bin/terminal.sh
```

Opens a zsh shell as the `vscode` user in the workspace directory. The container must be running first.

### `exec-in-devcontainer.sh`

Execute a command in the running dev container.

```bash
./bin/exec-in-devcontainer.sh <command> [args...]
```

Examples:

```bash
# List files
./bin/exec-in-devcontainer.sh ls -la

# Run pants commands
./bin/exec-in-devcontainer.sh pants test ::

# Check Python version
./bin/exec-in-devcontainer.sh python --version
```

## Typical Workflow

1. Build the container (first time or after config changes):

   ```bash
   ./bin/build-container.sh
   ```

2. Start the container:

   ```bash
   ./bin/start-devcontainer.sh
   ```

3. Open a shell or execute commands:

   ```bash
   ./bin/terminal.sh
   # or
   ./bin/exec-in-devcontainer.sh pants lint ::
   ```

4. Stop the container when done:

   ```bash
   ./bin/stop-devcontainer.sh
   ```

## Notes

- All scripts check for the devcontainer CLI and provide installation instructions if missing
- The workspace folder is automatically mounted in the container
- Scripts use the current directory as the workspace folder
