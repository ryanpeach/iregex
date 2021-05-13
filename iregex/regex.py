"""
This is the module containing the main Regex class.
"""

import re
from copy import copy
from typing import Any, List, Optional, Union

from iregex.consts import ANY, NEWLINE, ONE_OR_MORE, OPTIONAL, WHITESPACE, ZERO_OR_MORE
from iregex.exceptions import (
    AlreadyCapturedException,
    AlreadyRepeatingException,
    NonEmptyError,
    NotACharacterException,
    SetIntersectionError,
)


class Regex:
    """
    A wrapper for regex strings that hides the implementation.

    This class is immutable by convention.

    .. testsetup::

            from iregex import Regex

    .. doctest::

        >>> Regex()
        Regex(r"")

        >>> Regex("asdf")
        Regex(r"asdf")

    :param regex_str: An optional literal to start your Regex with.
    """

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
        Adds a literal to the end of the regex. Also aliases to `+`.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").literal(' ').literal('world')
            Regex(r"hello world")

            >>> Regex("hello") + ' ' + 'world'
            Regex(r"hello world")

            >>> "hello" + ' ' + Regex('world')
            Regex(r"hello world")

        :param regex: The regex to append to this regex.
        :raises SetIntersectionError: If the two _capture_groups share any values.
        :raises TypeError: If other is not either a Regex or a string.
        """
        return self + regex

    def logical_or(self, regex: Union[str, "Regex"]) -> "Regex":
        """
        The `logical_or` of two Regex's. Also aliases to `|`.

        Neither `self` nor `regex` may contained named capture groups.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").logical_or('world')
            Regex(r"(?:hello|world)")

            >>> Regex("hello") | 'world'
            Regex(r"(?:hello|world)")

            >>> "hello" | Regex('world')
            Regex(r"(?:hello|world)")

            >>> Regex("fizz") | Regex('buzz') | Regex('fizzbuzz')
            Regex(r"(?:fizz|buzz|fizzbuzz)")

        :raises NonEmptyError: If either contains named capture groups.
        """
        return self | regex

    def anything(self) -> "Regex":
        """
        Appends zero or more of any character to the Regex.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").anything().literal("world")
            Regex(r"hello.*world")

        """
        return self.literal(ANY + ZERO_OR_MORE)

    def whitespace(self) -> "Regex":
        r"""
        Allows unlimited whitespace.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").whitespace().literal("world")
            Regex(r"hello\s*world")

        """
        out = copy(self)
        out._data.append(WHITESPACE + ZERO_OR_MORE)
        return out

    def newlines(self) -> "Regex":
        r"""
        Allows newlines after text.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").newlines().literal("world")
            Regex(r"hello(?:\n|\r\n?)*world")

        """
        out = copy(self)
        out._data.append(NEWLINE + ZERO_OR_MORE)
        return out

    @staticmethod
    def _is_repeating(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is repeating."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        return txt_[-1] in (r"?", r"*", r"+", r"}")

    def zero_or_more_repetitions(self) -> "Regex":
        """
        Repeats the previous regex zero or more times.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("a").zero_or_more_repetitions()
            Regex(r"a*")

            >>> Regex("[asdf]").zero_or_more_repetitions()
            Regex(r"[asdf]*")

            >>> Regex("hello world").zero_or_more_repetitions()
            Regex(r"(?:hello world)*")

        :raises AlreadyRepeatingException: If this is already a repeating regex.
        """
        if Regex._is_repeating(self):
            raise AlreadyRepeatingException("{self} is already repeating.")
        out = self.make_non_capture_group()
        out._data.append(ZERO_OR_MORE)
        return out

    def one_or_more_repetitions(self) -> "Regex":
        """
        Repeats the previous regex one or more times.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("a").one_or_more_repetitions()
            Regex(r"a+")

            >>> Regex("[asdf]").one_or_more_repetitions()
            Regex(r"[asdf]+")

            >>> Regex("hello world").one_or_more_repetitions()
            Regex(r"(?:hello world)+")

        :raises AlreadyRepeatingException: If this is already a repeating regex.
        """
        if Regex._is_repeating(self):
            raise AlreadyRepeatingException("{self} is already repeating.")
        out = self.make_non_capture_group()
        out._data.append(ONE_OR_MORE)
        return out

    def m_to_n_repetitions(self, m: int, n: int) -> "Regex":
        """
        Repeats the previous regex m to n inclusive times.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("a").m_to_n_repetitions(0, 1)
            Regex(r"a?")

            >>> Regex("a").m_to_n_repetitions(3, 5)
            Regex(r"a{3,5}")

            >>> Regex("[asdf]").m_to_n_repetitions(3, 5)
            Regex(r"[asdf]{3,5}")

            >>> Regex("hello world").m_to_n_repetitions(3, 5)
            Regex(r"(?:hello world){3,5}")

        :param m: At least this many times.
        :param n: At most this many times (inclusive).
        :raises AlreadyRepeatingException: If this is already a repeating regex.
        """
        if Regex._is_repeating(self):
            raise AlreadyRepeatingException("{self} is already repeating.")
        out = self.make_non_capture_group()
        if m == 0 and n == 1:
            out._data.append(OPTIONAL)
        else:
            out._data.append("{" + str(m) + "," + str(n) + "}")
        return out

    def exactly_m_repetitions(self, m: int) -> "Regex":
        """
        Repeats the previous regex exactly m times.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("a").exactly_m_repetitions(3)
            Regex(r"a{3}")

            >>> Regex("[asdf]").exactly_m_repetitions(3)
            Regex(r"[asdf]{3}")

            >>> Regex("hello world").exactly_m_repetitions(3)
            Regex(r"(?:hello world){3}")

        :param m: Exactly this many instances.
        :raises AlreadyRepeatingException: If this is already a repeating regex.
        """
        if Regex._is_repeating(self):
            raise AlreadyRepeatingException("{self} is already repeating.")
        out = self.make_non_capture_group()
        out._data.append("{" + str(m) + "}")
        return out

    def m_or_more_repetitions(self, m: int) -> "Regex":
        """
        Repeats the previous regex m or more times.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("a").m_or_more_repetitions(0)
            Regex(r"a*")

            >>> Regex("a").m_or_more_repetitions(1)
            Regex(r"a+")

            >>> Regex("a").m_or_more_repetitions(3)
            Regex(r"a{3,}")

            >>> Regex("[asdf]").m_or_more_repetitions(3)
            Regex(r"[asdf]{3,}")

            >>> Regex("hello world").m_or_more_repetitions(3)
            Regex(r"(?:hello world){3,}")

        :param m: This many or more instances.
        :raises ValueError: When m < 0
        :raises AlreadyRepeatingException: If this is already a repeating regex.
        """
        if Regex._is_repeating(self):
            raise AlreadyRepeatingException("{self} is already repeating.")
        if m == 0:
            return self.zero_or_more_repetitions()
        elif m == 1:
            return self.one_or_more_repetitions()
        elif m < 0:
            raise ValueError(f"m must be >= 0, got {m}")
        out = self.make_non_capture_group()
        out._data.append("{" + str(m) + ",}")
        return out

    def optional(self) -> "Regex":
        """
        The previous regex can exist 0 or 1 times.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("a").optional()
            Regex(r"a?")

            >>> Regex("[asdf]").optional()
            Regex(r"[asdf]?")

            >>> Regex("hello world").optional()
            Regex(r"(?:hello world)?")

        :raises AlreadyRepeatingException: If this is already a repeating regex.
        """
        if Regex._is_repeating(self):
            raise AlreadyRepeatingException("{self} is already repeating.")
        out = self.make_non_capture_group()
        out._data.append(OPTIONAL)
        return out

    @staticmethod
    def _is_character(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is just a single character."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if len(txt_) == 1:
            return True
        if len(txt_) == 2 and txt_[0] == "\\":
            return True
        return False

    def any_char(self, *char: Union["Regex", str]) -> "Regex":
        """
        Any of the characters listed as parameters may be used.

        Pass characters as parameters one at a time like so:

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex().any_char('a')
            Regex(r"a")

            >>> Regex("hello").any_char('w', 'o', 'r', 'l', 'd')
            Regex(r"hello[world]")

        :param char: Some character.
        :raises NotACharacterException: Raised if any argument is not a character.
        """
        out = copy(self)
        for t in char:
            if not Regex._is_character(t):
                raise NotACharacterException(fr"{t} is not a character.")
        if len(char) > 1:
            out._data += ["["] + [str(c) for c in char] + ["]"]
        else:
            out._data = [str(c) for c in char]
        return out

    def exclude_char(self, *char: Union["Regex", str]) -> "Regex":
        """
        None of the characters listed as parameters may be used.

        Pass characters as parameters one at a time like so:

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").exclude_char('w', 'o', 'r', 'l', 'd')
            Regex(r"hello[^world]")

        :param char: Some character.
        :raises NotACharacterException: Raised if any argument is not a character.
        """
        out = copy(self)
        for t in char:
            if not Regex._is_character(t):
                raise NotACharacterException(fr"{t} is not a character.")
        out._data += ["[^"] + [str(c) for c in char] + ["]"]
        return out

    @staticmethod
    def _is_character_group(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is a character group."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if len(txt_) >= 2 and txt_[0] == r"[" and txt_[-1] == r"]":
            return True
        return False

    @staticmethod
    def _is_named_capture_group(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is a named capture group."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if len(txt_) >= 5 and txt_[0:3] == r"(?<" and txt_[-1] == r")":
            return True
        return False

    @staticmethod
    def _is_non_capture_group(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is a non capture group."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if not Regex._is_named_capture_group(txt):
            if len(txt_) >= 4 and txt_[0:3] == r"(?:" and txt_[-1] == r")":
                return True
        return False

    @staticmethod
    def _is_capture_group(txt: Union[str, "Regex"]) -> bool:
        """Tests if a regex string is a capture group."""
        txt_: str = str(txt) if isinstance(txt, Regex) else txt
        if not Regex._is_named_capture_group(txt) and not Regex._is_non_capture_group(
            txt
        ):
            if len(txt_) >= 2 and txt_[0] == r"(" and txt_[-1] == r")":
                return True
        return False

    def make_capture_group(self) -> "Regex":
        """
        Creates an anonymous capture group.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex(".*").make_capture_group().literal("world")
            Regex(r"(.*)world")

            >>> Regex(".*").make_capture_group().make_capture_group().literal("world")
            Regex(r"(.*)world")

            >>> Regex(".*").make_non_capture_group().make_capture_group().literal("world")
            Regex(r"(.*)world")

        :raises AlreadyCapturedException: If this is already a named capture group.
        """
        if Regex._is_named_capture_group(self):
            raise AlreadyCapturedException(f"This is already a capture group: {self}")
        if Regex._is_capture_group(self):
            return self
        out = copy(self)
        if Regex._is_non_capture_group(self):
            out._data = ["(", str(out)[3:-1], ")"]
        else:
            out._data = ["("] + out._data + [")"]
        return out

    def make_non_capture_group(self) -> "Regex":
        """
        Intelligently creates a capture group that you don't care to retreive the contents of.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("h").make_non_capture_group()  # This is unnecessary so it fails
            Regex(r"h")

            >>> Regex("[asdf]").make_non_capture_group()  # This is unnecessary so it fails
            Regex(r"[asdf]")

            >>> Regex("hello world").make_non_capture_group()  # This succeeds
            Regex(r"(?:hello world)")

            >>> Regex("hello world").make_capture_group().make_non_capture_group()  # This succeeds
            Regex(r"(?:hello world)")

        :raises AlreadyCapturedException: If this is already a named capture group.
        """
        out = copy(self)
        # You don't need to make a non_capture_group for simple cases
        if (
            Regex._is_character(self)
            or Regex._is_character_group(self)
            or Regex._is_non_capture_group(self)
        ):
            out._data = out._data
        elif Regex._is_named_capture_group(self):
            raise AlreadyCapturedException(f"This is already a capture group: {self}")
        elif Regex._is_capture_group(self):
            out._data = ["(?:", str(out)[1:-1], ")"]
        else:
            out._data = ["(?:"] + out._data + [")"]
        return out

    def make_named_capture_group(self, name: str) -> "Regex":
        """
        Makes the previous regex a capture group of name `name`.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex(".*").make_named_capture_group("hello").literal("world")
            Regex(r"(?<hello>.*)world")

            >>> Regex(".*").make_non_capture_group().make_named_capture_group("hello").literal("world")
            Regex(r"(?<hello>.*)world")

            >>> Regex(".*").make_capture_group().make_named_capture_group("hello").literal("world")
            Regex(r"(?<hello>.*)world")

        :param name: The name to assign the capture group.
        :raises AlreadyCapturedException: If this is already a named capture group.
        """
        out = copy(self)
        if Regex._is_non_capture_group(self):
            out._data = ["(?<", name, ">", str(out)[3:-1], ")"]
        elif Regex._is_capture_group(self):
            out._data = ["(?<", name, ">", str(out)[1:-1], ")"]
        elif Regex._is_named_capture_group(self):
            raise AlreadyCapturedException(f"{self} is already a named capture group.")
        else:
            out._data = ["(?<", name, ">"] + out._data + [")"]
            out._capture_groups.append(name)
        return out

    def make_lookahead(self) -> "Regex":
        """
        Makes the previous regex a lookahead group.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello") + (Regex("world").make_lookahead())
            Regex(r"hello(?=world)")

        """
        out = copy(self)
        out._data = ["(?="] + self._data + [")"]
        return out

    def make_lookbehind(self) -> "Regex":
        """
        Makes the previous regex a lookbehind group.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").make_lookbehind() + "world"
            Regex(r"(?<=hello)world")

        """
        out = copy(self)
        out._data = ["(?<="] + self._data + [")"]
        return out

    def make_negative_lookahead(self) -> "Regex":
        """
        Makes the previous regex a negative lookahead group.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello") + (Regex("world").make_negative_lookahead())
            Regex(r"hello(?!world)")

        """
        out = copy(self)
        out._data = ["(?!"] + self._data + [")"]
        return out

    def make_negative_lookbehind(self) -> "Regex":
        """
        Makes the previous regex a negative lookbehind group.

        .. testsetup::

            from iregex import Regex

        .. doctest::

            >>> Regex("hello").make_negative_lookbehind() + "world"
            Regex(r"(?<!hello)world")

        """
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
        return 'Regex(r"' + str(self) + '")'

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
        if Regex._is_non_capture_group(self):
            out._data = ["(?:", str(self)[3:-1], "|"]
            if Regex._is_non_capture_group(other_):
                out._data += [str(other_)[3:-1], ")"]
            else:
                out._data += other_._data + [")"]
        elif Regex._is_non_capture_group(other_):
            out._data = ["(?:", str(self), "|", str(other_)[3:-1], ")"]
        else:
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
        if Regex._is_non_capture_group(other_):
            out._data = ["(?:", str(other_)[3:-1], "|"]
            if Regex._is_non_capture_group(self):
                out._data += [str(self)[3:-1], ")"]
            else:
                out._data += self._data + [")"]
        elif Regex._is_non_capture_group(self):
            out._data = ["(?:", str(other_), "|", str(self)[3:-1], ")"]
        else:
            out._data = ["(?:"] + other_._data + ["|"] + self._data + [")"]
        out._capture_groups = []
        return out
