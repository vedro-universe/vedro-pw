from pathlib import Path
from random import choice
from typing import Union, cast

from playwright.async_api import BrowserType
from playwright.async_api import Playwright as AsyncPlaywright

from ._pw_browser import PlaywrightBrowser
from .options import DeviceOptions

__all__ = ("get_browser_type", "get_device_options", "show_pw_trace",)


def get_browser_type(playwright: AsyncPlaywright,
                     browser_name: Union[PlaywrightBrowser, str]) -> BrowserType:
    """
    Retrieve the `BrowserType` instance corresponding to the given browser name.

    If `PlaywrightBrowser.RANDOM` is passed, a random browser type is selected
    from the available options (`CHROMIUM`, `FIREFOX`, `WEBKIT`).

    :param playwright: The Playwright instance to retrieve the browser type from.
    :param browser_name: The name of the browser, either as a `PlaywrightBrowser` enum
                         or a string.
    :return: The `BrowserType` instance for the specified browser.
    :raises AttributeError: If the specified browser is not available in the Playwright instance.
    """
    if isinstance(browser_name, PlaywrightBrowser):
        browser_name = browser_name.value

    if browser_name == PlaywrightBrowser.RANDOM:
        browser_name = choice([x.value for x in PlaywrightBrowser
                               if x != PlaywrightBrowser.RANDOM])

    return cast(BrowserType, getattr(playwright, browser_name))


def get_device_options(playwright: AsyncPlaywright,
                       device_name: Union[str, None]) -> Union[DeviceOptions, None]:
    """
    Retrieve the device options for the specified device name.

    Device options define emulation settings such as viewport size, user agent,
    and other device-specific properties. This function ensures the device exists
    in Playwright's supported devices.

    :param playwright: The Playwright instance to retrieve device options from.
    :param device_name: The name of the device to emulate. If None, no device
                        options are returned.
    :return: A `DeviceOptions` dictionary containing the emulation options, or None
             if `device_name` is None.
    :raises ValueError: If the specified device is not supported by Playwright.
    """
    if device_name is None:
        return None

    device_options = playwright.devices.get(device_name)
    if device_options is None:
        raise ValueError(
            f"Device '{device_name}' is not supported or does not exist. "
            "Please refer to the list of supported devices here: "
            "https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json"  # noqa
        )
    return cast(DeviceOptions, device_options)


def show_pw_trace(path: Path) -> None:
    """
    Open the Playwright trace viewer for the specified trace file.

    This function launches a subprocess to open the Playwright trace viewer
    for analyzing the specified trace file. The viewer runs as a separate
    process, and this function does not block execution.

    :param path: The file path to the trace file to be opened.
    """
    import subprocess
    subprocess.Popen(
        args=["playwright", "show-trace", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
