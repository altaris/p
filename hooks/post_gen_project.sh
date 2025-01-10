#!/bin/bash

# ==============================================================================
# uv
# ==============================================================================

uv sync

# ==============================================================================
# .gitignore
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
# git
# ==============================================================================

git init
git add ./
git commit -a -m "Initial commit"

# ==============================================================================
# push to github
# ==============================================================================

{% if cookiecutter.push_to_github|lower == 'y' %}
REPO='{{ cookiecutter.github_username }}/{{ cookiecutter.project_name|lower|replace(' ', '-') }}.git'
echo "Pushing to $REPO"
git remote add origin git@github.com:$REPO
git branch -M master
git push -u origin master
{% endif %}