#!/usr/bin/env python

"""Setup script"""

import setuptools

name = "{{ cookiecutter.project_slug }}"
version = "{{ cookiecutter.version }}"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split()

packages = (
    [name]
    + [name + "." + p for p in setuptools.find_packages(where="./" + name)]
)

setuptools.setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email="{{ cookiecutter.email }}",
    description="{{ cookiecutter.project_short_description }}",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=name,
    packages=packages,
    platforms="any",
    project_urls={
        "Issues": "https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues",
    },
    python_requires=">=3.8",
    url="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}",
    version=version,
)
