from enum import Enum

__all__ = ("PlaywrightBrowser",)


class PlaywrightBrowser(Enum):
    FIREFOX = "firefox"
    CHROMIUM = "chromium"
    WEBKIT = "webkit"
