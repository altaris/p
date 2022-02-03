#!/bin/bash

# ==============================================================================
# Downloads
# ==============================================================================

function _download () {
    echo "Downloading '$1' to '$2'"
    curl -Ls "$1" -o "$2" > /dev/null
}

_download \
    "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore" \
    .gitignore

echo "
# MacOS littering everywhere
.DS_Store

# PyCharm
.idea

# VSCode
*.code-workspace
.vscode/" >> .gitignore

# ==============================================================================
# Setup VSCode
# ==============================================================================

mkdir .vscode
echo "{
    \"folders\": [
        {
            \"path\": \".\"
        }
    ]
}" > "$(basename "$(pwd)").code-workspace"
echo "{
    \"python.pythonPath\": \"venv/bin/python\",
    \"python.linting.pylintEnabled\": true,
    \"python.linting.enabled\": true,
    \"files.exclude\": {
        \"**/.DS_Store\": true,
        \"**/.git\": true,
        \"**/.hg\": true,
        \"**/.mypy_cache/\": true,
        \"**/.svn\": true,
        \"**/CVS\": true,
        \"**/Thumbs.db\": true,
        \"venv/\": true,
    }
}" > .vscode/settings.json

# ==============================================================================
# Git
# ==============================================================================

git init
git add ./
git commit -a -m "Initial commit"

# ==============================================================================
# Virtual environment
# ==============================================================================

virtualenv venv
# TODO: Fix
# source ./venv/bin/activate
# env python -m pip install -U pip
# env python -m pip install -U -r requirements.txt
# env python -m pip install -U -r requirements.dev.txt
