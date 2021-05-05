from typing import List, Optional, Union, Dict
from copy import copy

from py_idiomatic_regex.consts import *


class Regex:
    """A wrapper for regex strings that hides the implementation."""
    # Private Variables
    _data: List[str]
    _capture_groups: List[str]

    def __init__(self, regex_str: Optional[str] = None) -> None:
        self._data = [regex_str] if regex_str else []
        self._capture_groups = []

    # ============== Chained Methods ==============
    def literal(self, regex: Union[str, "Regex"]) -> "Regex":
        """Adds a literal to the end of the regex."""
        out = copy(self)
        if isinstance(regex, Regex):
            out._data += regex._data
        elif isinstance(regex, str):
            out._data.append(regex)
        else:
            raise TypeError(f"Type not supported: {type(regex)}")
        return out

    def whitespace(self) -> "Regex":
        """Allows unlimited whitespace."""
        out = copy(self)
        out._data.append(WHITESPACE+ZERO_OR_MORE)
        return out

    def zero_or_more_repititions(self) -> "Regex":
        """Repeats the previous regex zero or more times."""
        out = copy(self)
        out._data.append(ZERO_OR_MORE)
        return out

    def one_or_more_repititions(self) -> "Regex":
        """Repeats the previous regex one or more times."""
        out = copy(self)
        out._data.append(ONE_OR_MORE)
        return out

    def m_to_n_repititions(self, m: int, n: int) -> "Regex":
        """Repeats the previous regex m to n inclusive times."""
        out = self.make_capture_group()
        out._data.append("{"+str(m)+","+str(n)+"}")
        return out

    def exactly_m_repititions(self, m: int) -> "Regex":
        """Repeats the previous regex exactly m times."""
        out = self.make_capture_group()
        out._data.append("{"+str(m)+"}")
        return out

    def m_or_more_repititions(self, m: int) -> "Regex":
        """Repeats the previous regex m or more times."""
        if m == 0:
            return self.zero_or_more_repititions()
        elif m == 1:
            return self.one_or_more_repititions()
        elif m < 0:
            raise ValueError(f"m must be >= 0, got {m}")
        return self.exactly_m_repititions(m-1) + self.one_or_more_repititions()

    def optional(self) -> "Regex":
        """The previous regex can exist 0 or 1 times."""
        out = self.make_capture_group()
        out._data.append('?')
        return out

    def any_char(self, *text: str) -> "Regex":
        """Any char in the text may be used."""
        out = copy(self)
        out._data = ['['] + list(text) + [']']
        return out

    def exclude_char(self, *text: str) -> "Regex":
        """None of the chars in the text may be used."""
        out = copy(self)
        out._data = ['[^'] + list(text) + [']']
        return out

    def make_capture_group(self) -> "Regex":
        """Creates an anonymous capture group."""
        out = copy(self)
        out._data = ['('] + out._data + [')']
        out._capture_groups.append('')
        return out

    def make_named_capture_group(self, name: str) -> "Regex":
        """Makes the previous regex a capture group of name `name`."""
        out = copy(self)
        out._data = ['(?<'+name+'>'] + out._data + [')']
        out._capture_groups.append(name)
        return out

    def anything(self) -> "Regex":
        return self.literal(".*")

    # ============== Result Methods =============
    def find_all(self, text: str) -> List[Union[slice, Dict[str, slice]]]:
        raise NotImplementedError()

    # ============== Magic Methods ==============
    def __copy__(self) -> "Regex":
        out = Regex()
        out._data = copy(self._data)
        return out

    def __str__(self) -> str:
        return ''.join(self._data)

    def __repr__(self) -> str:
        return 'Regex('+str(self)+')'

    def __add__(self, other: "Regex") -> "Regex":
        out = Regex()
        out._data = self._data + other._data
        return out

    def __or__(self, other: "Regex") -> "Regex":
        out = Regex()
        out._data = ["("] + self._data + ["|"] + other._data + [")"]
        return out