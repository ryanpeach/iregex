# Py Idiomatic Regex (AKA iregex)

![TravisCI Build Status](https://travis-ci.com/ryanpeach/py_idiomatic_regex.svg?branch=master)
[![codecov](https://codecov.io/gh/ryanpeach/py_idiomatic_regex/branch/master/graph/badge.svg)](https://codecov.io/gh/ryanpeach/py_idiomatic_regex)

[Documentation Available Here](https://ryanpeach.github.io/py_idiomatic_regex)


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

And in python you would compile this like so:

```python
import re
re.compile(r"[a-zA-Z][_\w]*")
```

In this library the code would be:

```python
from iregex import Regex, ALPHA, ALPHA_NUMERIC, AnyChar, ZeroOrMore
(ALPHA + ZeroOrMore(AnyChar("_", ALPHA_NUMERIC))).compile()
```

Note: If you would like to use the `regex` library instead of `re` do this instead.

```python
import regex
from iregex import Regex, ALPHA, ALPHA_NUMERIC, AnyChar, ZeroOrMore
regex.compile(str(ALPHA + ZeroOrMore(AnyChar("_", ALPHA_NUMERIC))))
```

We do this to prevent the need for additional dependencies.

Just take a look at the documentation for the `Regex` class to get an idea of all the methods you can use!

You chain methods together for sequential operations and nest literals for nested operations.

# [PyParsing](https://github.com/pyparsing/pyparsing)

A lot of people will ask why use this over PyParsing? I actually had never heard of `pyparsing` before writing this library and sense have made updates that are inspired by `pyparsing`. The main reason I might use this over `pyparsing` is to stay specifically inside the Regex space using either the builtin `re` or `regex` library which can sometimes be faster than `pyparsing`. This library operates almost entirely on strings, which is a lot simpler than what `pyparsing` is doing under the hood. But please, use both!

# Contributions

Please make a contribution, this library is still growing!

Please download [poetry](https://python-poetry.org/) and run `poetry install` to set up your build environment.

We use `mypy` (so be sure to type your code), `flake8`, and `black` so be sure to use `pre-commit install` before your first push to comply with git pre-commit standards. Otherwise your pull request will not make it past TravisCI.

Always `pytest` your code and make PR's with good code coverage.
