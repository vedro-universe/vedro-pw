from typing import Any, Optional

import vedro
from playwright.async_api import Browser, BrowserType, async_playwright
from vedro import defer

from ._pw_browser import PlaywrightBrowser

__all__ = ("launched_browser",)


@vedro.context
async def launched_browser(browser: Optional[PlaywrightBrowser] = None, **kwargs: Any) -> Browser:
    if browser is None:
        browser = PlaywrightBrowser.FIREFOX

    cm = async_playwright()
    pw = await cm.__aenter__()
    defer(cm.__aexit__)

    options = {**kwargs, "headless": kwargs.get("headless", False)}

    browser_type: BrowserType = getattr(pw, browser.value)
    browser_instance = await browser_type.launch(**options)

    return browser_instance
