"""
Tests Regex class by testing the regex match results on given strings.
"""

import pytest

from iregex import Regex
from iregex.consts import ALPHA, NUMERIC


@pytest.mark.parametrize("text,expected", [("1a", True), ("1", False)])
def test_regex_literal_results(text: str, expected: bool) -> None:
    """Test basic literal addition."""
    regex = Regex(NUMERIC).literal(ALPHA).compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)


@pytest.mark.parametrize(
    "text,expected", [("1", True), ("1 ", True), ("1  ", True), (" 1 ", False)]
)
def test_whitespace_results(text: str, expected: bool) -> None:
    """Test basic whitespace addition."""
    regex = Regex(NUMERIC).whitespace().compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)


@pytest.mark.parametrize(
    "text,expected", [("1\n", True), ("1\n\r", True), ("1\r", True)]
)
def test_newline_results(text: str, expected: bool) -> None:
    """Test basic newline addition."""
    regex = Regex(NUMERIC).newlines().compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)


@pytest.mark.parametrize(
    "text,expected", [("", True), ("1", True), ("12", True), ("1a", False)]
)
def test_zero_or_more_repetitions_results(text: str, expected: bool) -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).zero_or_more_repetitions().compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", False),
        ("1", True),
        ("12", True),
        ("123", True),
        ("12345", True),
        ("123456", True),
        ("1a", False),
    ],
)
def test_one_or_more_repetitions_results(text: str, expected: bool) -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).one_or_more_repetitions().compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)


@pytest.mark.parametrize(
    "text,expected,m,n",
    [
        ("", False, 3, 5),
        ("1", False, 3, 5),
        ("12", False, 3, 5),
        ("123", True, 3, 5),
        ("12345", True, 3, 5),
        ("123456", False, 3, 5),
        ("1a", False, 3, 5),
    ],
)
def test_m_to_n_repetitions_results(text: str, expected: bool, m: int, n: int) -> None:
    """Test basic repetitions."""
    assert m < n
    regex = Regex(NUMERIC).m_to_n_repetitions(m, n).compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)


@pytest.mark.parametrize(
    "text,expected,m",
    [
        ("", False, 3),
        ("1", False, 3),
        ("12", False, 3),
        ("123", True, 3),
        ("12345", False, 3),
        ("123456", False, 3),
        ("1a", False, 3),
    ],
)
def test_exactly_m_repetitions_results(text: str, expected: bool, m: int) -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).exactly_m_repetitions(m).compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)


@pytest.mark.parametrize(
    "text,expected,m",
    [
        ("", False, 3),
        ("1", False, 3),
        ("12", False, 3),
        ("123", True, 3),
        ("12345", True, 3),
        ("123456", True, 3),
        ("1a", False, 3),
    ],
)
def test_m_or_more_repetitions_results(text: str, expected: bool, m: int) -> None:
    """Test basic repetitions."""
    regex = Regex(NUMERIC).m_or_more_repetitions(m).compile()
    if expected:
        assert regex.fullmatch(text)
    else:
        assert not regex.fullmatch(text)
