# Py Idiomatic Regex (AKA iregex)

![TravisCI Build Status](https://travis-ci.com/ryanpeach/py_idiomatic_regex.svg?branch=master)

An easier way to write regex in Python using OOP instead of strings.

Makes the code much easier to read and understand while still using Regex under the hood.

Very easy to use, entirely contained within two files `consts.py` and `regex.py`.

## Examples

Imagine a regex to match variable names in most common languages.

They must start with an alphabetical character, then for the second character on they can contain numbers and underscores as well.

The regex for this would be:

`[a-zA-Z][_\w]*`

In this library the code would be:

```python
from py_idiomatic_regex import *
Regex(ALPHA).literal(
    Regex().any_char("_", ALPHA_NUMERIC).zero_or_more_repetitions()
)
```

You chain methods together for sequential operations and nest literals for nested operations.

# Contributions

Please make a contribution, this library is still growing!

Please download [poetry](https://python-poetry.org/) and run `poetry install` to set up your build environment.

Please run `pre-commit install` to comply with git pre-commit standards.

Always `pytest` your code.
