#!/bin/zsh

if ! command -v devcontainer &> /dev/null; then
    echo "Error: devcontainer command not found"
    echo "Please install the devcontainer CLI: npm install -g @devcontainers/cli"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: $0 <command> [args...]"
    echo "Example: $0 ls -la"
    exit 1
fi

export WORKSPACE_FOLDER=`pwd`
export DOCKER_CLI_HINTS=false
devcontainer exec --workspace-folder $WORKSPACE_FOLDER "$@"
