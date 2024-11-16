from typing import Any, Dict, Optional, Union, overload

from playwright.async_api import Browser, BrowserContext, Page
from playwright.async_api import Playwright as AsyncPlaywright
from playwright.async_api import async_playwright
from vedro import defer

from ._configurable_browser import ConfigurableBrowser
from ._pw_browser import PlaywrightBrowser
from ._runtime_config import runtime_config as _runtime_config
from ._unpack import Unpack
from ._utils import get_browser_type, get_device_options
from .options import ConnectOptions, LaunchOptions, NewContextOptions

__all__ = ("launched_browser", "launched_local_browser", "launched_remote_browser",
           "created_browser_context", "opened_browser_page",)


@overload
async def launched_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                           device_name: Optional[str] = None,
                           *,
                           auto_close: bool = True,
                           playwright: Optional[AsyncPlaywright] = None,
                           **kwargs: LaunchOptions) -> ConfigurableBrowser:
    """
    Launch a local browser instance.

    :param browser_name: The name of the browser to launch.
    :param device_name: The name of the device to emulate.
    :param auto_close: Whether to close the browser automatically when the scenario ends.
    :param playwright: An optional Playwright instance to use.
    :param kwargs: Additional launch options for the browser.
    :return: A ConfigurableBrowser instance.
    """
    ...


@overload
async def launched_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                           device_name: Optional[str] = None,
                           *,
                           auto_close: bool = True,
                           playwright: Optional[AsyncPlaywright] = None,
                           **kwargs: ConnectOptions) -> ConfigurableBrowser:
    """
    Connect to a remote browser instance.

    :param browser_name: The name of the browser to connect to.
    :param device_name: The name of the device to emulate.
    :param auto_close: Whether to close the browser automatically when the scenario ends.
    :param playwright: An optional Playwright instance to use.
    :param kwargs: Additional connection options for the browser.
    :return: A ConfigurableBrowser instance.
    """
    ...


async def launched_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                           device_name: Optional[str] = None,
                           *,
                           auto_close: bool = True,
                           playwright: Optional[AsyncPlaywright] = None,
                           **kwargs: Any) -> ConfigurableBrowser:
    """
    Launch or connect to a browser instance based on runtime configuration.

    :param browser_name: The name of the browser to launch or connect to.
    :param device_name: The name of the device to emulate.
    :param auto_close: Whether to close the browser automatically when the scenario ends.
    :param playwright: An optional Playwright instance to use.
    :param kwargs: Additional options for the browser.
    :return: A ConfigurableBrowser instance.
    """
    if _runtime_config.remote:
        return await launched_remote_browser(browser_name, device_name,
                                             auto_close=auto_close,
                                             playwright=playwright,
                                             **kwargs)
    else:
        return await launched_local_browser(browser_name, device_name,
                                            auto_close=auto_close,
                                            playwright=playwright,
                                            **kwargs)


async def launched_local_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                                 device_name: Optional[str] = None,
                                 *,
                                 auto_close: bool = True,
                                 playwright: Optional[AsyncPlaywright] = None,
                                 **kwargs: LaunchOptions) -> ConfigurableBrowser:
    """
    Launch a local browser instance.

    :param browser_name: The name of the browser to launch.
    :param device_name: The name of the device to emulate.
    :param auto_close: Whether to close the browser automatically when the scenario ends.
    :param playwright: An optional Playwright instance to use.
    :param kwargs: Additional launch options for the browser.
    :return: A ConfigurableBrowser instance.
    """
    if playwright is None:
        playwright = await _get_playwright_instance()

    options: Dict[str, Any] = {
        **kwargs,
        "headless": kwargs.get("headless", not _runtime_config.headed),
        "slow_mo": kwargs.get("slow_mo", _runtime_config.slowmo),
    }
    if timeout := kwargs.get("timeout", _runtime_config.browser_timeout):
        options["timeout"] = timeout

    browser_type = get_browser_type(playwright, browser_name or _runtime_config.browser_name)
    browser_instance = await browser_type.launch(**options)
    if auto_close:
        defer(browser_instance.close)

    device_options = get_device_options(playwright, device_name or _runtime_config.device_name)
    return ConfigurableBrowser(browser_instance, device_options=device_options)


async def launched_remote_browser(browser_name: Optional[Union[PlaywrightBrowser, str]] = None,
                                  device_name: Optional[str] = None,
                                  *,
                                  auto_close: bool = True,
                                  playwright: Optional[AsyncPlaywright] = None,
                                  **kwargs: ConnectOptions) -> ConfigurableBrowser:
    """
    Connect to a remote browser instance.

    :param browser_name: The name of the browser to connect to.
    :param device_name: The name of the device to emulate.
    :param auto_close: Whether to close the browser automatically when the scenario ends.
    :param playwright: An optional Playwright instance to use.
    :param kwargs: Additional connection options for the browser.
    :return: A ConfigurableBrowser instance.
    """
    if playwright is None:
        playwright = await _get_playwright_instance(auto_close=auto_close)

    options: Dict[str, Any] = {
        **kwargs,
        "ws_endpoint": kwargs.get("ws_endpoint", _runtime_config.remote_endpoint),
        "slow_mo": kwargs.get("slow_mo", _runtime_config.slowmo),
    }

    browser_type = get_browser_type(playwright, browser_name or _runtime_config.browser_name)
    browser_instance = await browser_type.connect(**options)
    if auto_close:
        defer(browser_instance.close)

    device_options = get_device_options(playwright, device_name or _runtime_config.device_name)
    return ConfigurableBrowser(browser_instance, device_options=device_options)


async def created_browser_context(browser: Optional[Browser] = None,
                                  **kwargs: Unpack[NewContextOptions]) -> BrowserContext:
    """
    Create a new browser context.

    :param browser: An optional Browser instance. If None, a browser is launched.
    :param kwargs: Additional options for creating the browser context.
    :return: A BrowserContext instance.
    """
    if browser is None:
        browser = await launched_browser()

    context = await browser.new_context(**kwargs)

    # ConfigurableBrowser uses `defer(context.close)` to close the context gracefully,
    # ensuring any artifacts (like HAR files or videos) are fully saved and flushed.
    # However, this condition is necessary because users might manually create a browser instance
    # via `.launch()` and pass it to `created_browser_context`. In such cases, if `defer` is not
    # applied, the context might not close properly, leading to unsaved artifacts and potential
    # debugging difficulties due to the time taken to trace missing resources.
    if not isinstance(browser, ConfigurableBrowser):
        defer(context.close)

    return context


async def opened_browser_page(context: Optional[BrowserContext] = None) -> Page:
    """
    Open a new page in the given browser context.

    :param context: An optional BrowserContext instance. If None, a context is created.
    :return: A Page instance representing the new browser page.
    """
    if context is None:
        context = await created_browser_context()

    page = await context.new_page()

    return page


async def _get_playwright_instance(*, auto_close: bool = True) -> AsyncPlaywright:
    """
    Get a Playwright instance.

    :param auto_close: Whether to automatically close the Playwright instance when
                       the scenario ends.
    :return: An AsyncPlaywright instance.
    """
    playwright_manager = async_playwright()
    playwright = await playwright_manager.start()
    if auto_close:
        defer(playwright_manager.__aexit__)
    return playwright
