# -*- coding: utf-8 -*-

import os
import setuptools

# ======================================================================================================================
# Fill in this information for each package.
# ======================================================================================================================

AUTHOR = "Jakrin Juangbhanich"
EMAIL = "juangbhanich.k@gmail.com"
PACKAGE_NAME = "k_util"
DESCRIPTION = "General utility scripts in Python 3.6."
REPO = "https://github.com/krinj/k-util"

# ======================================================================================================================
# Automatic Package Setup Script.
# ======================================================================================================================


with open("version", "r") as f:
    VERSION = f.readline()


def find_packages_under(path):
    """ Recursive list all of the packages under a specific package."""
    all_packages = setuptools.find_packages()
    packages = []
    for package in all_packages:
        package_split = package.split(".")
        if package_split[0] == path:
            packages.append(package)
    return packages


def copy_version_to_package(path):
    """ Copy the single source of truth version number into the package as well. """
    init_file = os.path.join(path, "__init__.py")
    with open(init_file, "r") as original_file:
        lines = original_file.readlines()

    with open(init_file, "w") as new_file:
        for line in lines:
            if "__version__" not in line:
                new_file.write(line)
            else:
                new_file.write("__version__ = \"{}\"\n".format(VERSION))


copy_version_to_package(PACKAGE_NAME)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    name=PACKAGE_NAME,
    description=DESCRIPTION,
    long_description=long_description,
    version=VERSION,
    url=REPO,
    packages=find_packages_under(PACKAGE_NAME),
    package_dir={PACKAGE_NAME: PACKAGE_NAME},
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)

# ===================================================================================================
# Upload to PyPI. Get the user and password from the environment.
# ===================================================================================================

repo_user = os.environ["REPO_USER"]
repo_pass = os.environ["REPO_PASS"]

with open("upload_to_pypi.sh", 'w') as f:
    f.write('#!/usr/bin/env bash\n')
    f.write('pip install twine\n')
    f.write('twine upload -u {} -p {} dist/*\n'.format(repo_user, repo_pass))
