from playwright.async_api import Browser
from vedro import params, scenario, then, when

from vedro_pw import launched_browser as launched_local_by_default
from vedro_pw import launched_local_browser
from vedro_pw._configurable_browser import ConfigurableBrowser


@scenario("launch browser", [
    params(launched_local_by_default),
    params(launched_local_browser),
])
async def _(launched_browser):
    with when:
        browser = await launched_browser()

    with then:
        assert isinstance(browser, Browser)
        assert isinstance(browser, ConfigurableBrowser)
