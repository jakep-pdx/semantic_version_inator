""" packaging config """
import os
from setuptools import setup, find_packages

# with open("requirements.txt", encoding="utf-8") as req:
#     requirements = req.read().splitlines()


PKG_VERSION = "0.0.0"
try:
    new_ver = os.environ["new_ver"]
    if new_ver:
        PKG_VERSION = new_ver
    else:
        print("new_ver not found, using PKG_VERSION default:", PKG_VERSION)
except KeyError:
    print("new_ver not found, using PKG_VERSION default:", PKG_VERSION)

setup(
    name = "semantic_version_inator",
    description = "Utility to aid in incrementing the semantic version of a Python package in an automated build",
    long_description = "Utility to aid in incrementing the semantic version of a Python package in an automated build",
    version = PKG_VERSION,
    python_requires = ">=3.10",
    install_requires = "",
    license="Apache License 2.0",
    classifiers=[
        'License :: OSI Approved :: Apache Software License'
    ],
    pakckages = find_packages(include=["semantic_version_inator", "semantic_version_inator.*"]),
    entry_points = {
        'console_scripts': [
            'get_next_ver=semantic_version_inator.console:get_next_ver',
            'get_next_ver_file_name=semantic_version_inator.console:get_next_ver_file_name'
        ]
    }
)
