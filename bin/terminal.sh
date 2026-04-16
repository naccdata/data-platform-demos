#!/bin/zsh

if ! command -v devcontainer &> /dev/null; then
    echo "Error: devcontainer command not found"
    echo "Please install the devcontainer CLI: npm install -g @devcontainers/cli"
    exit 1
fi

export WORKSPACE_FOLDER=`pwd`
export DOCKER_CLI_HINTS=false

# Use devcontainer exec to open an interactive zsh shell
# This ensures the remoteEnv PATH is set correctly
devcontainer exec --workspace-folder $WORKSPACE_FOLDER /bin/zsh -l
