from ._capture_mode import CaptureMode
from ._pw_browser import PlaywrightBrowser

__all__ = ("RuntimeConfig", "runtime_config",)


class RuntimeConfig:
    def __init__(self) -> None:
        self._browser: PlaywrightBrowser = PlaywrightBrowser.CHROMIUM
        self._headed: bool = False
        self._slowmo: int = 0
        self._capture_screenshots: CaptureMode = CaptureMode.NEVER
        self._capture_video: CaptureMode = CaptureMode.NEVER
        self._capture_trace: CaptureMode = CaptureMode.NEVER

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

    # Capture Screenshots
    def get_capture_screenshots(self) -> CaptureMode:
        return self._capture_screenshots

    def set_capture_screenshots(self, value: CaptureMode) -> None:
        self._capture_screenshots = value

    # Capture Video
    def get_capture_video(self) -> CaptureMode:
        return self._capture_video

    def set_capture_video(self, value: CaptureMode) -> None:
        self._capture_video = value

    # Capture Trace
    def get_capture_trace(self) -> CaptureMode:
        return self._capture_trace

    def set_capture_trace(self, value: CaptureMode) -> None:
        self._capture_trace = value


runtime_config = RuntimeConfig()
