from typing import Any, Dict, List

from ._pw_browser import PlaywrightBrowser

__all__ = ("RuntimeConfig", "runtime_config",)


class RuntimeConfig:
    def __init__(self) -> None:
        self._browser: PlaywrightBrowser = PlaywrightBrowser.CHROMIUM
        self._headed: bool = False
        self._slowmo: int = 0

        self._browser_contexts: Dict[Any, Any] = {}

        self._should_capture_trace: bool = False
        self._trace_options: Dict[str, Any] = {}

        self._should_capture_video: bool = False
        self._video_options: Dict[str, Any] = {}

        self._should_capture_screenshots: bool = False
        self._screenshot_options: Dict[str, Any] = {}

    # Browser

    def get_browser(self) -> PlaywrightBrowser:
        return self._browser

    def set_browser(self, value: PlaywrightBrowser) -> None:
        self._browser = value

    # Headed

    def is_headed(self) -> bool:
        return self._headed

    def set_headed(self, value: bool) -> None:
        self._headed = value

    # Slowmo

    def get_slowmo(self) -> int:
        return self._slowmo

    def set_slowmo(self, value: int) -> None:
        if value < 0:
            raise ValueError("Slowmo must be a non-negative integer")
        self._slowmo = value

    # Browser Context

    def add_browser_context(self, context: Any) -> None:
        self._browser_contexts[context] = ...

    def remove_browser_context(self, context: Any) -> None:
        self._browser_contexts.pop(context, None)

    def get_browser_contexts(self) -> List[Any]:
        return [x for x in self._browser_contexts]

    # Capture Trace

    def should_capture_trace(self) -> bool:
        return self._should_capture_trace

    def set_capture_trace(self, value: bool) -> None:
        self._should_capture_trace = value

    def get_trace_options(self) -> Dict[str, Any]:
        return self._trace_options

    def set_trace_options(self, options: Dict[str, Any]) -> None:
        self._trace_options = options

    # Capture Video

    def should_capture_video(self) -> bool:
        return self._should_capture_video

    def set_capture_video(self, value: bool) -> None:
        self._should_capture_video = value

    def get_video_options(self) -> Dict[str, Any]:
        return self._video_options

    def set_video_options(self, options: Dict[str, Any]) -> None:
        self._video_options = options

    # Capture Screenshots

    def should_capture_screenshots(self) -> bool:
        return self._should_capture_screenshots

    def set_capture_screenshots(self, value: bool) -> None:
        self._should_capture_screenshots = value

    def get_screenshot_options(self) -> Dict[str, Any]:
        return self._screenshot_options

    def set_screenshot_options(self, options: Dict[str, Any]) -> None:
        self._screenshot_options = options


runtime_config = RuntimeConfig()
