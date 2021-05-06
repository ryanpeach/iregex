# Py Idiomatic Regex (AKA iregex)

![TravisCI Build Status](https://travis-ci.com/ryanpeach/py_idiomatic_regex.svg?branch=master)
[![codecov](https://codecov.io/gh/ryanpeach/py_idiomatic_regex/branch/master/graph/badge.svg)](https://codecov.io/gh/ryanpeach/py_idiomatic_regex)

[Documentation Available Here](https://ryanpeach.github.com/py_idiomatic_regex)


An easier way to write regex in Python using OOP instead of strings.

Makes the code much easier to read and understand while still using Regex under the hood.

Very easy to use, entirely contained within two files `consts.py` and `regex.py`.

## Installation

[Available on PyPi](https://pypi.org/project/iregex/)

`pip install iregex`

## Examples

Imagine a regex to match variable names in most common languages.

They must start with an alphabetical character, then for the second character on they can contain numbers and underscores as well.

The regex for this would be:

`[a-zA-Z][_\w]*`

In this library the code would be:

```python
from iregex import Regex
from iregex.consts import ALPHA, ALPHA_NUMERIC
Regex(ALPHA).literal(
    Regex().any_char("_", ALPHA_NUMERIC).zero_or_more_repetitions()
)
```

Just take a look at the documentation for the `Regex` class to get an idea of all the methods you can use!

You chain methods together for sequential operations and nest literals for nested operations.

# Contributions

Please make a contribution, this library is still growing!

Please download [poetry](https://python-poetry.org/) and run `poetry install` to set up your build environment.

We use `mypy` (so be sure to type your code), `flake8`, and `black` so be sure to use `pre-commit install` before your first push to comply with git pre-commit standards. Otherwise your pull request will not make it past TravisCI.

Always `pytest` your code and make PR's with good code coverage.
