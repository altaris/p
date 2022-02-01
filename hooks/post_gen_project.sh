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
    ".gitignore"

# ==============================================================================
# Git
# ==============================================================================

git init
git add ./
git commit -a -m "Initial commit"
