import re
from copy import copy
from typing import List, Optional, Union

from iregex.consts import ANY, ONE_OR_MORE, OPTIONAL, WHITESPACE, ZERO_OR_MORE
from iregex.exceptions import NonEmptyError, SetIntersectionError


class Regex:
    """A wrapper for regex strings that hides the implementation."""

    # Private Variables
    _data: List[str]
    _capture_groups: List[str]

    def __init__(self, regex_str: Optional[str] = None) -> None:
        """Optionally can take a literal as input."""
        self._data = [regex_str] if regex_str else []
        self._capture_groups = []

    # ============== Chained Methods ==============
    def literal(self, regex: Union[str, "Regex"]) -> "Regex":
        """
        Adds a literal to the end of the regex.
        :raises TypeError: When regex is not type Regex or str.
        """
        out = copy(self)
        if isinstance(regex, Regex):
            out._data += regex._data
        elif isinstance(regex, str):
            out._data.append(regex)
        else:
            raise TypeError(f"Type not supported: {type(regex)}")
        return out

    def anything(self) -> "Regex":
        """Appends zero or more of any character to the Regex."""
        return self.literal(ANY + ZERO_OR_MORE)

    def whitespace(self) -> "Regex":
        """Allows unlimited whitespace."""
        out = copy(self)
        out._data.append(WHITESPACE + ZERO_OR_MORE)
        return out

    def zero_or_more_repetitions(self) -> "Regex":
        """Repeats the previous regex zero or more times."""
        out = self.make_non_capture_group()
        out._data.append(ZERO_OR_MORE)
        return out

    def one_or_more_repetitions(self) -> "Regex":
        """Repeats the previous regex one or more times."""
        out = self.make_non_capture_group()
        out._data.append(ONE_OR_MORE)
        return out

    def m_to_n_repetitions(self, m: int, n: int) -> "Regex":
        """Repeats the previous regex m to n inclusive times."""
        out = self.make_non_capture_group()
        out._data.append("{" + str(m) + "," + str(n) + "}")
        return out

    def exactly_m_repetitions(self, m: int) -> "Regex":
        """Repeats the previous regex exactly m times."""
        out = self.make_non_capture_group()
        out._data.append("{" + str(m) + "}")
        return out

    def m_or_more_repetitions(self, m: int) -> "Regex":
        """
        Repeats the previous regex m or more times.
        :raises ValueError: When m < 0
        """
        if m == 0:
            return self.zero_or_more_repetitions()
        elif m == 1:
            return self.one_or_more_repetitions()
        elif m < 0:
            raise ValueError(f"m must be >= 0, got {m}")
        return self.exactly_m_repetitions(m - 1) + self.one_or_more_repetitions()

    def optional(self) -> "Regex":
        """The previous regex can exist 0 or 1 times."""
        out = self.make_non_capture_group()
        out._data.append(OPTIONAL)
        return out

    def any_char(self, *text: str) -> "Regex":
        """Any char in the text may be used."""
        out = copy(self)
        out._data += ["["] + list(text) + ["]"]
        return out

    def exclude_char(self, *text: str) -> "Regex":
        """None of the chars in the text may be used."""
        out = copy(self)
        out._data += ["[^"] + list(text) + ["]"]
        return out

    def make_capture_group(self) -> "Regex":
        """Creates an anonymous capture group."""
        out = copy(self)
        out._data = ["("] + out._data + [")"]
        return out

    def make_non_capture_group(self) -> "Regex":
        """Create a capture group that you don't care to retreive the contents of."""
        out = copy(self)
        out._data = ["(?:"] + out._data + [")"]
        return out

    def make_named_capture_group(self, name: str) -> "Regex":
        """Makes the previous regex a capture group of name `name`."""
        out = copy(self)
        out._data = ["(?<" + name + ">"] + out._data + [")"]
        out._capture_groups.append(name)
        return out

    def make_lookahead(self) -> "Regex":
        """Makes the previous regex a lookahead group."""
        out = copy(self)
        out._data = ["(?="] + self._data + [")"]
        return out

    def make_lookbehind(self) -> "Regex":
        """Makes the previous regex a lookbehind group."""
        out = copy(self)
        out._data = ["(?<="] + self._data + [")"]
        return out

    def make_negative_lookahead(self) -> "Regex":
        """Makes the previous regex a negative lookahead group."""
        out = copy(self)
        out._data = ["(?!"] + self._data + [")"]
        return out

    def make_negative_lookbehind(self) -> "Regex":
        """Makes the previous regex a negative lookbehind group."""
        out = copy(self)
        out._data = ["(?<!"] + self._data + [")"]
        return out

    # ============== Result Methods =============
    def compile(self) -> re.Pattern:
        """A simple wrapper around re.compile"""
        return re.compile(str(self))

    # ============== Magic Methods ==============
    def __copy__(self) -> "Regex":
        """A simple copy command."""
        out = Regex()
        out._data = copy(self._data)
        out._capture_groups = copy(self._capture_groups)
        return out

    def __str__(self) -> str:
        """Converts this object into a regex string."""
        return "".join(self._data)

    def __repr__(self) -> str:
        """For debugging and printing."""
        return "Regex(" + str(self) + ")"

    def __eq__(self, other: "Regex") -> bool:  # type: ignore
        """Two Regex's are equal if their regex strings are equal."""
        return str(self) == str(other)

    def __add__(self, other: "Regex") -> "Regex":
        """
        Adding two Regex's is just appending their strings. But they aren't allowed to share capture group names.
        :raises SetIntersectionError: If the two _capture_groups share any values.
        """
        out = Regex()
        out._data = self._data + other._data
        if set(self._capture_groups) & set(other._capture_groups):
            raise SetIntersectionError(
                "Capture groups in self and other have common names."
            )
        out._capture_groups = self._capture_groups + other._capture_groups
        return out

    def __or__(self, other: "Regex") -> "Regex":
        """
        The `or` of two Regex's is the group `(self|other)`.
        Neither self nor other may contained named capture groups.
        :raises NonEmptyError: If either contains named capture groups.
        """
        out = Regex()
        if self._capture_groups:
            raise NonEmptyError(
                f"Capture groups in self is not empty. Found: {self._capture_groups}"
            )
        if other._capture_groups:
            raise NonEmptyError(
                f"Capture groups in other is not empty. Found: {other._capture_groups}"
            )
        out._data = ["(?:"] + self._data + ["|"] + other._data + [")"]
        out._capture_groups = []
        return out
