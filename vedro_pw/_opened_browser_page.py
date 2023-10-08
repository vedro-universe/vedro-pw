from typing import Optional

import vedro
from playwright.async_api import BrowserContext, Page

from ._created_browser_context import created_browser_context

__all__ = ("opened_browser_page",)


@vedro.context
async def opened_browser_page(context: Optional[BrowserContext] = None) -> Page:
    if context is None:
        context = await created_browser_context()

    page = await context.new_page()

    return page
