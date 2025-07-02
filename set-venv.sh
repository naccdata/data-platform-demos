#!/bin/sh
ROOTS=$(pants roots)
python3 -c "print('PYTHONPATH=\"./' + ':./'.join('''${ROOTS}'''.split('\n')) + ':\$PYTHONPATH\"')" > .env

if [ ! -e python-default.lock ]; then
    pants generate-lockfiles
else
    echo "Skipping generation of lock file"
fi

pants --keep-sandboxes=on_failure export --py-resolve-format=symlinked_immutable_virtualenv --resolve=python-default 

ln -snf dist/export/python/virtualenvs/python-default /workspaces/data-platform-demos/venv
