import pytest

from iregex import Regex
from iregex.consts import (
    ALPHA,
    ANY,
    NUMERIC,
    ONE_OR_MORE,
    OPTIONAL,
    WHITESPACE,
    ZERO_OR_MORE,
)
from iregex.exceptions import NonEmptyError, SetIntersectionError


def test_regex_literal() -> None:
    """Test basic literal addition."""
    regex = Regex(NUMERIC).literal(ALPHA)
    assert str(regex) == NUMERIC + ALPHA


def test_whitespace() -> None:
    """Test basic whitespace addition."""
    regex = Regex(NUMERIC).whitespace()
    assert str(regex) == NUMERIC + WHITESPACE + ZERO_OR_MORE


def test_zero_or_more_repetitions() -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).zero_or_more_repetitions()
    assert str(regex) == f"(?:{NUMERIC})" + ZERO_OR_MORE


def test_one_or_more_repetitions() -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).one_or_more_repetitions()
    assert str(regex) == f"(?:{NUMERIC})" + ONE_OR_MORE


def test_m_to_n_repetitions() -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).m_to_n_repetitions(3, 5)
    assert str(regex) == f"(?:{NUMERIC})" + r"{3,5}"


def test_exactly_m_repetitions() -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).exactly_m_repetitions(3)
    assert str(regex) == f"(?:{NUMERIC})" + r"{3}"


def test_m_or_more_repetitions() -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).m_or_more_repetitions(3)
    assert str(regex) == f"(?:{NUMERIC})" + r"{2}" + f"(?:{NUMERIC})" + ONE_OR_MORE


def test_optional() -> None:
    """Test basic optional."""
    regex = Regex(NUMERIC).optional()
    assert str(regex) == f"(?:{NUMERIC})" + OPTIONAL


def test_any_char1() -> None:
    """Test basic any_char."""
    regex = Regex(NUMERIC).any_char("asdf")
    assert str(regex) == f"{NUMERIC}[asdf]"


def test_any_char2() -> None:
    """Test basic any_char."""
    regex = Regex(NUMERIC).any_char("a", "s", "d", "f")
    assert str(regex) == f"{NUMERIC}[asdf]"


def test_exclude_char1() -> None:
    """Test basic exclude_char."""
    regex = Regex(NUMERIC).exclude_char("asdf")
    assert str(regex) == f"{NUMERIC}[^asdf]"


def test_exclude_char2() -> None:
    """Test basic exclude_char."""
    regex = Regex(NUMERIC).exclude_char("a", "s", "d", "f")
    assert str(regex) == f"{NUMERIC}[^asdf]"


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
    "self,other,result", [(Regex(NUMERIC), Regex(NUMERIC), f"(?:{NUMERIC}|{NUMERIC})")],
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
