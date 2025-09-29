from playwright.async_api import BrowserContext
from vedro import scenario, then, when

from vedro_pw import created_browser_context


@scenario("create browser context")
async def _():
    with when:
        context = await created_browser_context()

    with then:
        assert isinstance(context, BrowserContext)
