from enum import Enum

__all__ = ("CaptureMode",)


class CaptureMode(str, Enum):
    ALWAYS = "always"
    NEVER = "never"
    ON_RESCHEDULE = "on-reschedule"
    ON_FAILURE = "on-failure"

    def __str__(self) -> str:
        return self.value
