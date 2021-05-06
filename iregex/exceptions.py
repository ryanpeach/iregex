class SetIntersectionError(Exception):
    """Happens when the intersection of two sets is non-empty."""

    pass


class NonEmptyError(Exception):
    """Happens when something that is supposed to be empty is not."""

    pass
