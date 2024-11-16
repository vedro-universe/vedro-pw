from typing import TypedDict

from playwright.async_api import ViewportSize

__all__ = ("DeviceOptions",)


class DeviceOptions(TypedDict, total=False):
    """
    Represents device options for configuring browser contexts.

    This TypedDict provides a structured way to define emulation options
    such as viewport, user agent, and device-specific characteristics
    (e.g., mobile settings and touch support).
    """
    viewport: ViewportSize
    """
    The viewport dimensions of the device. Specifies the width and height
    for rendering web pages.
    """

    user_agent: str
    """
    The user agent string to use for emulation. This string identifies
    the browser and device type during requests.
    """

    is_mobile: bool
    """
    Whether to emulate mobile device behavior, including considering
    the meta viewport tag. Defaults to `False`.
    """

    has_touch: bool
    """
    Indicates if the device supports touch input. Defaults to `False`.
    """

    device_scale_factor: float
    """
    The device scale factor (DPR - Device Pixel Ratio). This controls the
    density of pixels emulated for the device. Defaults to `1.0`.
    """

    default_browser_type: str
    """
    The default browser type to use in the context. Can be `chromium`,
    `firefox`, or `webkit`.
    """
