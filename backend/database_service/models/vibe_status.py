from enum import IntEnum


class VibeStatus(IntEnum):
    """Lifecycle stage of a vibe task. Values align with the proto enum."""

    UNSPECIFIED = 0
    PENDING = 1
    IN_PROGRESS = 2
    GROOVY = 3
