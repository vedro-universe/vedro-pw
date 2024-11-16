from enum import Enum

__all__ = ("PlaywrightBrowser",)


class PlaywrightBrowser(str, Enum):
    """
    Defines the supported browser types for Playwright.

    This enumeration includes the following browser types:
    - `FIREFOX`: Use the Mozilla Firefox browser.
    - `CHROMIUM`: Use the Chromium browser.
    - `WEBKIT`: Use the WebKit browser.

    Additionally, it supports:
    - `RANDOM`: Randomly select a browser type.

    These values can be used to specify the browser to be launched or connected to.
    """

    FIREFOX = "firefox"
    CHROMIUM = "chromium"
    WEBKIT = "webkit"
    RANDOM = "random"

    def __str__(self) -> str:
        """
        Return the string representation of the PlaywrightBrowser.

        :return: The string value of the browser type.
        """
        return self.value
