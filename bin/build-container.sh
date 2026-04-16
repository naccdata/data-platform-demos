#!/bin/zsh

if ! command -v devcontainer &> /dev/null; then
    echo "Error: devcontainer command not found"
    echo "Please install the devcontainer CLI: npm install -g @devcontainers/cli"
    exit 1
fi

export DOCKER_CLI_HINTS=false
devcontainer build --workspace-folder .
