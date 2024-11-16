from random import choice
from typing import Union, cast

from playwright.async_api import BrowserType
from playwright.async_api import Playwright as AsyncPlaywright

from ._pw_browser import PlaywrightBrowser
from .options import DeviceOptions

__all__ = ("get_browser_type", "get_device_options",)


def get_browser_type(playwright: AsyncPlaywright,
                     browser_name: Union[PlaywrightBrowser, str]) -> BrowserType:
    if isinstance(browser_name, PlaywrightBrowser):
        browser_name = browser_name.value

    if browser_name == PlaywrightBrowser.RANDOM:
        browser_name = choice([x.value for x in PlaywrightBrowser
                               if x != PlaywrightBrowser.RANDOM])

    return cast(BrowserType, getattr(playwright, browser_name))


def get_device_options(playwright: AsyncPlaywright,
                       device_name: Union[str, None]) -> Union[DeviceOptions, None]:
    if device_name is None:
        return None

    device_options = playwright.devices.get(device_name)
    if device_options is None:
        raise ValueError(f"Device '{device_name}' is not supported or does not exist")
    return cast(DeviceOptions, device_options)
