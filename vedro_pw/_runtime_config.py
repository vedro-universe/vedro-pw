from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ._pw_browser import PlaywrightBrowser
from .options import ScreenshotOptions, TraceOptions, VideoOptions

__all__ = ("RuntimeConfig", "runtime_config",)


@dataclass
class RuntimeConfig:
    browser_name: PlaywrightBrowser = PlaywrightBrowser.CHROMIUM
    device_name: Optional[str] = None

    headed: bool = False
    slowmo: int = 0

    remote: bool = False
    remote_endpoint: str = ""

    timeout: Optional[int] = None
    navigation_timeout: Optional[int] = None
    browser_timeout: Optional[int] = None

    # using dict instead of set to store browser contexts with preserved order
    browser_contexts: Dict[Any, Any] = field(default_factory=dict)

    should_capture_trace: bool = False
    trace_options: TraceOptions = field(default_factory=lambda: TraceOptions())

    should_capture_video: bool = False
    video_options: VideoOptions = field(default_factory=lambda: VideoOptions())

    should_capture_screenshots: bool = False
    screenshot_options: ScreenshotOptions = field(default_factory=lambda: ScreenshotOptions())

    def add_browser_context(self, context: Any) -> None:
        self.browser_contexts[context] = ...

    def remove_browser_context(self, context: Any) -> None:
        self.browser_contexts.pop(context, None)

    def get_browser_contexts(self) -> List[Any]:
        return list(self.browser_contexts.keys())


runtime_config = RuntimeConfig()
