from typing import Any, Optional

import vedro
from playwright.async_api import Browser, BrowserContext
from vedro import defer

from ._configurable_browser import ConfigurableBrowser
from ._launched_browser import launched_browser

__all__ = ("created_browser_context",)


@vedro.context
async def created_browser_context(browser: Optional[Browser] = None,
                                  **kwargs: Any) -> BrowserContext:
    if browser is None:
        browser = await launched_browser()

    options = {**kwargs}
    context = await browser.new_context(**options)

    # ConfigurableBrowser closes the context using defer
    if not isinstance(browser, ConfigurableBrowser):
        defer(context.close)

    return context
