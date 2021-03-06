# semantic-version-inator

Utility to aid in incrementing the semantic version of a Python package in an automated build.

How to use:

Set up CI/CD pipeline/workflow to set parameters: `release_type` and `current_version`

The `release_type` parameter should have a default value of PATCH, with an option to set as MINOR 
or MAJOR as appropriate. This param could be user selectable when manually triggering a build, or 
could be automated if a means of programmatically determining type of release is possible.

The `current_version` parameter must be derived from the latest published package version. 
One option is to download the latest (i.e. pip download) and parse the file name from the file.

Installing this package installs two console commands, each taking the two arguments noted above: 

`get_next_ver_file_name` is a convenience function, intended to parse the current version 
from a package file name, i.e. pkg_name-0.0.0-py3-none-any.whl:

input/output examples:
```
get_next_ver_file_name pkg_name-0.0.0-py3-none-any.whl PATCH
0.0.1
```
```
get_next_ver_file_name pkg_name-0.0.0-py3-none-any.whl MINOR
0.1.0
```
```
get_next_ver_file_name pkg_name-0.0.0-py3-none-any.whl MAJOR
1.0.0
```

`get_next_ver` is an alternative to the above in case the above does not handle a given package
name well, or if the version is obtained independently of the current version package file name. 
It is intended to receive the current semantic version (not file name), i.e. 0.0.0:

input/output examples:
```
get_next_ver 0.0.0 PATCH
0.0.1
```
```
get_next_ver 0.0.0 MINOR
0.1.0
```
```
get_next_ver 0.0.0 MAJOR
1.0.0
```

When the new version number is derived using one of the options above, set it as an environment 
variable, which setup.py can use to dynamically set during the package build process, i.e.:

setup.py sample content:

```
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
    ...
    version=PKG_VERSION,
    ...
)
```

Example Github Actions workflow using the above - note:
 - replace <<<PROJECT_NAME>>> with actual repository directory (project) name
 - assumes this package is pip installed as one of the dev-dependencies

```
name: Build <<<PROJECT_NAME>>>

on:
  push:
    branches:
      - "main"
  workflow_dispatch:
    inputs:
      publishPackage:
        description: Publish Package
        required: true
        default: false
        type: boolean
      versionType:
        description: 'Version Type'
        required: true
        default: 'PATCH'
        type: choice
        options:
        - 'PATCH'
        - 'MINOR'
        - 'MAJOR'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
      with:
        path: <<<PROJECT_NAME>>>
    
    - name: set vars
      run: |
        publishPackage="false"
        if [ "${{ github.event.inputs.publishPackage }}" != "" ]
        then
          publishPackage="${{ github.event.inputs.publishPackage }}"
        fi
        echo "publishPackage=$publishPackage" >> $GITHUB_ENV

        versionType="PATCH"
        if [ "${{ github.event.inputs.versionType }}" != "" ]
        then
          versionType="${{ github.event.inputs.versionType }}"
        fi
        echo "versionType=$versionType" >> $GITHUB_ENV

    - name: check vars
      run: |
        echo "publishPackage: ${{ env.publishPackage }}"
        echo "versionType: ${{ env.versionType }}"

    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f <<<PROJECT_NAME>>>/requirements-dev.txt ]; then pip install -r <<<PROJECT_NAME>>>/requirements-dev.txt; fi

    - name: Run pylint
      run: |
        pylint <<<PROJECT_NAME>>>/<<<PROJECT_NAME>>> --fail-under=8

    - name: Run pytest
      run: |
        pytest <<<PROJECT_NAME>>> --cov-report=html --cov-branch --cov=.

    - name: Check coverage
      run: |
        coverage report --fail-under=80 --omit="setup.py,*/__init__.py,*/tests/*"

    - name: Get next version
      continue-on-error: true
      run: |
        pip download <<<PROJECT_NAME>>>
        file_name=$(ls <<<PROJECT_NAME>>>*.whl)
        if [ "$file_name" != "" ]
          then
          new_ver=$(get_next_ver_file_name $file_name ${{ env.versionType }})
          echo "new_ver: "$new_ver
          echo "new_ver=$new_ver" >> $GITHUB_ENV
        else
          echo "unable to get next version"
        fi

    - name: Build package
      run: |
        cd <<<PROJECT_NAME>>>
        python -m build --wheel

    - name: Publish package to pypi
      if: ${{ env.publishPackage == 'true' }}
      uses: pypa/gh-action-pypi-publish@release/v1.5
      with:
        user: __token__
        password: ${{ secrets.PYPI_API_TOKEN }}
        packages_dir: <<<PROJECT_NAME>>>/dist

```