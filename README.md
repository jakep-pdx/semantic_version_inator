# semantic_version_inator

Utility to aid in incrementing the semantic version of a Python package in an automated build.

How to use:

Set up CI/CD pipeline/workflow to set parameters: `release_type` and `current_version`

The `release_type` parameter should have a default value of PATCH, with an option to set as MINOR 
or MAJOR as appropriate. This param could be user selectable when manually triggering a build, or 
could be automated if a means of programatically determining type of release is possible.

The `current_version` parameter must be derrived from the latest published package version. 
One option is to download the latest (i.e. pip download) and parse the file name from the file.

Installing this package installs two console commands, each taking the two arguments noted above: 

`get_next_ver_file_name` is a convenience function, intended to parse the current version 
from a pakcage file name, i.e. pkg_name-0.0.0-py3-none-any.whl:

example input:
```
get_next_ver_file_name pkg_name-0.0.0-py3-none-any.whl PATCH
```
example output:
```
0.0.1
```

`get_next_ver` is an alternative to the above in case the above does not handle a given package
name well, or if the version is obtained independently of the current version package file name. 
It is intended to receive the current semantic version (not file name), i.e. 0.0.0:

example input:
```
get_next_ver 0.0.0 PATCH
```
example output:
```
0.0.1
```

Set the new version number as an environment variable, which setup.py can use, i.e.:

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
