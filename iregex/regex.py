"""
This is the module containing the main Regex class.
"""

import re
from copy import copy
from typing import List, Optional, Union, Any

from iregex.consts import ANY, ONE_OR_MORE, OPTIONAL, WHITESPACE, ZERO_OR_MORE, NEWLINE
from iregex.exceptions import NonEmptyError, SetIntersectionError, NotACharacterException


class Regex:
    """
    A wrapper for regex strings that hides the implementation.

    This class is immutable by convention.
    """

    # Private Variables
    _data: List[str]
    _capture_groups: List[str]

    def __init__(self, regex_str: Optional[str] = None) -> None:
        """
        Optionally can take a literal as input.

        :param regex_str: An optional literal to start your Regex with.
        """
        self._data = [regex_str] if regex_str else []
        self._capture_groups = []

    # ============== Chained Methods ==============
    def literal(self, regex: Union[str, "Regex"]) -> "Regex":
        """
        Adds a literal to the end of the regex.

        :param regex: The regex to append to this regex.
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

    def newline(self) -> "Regex":
        """Allows newline."""
        out = copy(self)
        out._data.append(NEWLINE + ZERO_OR_MORE)
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
        """
        Repeats the previous regex m to n inclusive times.

        :param m: At least this many times.
        :param n: At most this many times (inclusive).
        """
        out = self.make_non_capture_group()
        out._data.append("{" + str(m) + "," + str(n) + "}")
        return out

    def exactly_m_repetitions(self, m: int) -> "Regex":
        """
        Repeats the previous regex exactly m times.

        :param m: Exactly this many instances.
        """
        out = self.make_non_capture_group()
        out._data.append("{" + str(m) + "}")
        return out

    def m_or_more_repetitions(self, m: int) -> "Regex":
        """
        Repeats the previous regex m or more times.

        :param m: This many or more instances.
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

    def any_char(self, *char: str) -> "Regex":
        """
        Any char in the text may be used.

        :param char: Some character.
        :raises NotACharacterException: Raised if any argument is not a character.
        """
        out = copy(self)
        for t in char:
            if not Regex._is_character(t):
                raise NotACharacterException(f"{t} is not a character.")
        if len(char) > 1:
            out._data += ["["] + list(char) + ["]"]
        else:
            out._data = list(char)
        return out

    def exclude_char(self, *char: str) -> "Regex":
        """
        None of the chars in the text may be used.

        :param char: Some character.
        :raises NotACharacterException: Raised if any argument is not a character.
        """
        out = copy(self)
        for t in char:
            if not Regex._is_character(t):
                raise NotACharacterException(f"{t} is not a character.")
        out._data += ["[^"] + list(char) + ["]"]
        return out

    def make_capture_group(self) -> "Regex":
        """Creates an anonymous capture group."""
        out = copy(self)
        out._data = ["("] + out._data + [")"]
        return out

    @staticmethod
    def _is_character(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is just a single character."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if len(txt_) == 1:
            return True
        if len(txt_) == 2 and txt_[0] == '\\':
            return True
        return False

    @staticmethod
    def _is_character_group(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is a character group."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if len(txt_) >= 2 and txt_[0] == r'[' and txt_[-1] == r']':
            return True
        return False

    @staticmethod
    def _is_capture_group(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is a capture group."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if len(txt_) >= 2 and txt_[0] == r'(' and txt_[-1] == r')':
            return True
        return False

    def make_non_capture_group(self) -> "Regex":
        """Create a capture group that you don't care to retreive the contents of."""
        out = copy(self)
        # You don't need to make a non_capture_group for simple cases
        if Regex._is_character(self) or \
                Regex._is_character_group(self) or \
                Regex._is_capture_group(self):
            out._data = out._data
        else:
            out._data = ["(?:"] + out._data + [")"]
        return out

    def make_named_capture_group(self, name: str) -> "Regex":
        """
        Makes the previous regex a capture group of name `name`.

        :param name: The name to assign the capture group.
        """
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
    def compile(self, *args: Any, **kwargs: Any) -> re.Pattern:
        """
        A simple wrapper around re.compile.

        :param args: Positional parameters to pass to re.compile.
        :param kwargs: Keyword parameters to pass to re.compile.
        """
        return re.compile(str(self), *args, **kwargs)

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

    def __add__(self, other: Union["Regex", str]) -> "Regex":
        """
        Adding two Regex's is just appending their strings.
        But they aren't allowed to share capture group names.
        Can be used as an easy substitute for literal. But is a little slower.

        :raises SetIntersectionError: If the two _capture_groups share any values.
        :raises TypeError: If other is not either a Regex or a string.
        """
        # Handle data types
        if isinstance(other, str):
            other_ = Regex(other)
        elif isinstance(other, Regex):
            other_ = other
            if set(self._capture_groups) & set(other._capture_groups):
                raise SetIntersectionError(
                    "Capture groups in self and other have common names."
                )
        else:
            raise TypeError(f"Unrecognized type: {type(other)}")
        del other  # So you don't reuse the variable

        out = Regex()
        out._data = self._data + other_._data
        out._capture_groups = self._capture_groups + other_._capture_groups
        return out

    def __radd__(self, other: Union["Regex", str]) -> "Regex":
        """
        Adding two Regex's is just appending their strings.
        But they aren't allowed to share capture group names.
        Can be used as an easy substitute for literal. But is a little slower.

        :raises SetIntersectionError: If the two _capture_groups share any values.
        :raises TypeError: If other is not either a Regex or a string.
        """
        # Handle data types
        if isinstance(other, str):
            other_ = Regex(other)
        elif isinstance(other, Regex):
            other_ = other
            if set(self._capture_groups) & set(other._capture_groups):
                raise SetIntersectionError(
                    "Capture groups in self and other have common names."
                )
        else:
            raise TypeError(f"Unrecognized type: {type(other)}")
        del other  # So you don't reuse the variable

        out = Regex()
        out._data = other_._data + self._data
        out._capture_groups = other_._capture_groups + self._capture_groups
        return out

    def __or__(self, other: Union[str, "Regex"]) -> "Regex":
        """
        The `or` of two Regex's is the group `(self|other)`.
        Neither self nor other may contained named capture groups.

        :raises NonEmptyError: If either contains named capture groups.
        """
        # Handle data types
        if isinstance(other, str):
            other_ = Regex(other)
        elif isinstance(other, Regex):
            other_ = other
            if other._capture_groups:
                raise NonEmptyError(
                    f"Capture groups in other is not empty. Found: {other._capture_groups}"
                )
        else:
            raise TypeError(f"Unrecognized type: {type(other)}")
        del other  # So you don't reuse the variable

        # Some other errors
        if self._capture_groups:
            raise NonEmptyError(
                f"Capture groups in self is not empty. Found: {self._capture_groups}"
            )

        out = Regex()
        out._data = ["(?:"] + self._data + ["|"] + other_._data + [")"]
        out._capture_groups = []
        return out

    def __ror__(self, other: Union[str, "Regex"]) -> "Regex":
        """
        The `or` of two Regex's is the group `(self|other)`.
        Neither self nor other may contained named capture groups.

        :raises NonEmptyError: If either contains named capture groups.
        """
        # Handle data types
        if isinstance(other, str):
            other_ = Regex(other)
        elif isinstance(other, Regex):
            other_ = other
            if other._capture_groups:
                raise NonEmptyError(
                    f"Capture groups in other is not empty. Found: {other._capture_groups}"
                )
        else:
            raise TypeError(f"Unrecognized type: {type(other)}")
        del other  # So you don't reuse the variable

        # Some other errors
        if self._capture_groups:
            raise NonEmptyError(
                f"Capture groups in self is not empty. Found: {self._capture_groups}"
            )

        out = Regex()
        out._data = ["(?:"] + other_._data + ["|"] + self._data + [")"]
        out._capture_groups = []
        return out
