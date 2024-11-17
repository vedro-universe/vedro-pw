from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Literal, Pattern, Sequence, TypedDict, Union

if TYPE_CHECKING:
    from playwright._impl._api_structures import ClientCertificate
else:
    from typing import Any
    ClientCertificate = Any

from playwright.async_api import (
    FloatRect,
    Geolocation,
    HttpCredentials,
    Locator,
    ProxySettings,
    StorageState,
    ViewportSize,
)

__all__ = ("LaunchOptions", "ConnectOptions", "NewContextOptions", "DeviceOptions",
           "TraceOptions", "VideoOptions", "ScreenshotOptions",)


class LaunchOptions(TypedDict, total=False):
    """
    Represents the options for launching a browser instance.

    Defines all configurable parameters for the `launch` method of the `BrowserType` class.
    """

    executable_path: Union[str, Path]
    """Path to a browser executable to run instead of the bundled one."""

    channel: str
    """Browser distribution channel. Supported values include 'chrome', 'msedge', etc."""

    args: Sequence[str]
    """Additional arguments to pass to the browser instance."""

    ignore_default_args: Union[bool, Sequence[str]]
    """If `True`, disables Playwright's default browser arguments."""

    handle_sigint: bool
    """Close the browser process on Ctrl-C."""

    handle_sigterm: bool
    """Close the browser process on SIGTERM."""

    handle_sighup: bool
    """Close the browser process on SIGHUP."""

    timeout: float
    """Maximum time in milliseconds to wait for the browser instance to start."""

    env: Dict[str, Union[str, float, bool]]
    """Environment variables to be visible to the browser."""

    headless: bool
    """Run the browser in headless mode."""

    devtools: bool
    """Auto-open a Developer Tools panel for each tab (Chromium-only)."""

    proxy: ProxySettings
    """Network proxy settings."""

    downloads_path: Union[str, Path]
    """Path where accepted downloads are stored."""

    slow_mo: float
    """Slows down Playwright operations by the specified milliseconds."""

    traces_dir: Union[str, Path]
    """Path to save browser traces."""

    chromium_sandbox: bool
    """Enable or disable Chromium sandboxing."""

    firefox_user_prefs: Dict[str, Union[str, float, bool]]
    """Custom Firefox user preferences."""


class ConnectOptions(TypedDict, total=False):
    """
    Represents the options for connecting to an existing browser instance.

    Defines all configurable parameters for the `connect` method of the `BrowserType` class.
    """

    ws_endpoint: str
    """A browser websocket endpoint to connect to."""

    timeout: float
    """Maximum time in milliseconds to wait for the connection to be established."""

    slow_mo: float
    """Slows down Playwright operations by the specified amount of milliseconds."""

    headers: Dict[str, str]
    """Additional HTTP headers to be sent with the web socket connect request."""

    expose_network: str
    """Defines network rules to expose from the client to the connected browser."""


class NewContextOptions(TypedDict, total=False):
    """
    Represents the options for creating a new browser context.

    Defines all configurable parameters for the `new_context` method of the `Browser` class.
    """

    viewport: ViewportSize
    """
    Sets a consistent viewport for each page. Defaults to 1280x720 if not disabled by `no_viewport`
    """

    screen: ViewportSize
    """Emulates consistent window screen size available inside web pages."""

    no_viewport: bool
    """Disables fixed viewport, allowing window resizing in headed mode."""

    ignore_https_errors: bool
    """Specifies whether to ignore HTTPS errors when sending network requests."""

    java_script_enabled: bool
    """Specifies whether JavaScript should be enabled. Defaults to `true`."""

    bypass_csp: bool
    """Enables bypassing of page's Content-Security-Policy."""

    user_agent: str
    """Specifies the user agent string to use in this context."""

    locale: str
    """Specifies the user locale, affecting `navigator.language` and date/number formatting."""

    timezone_id: str
    """Specifies the timezone for the context."""

    geolocation: Geolocation
    """Sets geolocation for the context."""

    permissions: Sequence[str]
    """List of permissions to grant to all pages in the context."""

    extra_http_headers: Dict[str, str]
    """Additional HTTP headers sent with every request in the context."""

    offline: bool
    """Emulates offline network conditions."""

    http_credentials: HttpCredentials
    """Credentials for HTTP authentication."""

    device_scale_factor: float
    """Specifies the device scale factor (similar to DPR)."""

    is_mobile: bool
    """Specifies if the context should emulate a mobile device."""

    has_touch: bool
    """Specifies whether the viewport should support touch events."""

    color_scheme: Literal["dark", "light", "no-preference", "null"]
    """Emulates the `prefers-color-scheme` media feature."""

    reduced_motion: Literal["no-preference", "null", "reduce"]
    """Emulates the `prefers-reduced-motion` media feature."""

    forced_colors: Literal["active", "none", "null"]
    """Emulates the `forced-colors` media feature."""

    accept_downloads: bool
    """Automatically accepts all downloads in the context."""

    default_browser_type: str
    """Specifies the default browser type for the context."""

    proxy: ProxySettings
    """Configures network proxy settings."""

    record_har_path: Union[str, Path]
    """Specifies the file path to save HAR recordings."""

    record_har_omit_content: bool
    """Controls whether to omit request content from HAR recordings."""

    record_video_dir: Union[str, Path]
    """Specifies the directory to save recorded videos."""

    record_video_size: ViewportSize
    """Specifies the dimensions of recorded videos."""

    storage_state: Union[StorageState, str, Path]
    """Populates the context with given storage state (e.g., cookies and localStorage)."""

    base_url: str
    """Specifies the base URL for relative navigations."""

    strict_selectors: bool
    """Enables strict selectors mode for this context."""

    service_workers: Literal["allow", "block"]
    """Controls whether service workers can be registered."""

    record_har_url_filter: Union[str, Pattern[str]]
    """Specifies a URL filter for HAR recordings."""

    record_har_mode: Literal["full", "minimal"]
    """Controls the level of detail recorded in HAR files."""

    record_har_content: Literal["attach", "embed", "omit"]
    """Specifies how to handle resource content in HAR files."""

    client_certificates: List[ClientCertificate]
    """Configures TLS client certificates for the context."""


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
