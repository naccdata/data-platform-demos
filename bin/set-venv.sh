#!/bin/sh
ROOTS=$(pants roots)
PYTHONPATH_LINE=$(python3 -c "print('PYTHONPATH=\"./' + ':./'.join('''${ROOTS}'''.split('\n')) + ':\$PYTHONPATH\"')")

# Update or add PYTHONPATH in .env while preserving other variables
if [ -f .env ]; then
    # If PYTHONPATH exists, update it; otherwise, append it
    if grep -q "^PYTHONPATH=" .env; then
        # Use a temporary file to avoid issues with in-place editing
        grep -v "^PYTHONPATH=" .env > .env.tmp
        echo "$PYTHONPATH_LINE" >> .env.tmp
        mv .env.tmp .env
    else
        echo "$PYTHONPATH_LINE" >> .env
    fi
else
    # Create new .env file if it doesn't exist
    echo "$PYTHONPATH_LINE" > .env
fi

if [ ! -e python-default.lock ]; then
    pants generate-lockfiles
else
    echo "Skipping generation of lock file"
fi

pants export --py-resolve-format=symlinked_immutable_virtualenv --resolve=python-default

ln -snf dist/export/python/virtualenvs/python-default ./.venv

# Clean up any dead symlinks in .venv before creating new ones
if [ -d .venv ]; then
    find .venv -type l ! -exec test -e {} \; -delete 2>/dev/null || true
fi

# Find the latest Python version directory and create a bin symlink
LATEST_PY_VERSION=$(ls -1 dist/export/python/virtualenvs/python-default/ | grep -E '^[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -1)
if [ -n "$LATEST_PY_VERSION" ]; then
    ln -snf "$LATEST_PY_VERSION/bin" ./.venv/bin
    echo "Created .venv/bin symlink pointing to Python $LATEST_PY_VERSION"
else
    echo "Warning: Could not find Python version directory in .venv"
fi