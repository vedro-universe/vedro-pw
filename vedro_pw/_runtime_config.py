from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ._pw_browser import PlaywrightBrowser

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

    browser_contexts: Dict[Any, Any] = field(default_factory=dict)

    should_capture_trace: bool = False
    trace_options: Dict[str, Any] = field(default_factory=dict)

    should_capture_video: bool = False
    video_options: Dict[str, Any] = field(default_factory=dict)

    should_capture_screenshots: bool = False
    screenshot_options: Dict[str, Any] = field(default_factory=dict)

    def add_browser_context(self, context: Any) -> None:
        self.browser_contexts[context] = ...

    def remove_browser_context(self, context: Any) -> None:
        self.browser_contexts.pop(context, None)

    def get_browser_contexts(self) -> List[Any]:
        return list(self.browser_contexts.keys())


runtime_config = RuntimeConfig()
