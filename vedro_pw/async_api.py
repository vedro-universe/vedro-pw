from typing import Any, Optional, Union, cast

import vedro
from playwright.async_api import Browser, BrowserContext, Page
from playwright.async_api import Playwright as AsyncPlaywright
from playwright.async_api import async_playwright
from vedro import defer

from ._configurable_browser import ConfigurableBrowser
from ._pw_browser import PlaywrightBrowser
from ._runtime_config import runtime_config as _runtime_config
from ._types import ConnectOptions, LaunchOptions
from ._utils import get_browser_type, get_device_options

__all__ = ("launched_browser", "launched_local_browser", "launched_remote_browser",
           "created_browser_context", "opened_browser_page",)


@vedro.context
async def launched_local_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                                 device_name: Optional[str] = None,
                                 *,
                                 auto_close: bool = True,
                                 playwright: Optional[AsyncPlaywright] = None,
                                 launch_options: Optional[LaunchOptions] = None
                                 ) -> ConfigurableBrowser:
    if playwright is None:
        playwright = await _get_playwright_instance()

    if launch_options is None:
        launch_options = {}

    options: LaunchOptions = {
        **launch_options,
        "headless": launch_options.get("headless", not _runtime_config.headed),
        "slow_mo": launch_options.get("slow_mo", _runtime_config.slowmo),
    }
    if timeout := launch_options.get("timeout", _runtime_config.browser_timeout):
        options["timeout"] = timeout

    browser_type = get_browser_type(playwright, browser_name or _runtime_config.browser_name)
    browser_instance = await browser_type.launch(**options)
    if auto_close:
        defer(browser_instance.close)

    device_options = get_device_options(playwright, device_name or _runtime_config.device_name)
    return ConfigurableBrowser(browser_instance, device_options=device_options)


@vedro.context
async def launched_remote_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                                  device_name: Optional[str] = None,
                                  *,
                                  auto_close: bool = True,
                                  playwright: Optional[AsyncPlaywright] = None,
                                  connect_options: Optional[ConnectOptions] = None
                                  ) -> ConfigurableBrowser:
    if playwright is None:
        playwright = await _get_playwright_instance(auto_close=auto_close)

    if connect_options is None:
        connect_options = {}

    options: ConnectOptions = {
        **connect_options,
        "ws_endpoint": connect_options.get("ws_endpoint", _runtime_config.remote_endpoint),
        "slow_mo": connect_options.get("slow_mo", _runtime_config.slowmo),
    }

    browser_type = get_browser_type(playwright, browser_name or _runtime_config.browser_name)
    browser_instance = await browser_type.connect(**options)
    if auto_close:
        defer(browser_instance.close)

    device_options = get_device_options(playwright, device_name or _runtime_config.device_name)
    return ConfigurableBrowser(browser_instance, device_options=device_options)


@vedro.context
async def launched_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                           device_name: Optional[str] = None,
                           *,
                           auto_close: bool = True,
                           playwright: Optional[AsyncPlaywright] = None,
                           options: Optional[Union[LaunchOptions, ConnectOptions]] = None,
                           ) -> ConfigurableBrowser:
    if _runtime_config.remote:
        return await launched_remote_browser(browser_name, device_name,
                                             auto_close=auto_close,
                                             playwright=playwright,
                                             connect_options=cast(ConnectOptions, options))
    else:
        return await launched_local_browser(browser_name, device_name,
                                            auto_close=auto_close,
                                            playwright=playwright,
                                            launch_options=cast(LaunchOptions, options))


@vedro.context
async def created_browser_context(browser: Optional[Browser] = None,
                                  **kwargs: Any) -> BrowserContext:
    if browser is None:
        browser = await launched_browser()

    options = {**kwargs}
    context = await browser.new_context(**options)

    # ConfigurableBrowser uses `defer(context.close)` to close the context gracefully,
    # ensuring any artifacts (like HAR files or videos) are fully saved and flushed.
    # However, this condition is necessary because users might manually create a browser instance
    # via `.launch()` and pass it to `created_browser_context`. In such cases, if `defer` is not
    # applied, the context might not close properly, leading to unsaved artifacts and potential
    # debugging difficulties due to the time taken to trace missing resources.
    if not isinstance(browser, ConfigurableBrowser):
        defer(context.close)

    return context


@vedro.context
async def opened_browser_page(context: Optional[BrowserContext] = None) -> Page:
    if context is None:
        context = await created_browser_context()

    page = await context.new_page()

    return page


async def _get_playwright_instance(*, auto_close: bool = True) -> AsyncPlaywright:
    playwright_manager = async_playwright()
    playwright = await playwright_manager.start()
    if auto_close:
        defer(playwright_manager.__aexit__)
    return playwright
