from pathlib import Path
from typing import Literal, Sequence, TypedDict, Union

from playwright.async_api import FloatRect, Locator, ViewportSize

__all__ = ("DeviceOptions", "TraceOptions", "VideoOptions", "ScreenshotOptions",)


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


class TraceOptions(TypedDict, total=False):
    """
    Represents the configuration options for saving a trace during tracing.

    This TypedDict defines optional parameters to customize trace capturing and saving,
    such as file paths, trace names, and included data (e.g., snapshots, screenshots).
    """

    path: Union[Path, str]
    """
    The file path where the final trace zip file will be saved. Used in `tracing.stop()`.
    """

    name: str
    """
    The prefix for intermediate trace files, stored in the `tracesDir` directory
    specified in `browser_type.launch()`.
    """

    title: str
    """
    The title of the trace to be displayed in the Trace Viewer.
    """

    screenshots: bool
    """
    Indicates whether to capture screenshots during tracing to build a timeline preview.
    Defaults to `False`.
    """

    snapshots: bool
    """
    Indicates whether to capture DOM snapshots and record network activity during tracing.
    Defaults to `False`.
    """

    sources: bool
    """
    Indicates whether to include source files for trace actions in the trace output.
    Defaults to `False`.
    """


class VideoOptions(TypedDict, total=False):
    """
    Represents the configuration options for video recording in a browser context.

    This TypedDict defines optional parameters to enable and customize video
    recording, such as the output directory and the dimensions of the recorded videos.
    """

    record_video_dir: Union[Path, str]
    """
    The directory where recorded videos for all pages in the browser context will be saved.
    If not specified, videos will not be recorded. Make sure to call
    `browser_context.close()` to ensure that videos are saved properly.
    """

    record_video_size: ViewportSize
    """
    The dimensions of the recorded videos, defined by width and height.

    - If not specified, the size defaults to the `viewport` dimensions scaled down to fit 800x800.
    - If `viewport` is not explicitly configured, the video size defaults to 800x450.
    - Each page's video will be scaled down as necessary to fit the specified size.
    """


class ScreenshotOptions(TypedDict, total=False):
    """
    Represents the configuration options for taking a screenshot of a page.

    This TypedDict defines optional parameters to control the screenshot
    capture process, such as file path, format, quality, and additional
    visual settings like animations, masking, and styles.
    """

    timeout: float
    """
    Maximum time in milliseconds to wait for the screenshot to be taken.
    Defaults to `30000` (30 seconds). Pass `0` to disable the timeout.
    """

    type: Literal["jpeg", "png"]
    """
    The image format for the screenshot. Can be either `"jpeg"` or `"png"`.
    Defaults to `"png"`.
    """

    path: Union[str, Path]
    """
    The file path where the screenshot will be saved. The image format is
    inferred from the file extension. If no path is specified, the screenshot
    is not saved to disk.
    """

    quality: int
    """
    The quality of the image, specified as an integer between 0 and 100.
    This is only applicable to `"jpeg"` images. Ignored for `"png"` images.
    """

    omit_background: bool
    """
    Whether to hide the default white background and capture the screenshot
    with transparency. This option is not applicable to `"jpeg"` images.
    Defaults to `False`.
    """

    full_page: bool
    """
    Whether to capture a screenshot of the full scrollable page, instead
    of just the visible viewport. Defaults to `False`.
    """

    clip: FloatRect
    """
    Specifies a rectangular region of the page to clip for the screenshot.
    The rectangle is defined by its x and y coordinates, width, and height.
    """

    animations: Literal["allow", "disabled"]
    """
    Specifies how animations are handled during the screenshot:

    - `"allow"`: Leaves animations untouched (default).
    - `"disabled"`: Disables CSS animations, CSS transitions, and Web Animations.
        - Finite animations are fast-forwarded to completion (fires `transitionend`).
        - Infinite animations are canceled to their initial state.
    """

    caret: Literal["hide", "initial"]
    """
    Controls the visibility of the text caret during the screenshot:

    - `"hide"`: Hides the text caret (default).
    - `"initial"`: Leaves the text caret unchanged.
    """

    scale: Literal["css", "device"]
    """
    Determines the scaling of the screenshot:

    - `"css"`: Captures one pixel per CSS pixel on the page (default for high-dpi).
    - `"device"`: Captures one pixel per device pixel, producing larger screenshots
      on high-dpi devices.
    """

    mask: Sequence[Locator]
    """
    A list of locators specifying elements to mask in the screenshot. Masked
    elements are overlaid with a box of the color specified by `mask_color`.
    """

    mask_color: str
    """
    The color of the overlay box used for masking elements, specified in CSS
    color format (e.g., `#FF00FF` for pink). The default color is pink (`#FF00FF`).
    """

    style: str
    """
    A custom stylesheet to apply during the screenshot. This can be used to
    hide dynamic elements, make elements invisible, or modify their properties
    for creating repeatable screenshots. The stylesheet pierces the Shadow DOM
    and applies to inner frames as well.
    """
