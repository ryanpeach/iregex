"""
Convenient constants for use in Regex.
"""

#: Any whitespace character
WHITESPACE = r"\s"

#: Any non-whitespace character
NON_WHITESPACE = r"\S"

#: Any lowercase character a-z
LOWERCASE = r"[a-z]"

#: Any uppercase character A-Z
UPPERCASE = r"[A-Z]"

#: Any lower or uppercase character a-z A-Z
ALPHA = r"[a-zA-Z]"

#: Any numeric character 0-9
NUMERIC = r"\d"

#: Any non-numeric character
NON_NUMERIC = r"\D"

#: Any alphanumeric character a-z or 0-9
ALPHA_NUMERIC = r"\w"

#: Any non-alphanumeric character
NON_ALPHANUMERIC = r"\W"

#: Any character at all
ANY = r"."

#: The literal period
PERIOD = r"\."

#: The start of a line
START_OF_LINE = r"^"

#: The end of a line
END_OF_LINE = r"$"

#: One or more of the last character or group
ONE_OR_MORE = r"+"

#: Zero or more of the last character or group
ZERO_OR_MORE = r"*"

#: Zero or one of the last character or group
OPTIONAL = r"?"

#: Literal Plus
PLUS = r"\+"

#: Literal ASTERISK
ASTERISK = r"\*"

#: Literal Dollar Sign
DOLLAR = r"\$"

#: Literal Question Mark
QUESTION_MARK = r"\?"

#: Indicates a newline, use in `re.MULTILINE` mode.
#: Supports all operating systems
NEWLINE = r"(?:\n|\r\n?)"
