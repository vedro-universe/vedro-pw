from typing import Type

from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import ArgParsedEvent, ArgParseEvent, CleanupEvent, StartupEvent

from ._capture_mode import CaptureMode
from ._pw_browser import PlaywrightBrowser
from ._runtime_config import RuntimeConfig
from ._runtime_config import runtime_config as _runtime_config

__all__ = ("Playwright", "PlaywrightPlugin",)


class PlaywrightPlugin(Plugin):
    def __init__(self, config: Type["Playwright"], *,
                 runtime_config: RuntimeConfig = _runtime_config) -> None:
        super().__init__(config)
        self._runtime_config = runtime_config
        self._browser: PlaywrightBrowser = config.browser
        self._headed: bool = config.headed
        self._slowmo: int = config.slowmo
        self._capture_screenshots: CaptureMode = config.capture_screenshots
        self._capture_video: CaptureMode = config.capture_video
        self._capture_trace: CaptureMode = config.capture_trace

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
                  .listen(ArgParsedEvent, self.on_arg_parsed) \
                  .listen(StartupEvent, self.on_startup) \
                  .listen(CleanupEvent, self.on_cleanup)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        group = event.arg_parser.add_argument_group("Playwright")

        group.add_argument("--pw-browser", action="store",
                           type=PlaywrightBrowser, choices=PlaywrightBrowser,
                           default=self._browser,
                           help=f"Specify the browser to use (default: {self._browser})")
        group.add_argument("--pw-headed", action="store_true", default=self._headed,
                           help=f"Run the browser in headed mode (default: {self._headed})")
        group.add_argument("--pw-slowmo", action="store", type=int, default=self._slowmo,
                           help=("Slow down Playwright operations by the specified milliseconds "
                                 f"(default: {self._slowmo})"))

        group.add_argument("--pw-screenshots", action="store",
                           type=CaptureMode, choices=CaptureMode,
                           default=self._capture_screenshots,
                           help=("Control screenshot capturing behavior "
                                 f"(default: {self._capture_screenshots})"))
        group.add_argument("--pw-video", action="store",
                           type=CaptureMode, choices=CaptureMode,
                           default=self._capture_video,
                           help=("Control video recording behavior default "
                                 f"({self._capture_video})"))
        group.add_argument("--pw-trace", action="store",
                           type=CaptureMode, choices=CaptureMode,
                           default=self._capture_trace,
                           help=("Control trace recording behavior "
                                 f"(default: {self._capture_trace})"))

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._runtime_config.set_browser(event.args.pw_browser)
        self._runtime_config.set_headed(event.args.pw_headed)
        self._runtime_config.set_slowmo(event.args.pw_slowmo)
        self._runtime_config.set_capture_screenshots(event.args.pw_screenshots)
        self._runtime_config.set_capture_video(event.args.pw_video)
        self._runtime_config.set_capture_trace(event.args.pw_trace)

    def on_startup(self, event: StartupEvent) -> None:
        pass

    def on_cleanup(self, event: CleanupEvent) -> None:
        pass


class Playwright(PluginConfig):
    plugin = PlaywrightPlugin
    description = "<desc>"

    browser: PlaywrightBrowser = PlaywrightBrowser.CHROMIUM
    headed: bool = False
    slowmo: int = 0

    capture_screenshots: CaptureMode = CaptureMode.NEVER
    capture_video: CaptureMode = CaptureMode.NEVER
    capture_trace: CaptureMode = CaptureMode.NEVER
