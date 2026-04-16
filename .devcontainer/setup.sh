#!/bin/bash
set -e

echo "Setting up development environment..."

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync

# Verify installations
python --version
uv --version

echo "Development environment ready!"
