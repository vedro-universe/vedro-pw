from typing import Union, cast

from playwright.async_api import BrowserType
from playwright.async_api import Playwright as AsyncPlaywright

from ._pw_browser import PlaywrightBrowser

__all__ = ("get_browser_type",)


def get_browser_type(playwright: AsyncPlaywright,
                     browser_name: Union[PlaywrightBrowser, str]) -> BrowserType:
    return cast(BrowserType, getattr(
        playwright,
        browser_name.value if isinstance(browser_name, PlaywrightBrowser) else browser_name
    ))
