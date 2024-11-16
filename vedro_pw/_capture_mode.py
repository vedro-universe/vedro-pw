from enum import Enum

__all__ = ("CaptureMode",)


class CaptureMode(str, Enum):
    """
    Defines modes for controlling the behavior of capturing screenshots, video, or traces.

    This enumeration includes the following modes:
    - `ALWAYS`: Always capture the artifact.
    - `NEVER`: Never capture the artifact.
    - `ON_RESCHEDULE`: Capture the artifact only when the scenario is rescheduled.
    - `ON_FAILURE`: Capture the artifact only when the scenario or step fails.
    """

    ALWAYS = "always"
    NEVER = "never"
    ON_RESCHEDULE = "on-reschedule"
    ON_FAILURE = "on-failure"

    def __str__(self) -> str:
        """
        Return the string representation of the CaptureMode.

        :return: The string value of the CaptureMode.
        """
        return self.value
