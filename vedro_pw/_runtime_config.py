from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from playwright.async_api import BrowserContext

from ._pw_browser import PlaywrightBrowser
from .options import ScreenshotOptions, TraceOptions, VideoOptions

__all__ = ("RuntimeConfig", "runtime_config",)


@dataclass
class RuntimeConfig:
    """
    Holds runtime configurations for Playwright browser sessions.

    This configuration class manages various browser-related settings such as
    the browser type, device emulation, timeouts, and artifact capture options
    (e.g., traces, videos, screenshots). It also tracks active browser contexts.
    """

    browser_name: PlaywrightBrowser = PlaywrightBrowser.CHROMIUM
    """
    The browser to use for sessions. Can be `CHROMIUM`, `FIREFOX`, or `WEBKIT`.
    """

    device_name: Optional[str] = None
    """
    The device to emulate during browser sessions, or `None` to disable device emulation.
    """

    headed: bool = False
    """
    Whether to launch the browser in headed (visible UI) mode.
    """

    slowmo: int = 0
    """
    Delay (in milliseconds) between Playwright operations.
    """

    remote: bool = False
    """
    Indicates if a remote browser instance should be used.
    """

    remote_endpoint: str = ""
    """
    WebSocket URL for connecting to a remote browser instance, if `remote` is `True`.
    """

    timeout: Optional[int] = None
    """
    Default timeout (in milliseconds) for browser operations, such as page load or
    element interactions.
    """

    navigation_timeout: Optional[int] = None
    """
    Timeout (in milliseconds) for browser navigation operations, such as page.goto().
    """

    browser_timeout: Optional[int] = None
    """
    Timeout (in milliseconds) for launching the browser.
    """

    browser_contexts: Dict[Any, Any] = field(default_factory=dict)
    """
    Tracks active browser contexts as a dictionary where the keys are context instances.
    """

    should_capture_trace: bool = False
    """
    Indicates whether to enable trace recording during browser sessions.
    """

    trace_options: TraceOptions = field(default_factory=lambda: TraceOptions())
    """
    Configuration options for trace recording, including file paths, names, and captured data.
    """

    should_capture_video: bool = False
    """
    Indicates whether video recording should be enabled for browser sessions.
    """

    video_options: VideoOptions = field(default_factory=lambda: VideoOptions())
    """
    Configuration options for video recording, such as file formats and storage paths.
    """

    should_capture_screenshots: bool = False
    """
    Indicates whether screenshots should be captured during browser sessions.
    """

    screenshot_options: ScreenshotOptions = field(default_factory=lambda: ScreenshotOptions())
    """
    Configuration options for screenshot capturing, including format, quality, and storage paths.
    """

    def add_browser_context(self, context: BrowserContext) -> None:
        """
        Add a browser context to the tracked list of active contexts.

        :param context: The browser context to add.
        """
        self.browser_contexts[context] = ...

    def remove_browser_context(self, context: BrowserContext) -> None:
        """
        Remove a browser context from the tracked list of active contexts.

        :param context: The browser context to remove.
        """
        self.browser_contexts.pop(context, None)

    def get_browser_contexts(self) -> List[BrowserContext]:
        """
        Retrieve the list of active browser contexts.

        :return: A list of active browser contexts.
        """
        return list(self.browser_contexts.keys())


runtime_config = RuntimeConfig()
