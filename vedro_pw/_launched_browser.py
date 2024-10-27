from typing import Any, Optional

import vedro
from playwright.async_api import Browser, BrowserType, async_playwright
from vedro import defer

from ._pw_browser import PlaywrightBrowser
from ._runtime_config import runtime_config as _runtime_config

__all__ = ("launched_browser",)


@vedro.context
async def launched_browser(browser: Optional[PlaywrightBrowser] = None, **kwargs: Any) -> Browser:
    browser_name = browser.value if browser else _runtime_config.get_browser().value
    options = {
        **kwargs,
        "headless": kwargs.get("headless", not _runtime_config.is_headed()),
        "slow_mo": kwargs.get("slow_mo", _runtime_config.get_slowmo()),
    }

    cm = async_playwright()
    pw = await cm.__aenter__()
    defer(cm.__aexit__)

    browser_type: BrowserType = getattr(pw, browser_name)
    browser_instance = await browser_type.launch(**options)

    return browser_instance
