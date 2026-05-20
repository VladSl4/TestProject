from enum import IntEnum


class LogCategory(IntEnum):
    """Severity bucket assigned by the analyzer. Values match the proto enum."""

    UNSPECIFIED = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
