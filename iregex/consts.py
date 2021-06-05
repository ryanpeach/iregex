"""
Convenient constants for use in Regex.
"""

from iregex.regex import Regex

#: Any whitespace character
WHITESPACE = Regex(r"\s")

#: Any non-whitespace character
NON_WHITESPACE = Regex(r"\S")

#: Any lowercase character a-z
LOWERCASE = Regex(r"[a-z]")

#: Any uppercase character A-Z
UPPERCASE = Regex(r"[A-Z]")

#: Any lower or uppercase character a-z A-Z
ALPHA = Regex(r"[a-zA-Z]")

#: Any numeric character 0-9
NUMERIC = Regex(r"\d")

#: Any non-numeric character
NON_NUMERIC = Regex(r"\D")

#: Any alphanumeric character a-z or 0-9
ALPHA_NUMERIC = Regex(r"\w")

#: Any non-alphanumeric character
NON_ALPHANUMERIC = Regex(r"\W")

#: Any character at all
ANY_CHAR = Regex(r".")

#: Any number of any character at all
ANYTHING = Regex(r".*")

#: The literal period
PERIOD = Regex(r"\.")

#: The start of a line
START_OF_LINE = Regex(r"^")

#: The end of a line
END_OF_LINE = Regex(r"$")

#: One or more of the last character or group
ONE_OR_MORE = Regex(r"+")

#: Zero or more of the last character or group
ZERO_OR_MORE = Regex(r"*")

#: Zero or one of the last character or group
OPTIONAL = Regex(r"?")

#: Literal Plus
PLUS = Regex(r"\+")

#: Literal ASTERISK
ASTERISK = r"\*"

#: Literal Dollar Sign
DOLLAR = r"\$"

#: Literal Question Mark
QUESTION_MARK = r"\?"

#: Indicates a newline, use in `re.MULTILINE` mode.
#: Supports all operating systems
NEWLINE = r"(?:\n|\r\n?)"
