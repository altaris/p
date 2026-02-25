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
# ML frameworks, model weights
*.ckpt
*.onnx
*.pt
*.pth
*.st
lightning_logs/
runs/
wandb/


# VSCode
*.code-workspace

# MacOS littering everywhere
.DS_Store

# My stuff
*_test.py
asdf/
bar/
foo/
foobar/
out/
output/
outputs/
secrets/
TODO.txt
" >> .gitignore

# ==============================================================================
# git
# ==============================================================================

git init
git config --local user.name "{{ cookiecutter.full_name }}"
git config --local user.email "{{ cookiecutter.email }}"
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