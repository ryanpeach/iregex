"""
Tests Regex class by testing output string representation.
"""

from typing import Callable

import pytest

from iregex import Regex
from iregex.consts import (
    ALPHA,
    ANY,
    NEWLINE,
    NUMERIC,
    ONE_OR_MORE,
    WHITESPACE,
    ZERO_OR_MORE,
)
from iregex.exceptions import (
    NonEmptyError,
    NotACharacterException,
    SetIntersectionError,
)


def test_regex_literal() -> None:
    """Test basic literal addition."""
    regex = Regex(NUMERIC).literal(ALPHA)
    assert str(regex) == NUMERIC + ALPHA


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).whitespace(), NUMERIC + WHITESPACE + ZERO_OR_MORE),
        (
            Regex(NUMERIC + ALPHA).whitespace(),
            NUMERIC + ALPHA + WHITESPACE + ZERO_OR_MORE,
        ),
    ],
)
def test_whitespace(regex: Regex, result: str) -> None:
    """Test basic whitespace addition."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).newlines(), NUMERIC + NEWLINE + ZERO_OR_MORE),
        (Regex(NUMERIC + ALPHA).newlines(), NUMERIC + ALPHA + NEWLINE + ZERO_OR_MORE),
    ],
)
def test_newline(regex: Regex, result: str) -> None:
    """Test basic newline addition."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).zero_or_more_repetitions(), f"{NUMERIC}" + ZERO_OR_MORE),
        (
            Regex(NUMERIC + ALPHA).zero_or_more_repetitions(),
            f"(?:{NUMERIC+ALPHA})" + ZERO_OR_MORE,
        ),
    ],
)
def test_zero_or_more_repetitions(regex: Regex, result: str) -> None:
    """Test basic repetitions."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).one_or_more_repetitions(), f"{NUMERIC}" + ONE_OR_MORE),
        (
            Regex(NUMERIC + ALPHA).one_or_more_repetitions(),
            f"(?:{NUMERIC+ALPHA})" + ONE_OR_MORE,
        ),
    ],
)
def test_one_or_more_repetitions(regex: Regex, result: str) -> None:
    """Test basic repetitions."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).m_to_n_repetitions(3, 5), f"{NUMERIC}" + "{3,5}"),
        (
            Regex(NUMERIC + ALPHA).m_to_n_repetitions(3, 5),
            f"(?:{NUMERIC+ALPHA})" + "{3,5}",
        ),
    ],
)
def test_m_to_n_repetitions(regex: Regex, result: str) -> None:
    """Test basic repetitions."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).exactly_m_repetitions(3), f"{NUMERIC}" + "{3}"),
        (
            Regex(NUMERIC + ALPHA).exactly_m_repetitions(3),
            f"(?:{NUMERIC+ALPHA})" + "{3}",
        ),
    ],
)
def test_exactly_m_repetitions(regex: Regex, result: str) -> None:
    """Test basic repetitions."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).m_or_more_repetitions(3), f"{NUMERIC}" + "{3,}"),
        (
            Regex(NUMERIC + ALPHA).m_or_more_repetitions(3),
            f"(?:{NUMERIC+ALPHA})" + "{3,}",
        ),
    ],
)
def test_m_or_more_repetitions(regex: Regex, result: str) -> None:
    """Test basic repetitions."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [
        (Regex(NUMERIC).optional(), f"{NUMERIC}?"),
        (Regex(NUMERIC + ALPHA).optional(), f"(?:{NUMERIC+ALPHA})?"),
    ],
)
def test_optional(regex: Regex, result: str) -> None:
    """Test basic optional."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex,result",
    [(Regex().any_char("a"), f"a"), (Regex().any_char("a", "b"), f"[ab]"),],
)
def test_any_char(regex: Regex, result: str) -> None:
    """Test basic any_char."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex_lazy",
    [lambda: Regex().any_char("ab"), lambda: Regex().any_char("a", "bc"),],
)
def test_any_char_error(regex_lazy: Callable) -> None:
    """Test basic any_char."""
    with pytest.raises(NotACharacterException):
        regex_lazy()


@pytest.mark.parametrize(
    "regex,result",
    [(Regex().exclude_char("a"), f"[^a]"), (Regex().exclude_char("a", "b"), f"[^ab]"),],
)
def test_exclude_char(regex: Regex, result: str) -> None:
    """Test basic exclude_char."""
    assert str(regex) == result


@pytest.mark.parametrize(
    "regex_lazy",
    [lambda: Regex().exclude_char("ab"), lambda: Regex().exclude_char("a", "bc"),],
)
def test_exclude_char_error(regex_lazy: Callable) -> None:
    """Test basic exclude_char."""
    with pytest.raises(NotACharacterException):
        regex_lazy()


def test_anything() -> None:
    """Test basic anything."""
    regex = Regex(NUMERIC).anything()
    assert str(regex) == NUMERIC + ANY + ZERO_OR_MORE


def test_capture_group1() -> None:
    """Basic test capture group."""
    regex = Regex(NUMERIC + ALPHA).make_capture_group().literal(ZERO_OR_MORE)
    assert str(regex) == f"({NUMERIC+ALPHA}){ZERO_OR_MORE}"


def test_non_capture_group1() -> None:
    """Basic test capture group."""
    regex = Regex(NUMERIC + ALPHA).make_non_capture_group().literal(ZERO_OR_MORE)
    assert str(regex) == f"(?:{NUMERIC+ALPHA}){ZERO_OR_MORE}"


def test_named_capture_group1() -> None:
    """Basic test named capture group."""
    regex = (
        Regex(NUMERIC + ALPHA).make_named_capture_group("name").literal(ZERO_OR_MORE)
    )
    assert str(regex) == f"(?<name>{NUMERIC+ALPHA}){ZERO_OR_MORE}"


def test_make_lookahead() -> None:
    """Test basic lookahead."""
    regex = Regex(ALPHA).literal(Regex(NUMERIC).make_lookahead())
    assert str(regex) == ALPHA + f"(?={NUMERIC})"


def test_make_negative_lookahead() -> None:
    """Test negative lookahead."""
    regex = Regex(ALPHA).literal(Regex(NUMERIC).make_negative_lookahead())
    assert str(regex) == ALPHA + f"(?!{NUMERIC})"


def test_make_lookbehind() -> None:
    """Test basic lookbehind."""
    regex = Regex(NUMERIC).make_lookbehind().literal(ALPHA)
    assert str(regex) == f"(?<={NUMERIC})" + ALPHA


def test_make_negative_lookbehind() -> None:
    """Test negative lookbehind."""
    regex = Regex(NUMERIC).make_negative_lookbehind().literal(ALPHA)
    assert str(regex) == f"(?<!{NUMERIC})" + ALPHA


@pytest.mark.parametrize(
    "self,other,result",
    [
        (Regex(NUMERIC), Regex(NUMERIC), Regex(NUMERIC).literal(NUMERIC)),
        (Regex(NUMERIC), NUMERIC, Regex(NUMERIC).literal(NUMERIC)),
        (NUMERIC, Regex(NUMERIC), Regex(NUMERIC).literal(NUMERIC)),
        (
            Regex(NUMERIC).make_named_capture_group("name1"),
            Regex(ALPHA).make_named_capture_group("name2"),
            Regex(f"(?<name1>{NUMERIC})(?<name2>{ALPHA})"),
        ),
    ],
)
def test_add(self: Regex, other: Regex, result: Regex) -> None:
    """Tests lots of adds."""
    assert self + other == result


@pytest.mark.parametrize(
    "self,other",
    [
        (
            Regex(NUMERIC).make_named_capture_group("name"),
            Regex(ALPHA).make_named_capture_group("name"),
        )
    ],
)
def test_add_set_intersection_error(self: Regex, other: Regex) -> None:
    """Tests that an add error pops up in certain scenarios."""
    with pytest.raises(SetIntersectionError):
        self + other


@pytest.mark.parametrize(
    "self,other,result",
    [
        (Regex(NUMERIC), Regex(ALPHA), f"(?:{NUMERIC}|{ALPHA})"),
        (Regex(NUMERIC), ALPHA, f"(?:{NUMERIC}|{ALPHA})"),
        (NUMERIC, Regex(ALPHA), f"(?:{NUMERIC}|{ALPHA})"),
        (
            Regex(fr"(?:{NUMERIC}|{ALPHA})"),
            Regex(WHITESPACE),
            f"(?:{NUMERIC}|{ALPHA}|{WHITESPACE})",
        ),
        (
            Regex(WHITESPACE),
            Regex(fr"(?:{NUMERIC}|{ALPHA})"),
            f"(?:{WHITESPACE}|{NUMERIC}|{ALPHA})",
        ),
    ],
)
def test_or(self: Regex, other: Regex, result: Regex) -> None:
    """Tests basic or."""
    assert str(self | other) == str(result)


@pytest.mark.parametrize(
    "self,other",
    [
        (
            Regex(NUMERIC).make_named_capture_group("name1"),
            Regex(ALPHA).make_named_capture_group("name2"),
        )
    ],
)
def test_or_non_empty_error(self: Regex, other: Regex) -> None:
    """Tests that an or error pops up in certain scenarios."""
    with pytest.raises(NonEmptyError):
        self | other
