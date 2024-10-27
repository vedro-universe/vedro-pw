from enum import Enum

__all__ = ("PlaywrightBrowser",)


class PlaywrightBrowser(str, Enum):
    FIREFOX = "firefox"
    CHROMIUM = "chromium"
    WEBKIT = "webkit"

    def __str__(self) -> str:
        return self.value
