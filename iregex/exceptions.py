"""
Custom exceptions used in this library.
"""


class SetIntersectionError(Exception):
    """Happens when the intersection of two sets is non-empty."""

    pass


class NonEmptyError(Exception):
    """Happens when something that is supposed to be empty is not."""

    pass


class NotACharacterException(Exception):
    """Happens when something that should have been a character is not a character."""

    pass


class AlreadyRepeatingException(Exception):
    """Happens when a repeating character is already at the end of the regex."""

    pass


class AlreadyCapturedException(Exception):
    """Happens when a capture group already exists and can't be replaced."""

    pass
