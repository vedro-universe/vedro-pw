from pathlib import Path
from typing import Dict, Type, Union

from vedro import FileArtifact, create_tmp_dir, create_tmp_file
from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import (
    ArgParsedEvent,
    ArgParseEvent,
    CleanupEvent,
    ScenarioFailedEvent,
    ScenarioPassedEvent,
    ScenarioRunEvent,
    StepFailedEvent,
    StepPassedEvent,
)

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

        self._remote: bool = config.remote
        self._remote_endpoint: str = config.remote_endpoint

        self._capture_screenshots: CaptureMode = config.capture_screenshots
        self._capture_video: CaptureMode = config.capture_video
        self._capture_trace: CaptureMode = config.capture_trace

        self._timeout: Union[int, None] = config.timeout
        self._navigation_timeout: Union[int, None] = config.navigation_timeout
        self._browser_timeout: Union[int, None] = config.browser_timeout

        self._prev_scenario_id: Union[str, None] = None
        self._captured_trace: Union[Path, None] = None
        self._captured_video: Union[Path, None] = None
        self._captured_screenshots: Dict[str, Path] = {}

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
                  .listen(ArgParsedEvent, self.on_arg_parsed) \
                  .listen(ScenarioRunEvent, self.on_scenario_run) \
                  .listen(StepPassedEvent, self.on_step_end) \
                  .listen(StepFailedEvent, self.on_step_end) \
                  .listen(ScenarioPassedEvent, self.on_scenario_end) \
                  .listen(ScenarioFailedEvent, self.on_scenario_end) \
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

        group.add_argument("--pw-remote", action="store_true", default=self._remote,
                           help=f"Connect to a remote browser instance (default: {self._remote})")
        group.add_argument("--pw-remote-endpoint", action="store", default=self._remote_endpoint,
                           help=("WebSocket endpoint URL for the remote browser "
                                 f"(default: {self._remote_endpoint})"))

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

        group.add_argument("--pw-device", action="store",
                           help="Emulate a specific device (e.g., iPhone 15 Pro or Pixel 7)")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._runtime_config.set_browser(event.args.pw_browser)
        self._runtime_config.set_headed(event.args.pw_headed)
        self._runtime_config.set_slowmo(event.args.pw_slowmo)
        self._runtime_config.set_device(event.args.pw_device)

        self._runtime_config.set_remote(event.args.pw_remote)
        self._runtime_config.set_remote_endpoint(event.args.pw_remote_endpoint)

        self._capture_screenshots = event.args.pw_screenshots
        self._capture_video = event.args.pw_video
        self._capture_trace = event.args.pw_trace

        if self._timeout is not None:
            self._runtime_config.set_timeout(self._timeout)
        if self._navigation_timeout is not None:
            self._runtime_config.set_navigation_timeout(self._navigation_timeout)
        if self._browser_timeout is not None:
            self._runtime_config.set_browser_timeout(self._browser_timeout)

    async def on_scenario_run(self, event: ScenarioRunEvent) -> None:
        is_rescheduled = (event.scenario_result.scenario.unique_id == self._prev_scenario_id)
        self._prev_scenario_id = event.scenario_result.scenario.unique_id

        self._captured_trace = None
        self._runtime_config.set_capture_trace(False)
        if self._should_capture(self._capture_trace, is_rescheduled):
            self._runtime_config.set_capture_trace(True)
            self._captured_trace = create_tmp_file(prefix="pw_trace_", suffix=".zip")
            self._runtime_config.set_trace_options({
                "path": self._captured_trace,
                "screenshots": True,
                "snapshots": True,
            })

        self._captured_video = None
        self._runtime_config.set_capture_video(False)
        if self._should_capture(self._capture_video, is_rescheduled):
            self._runtime_config.set_capture_video(True)
            self._captured_video = create_tmp_dir(prefix="pw_video_")
            self._runtime_config.set_video_options({
                "record_video_dir": self._captured_video,
                "record_video_size": None,
            })

        self._captured_screenshots = {}
        self._runtime_config.set_capture_screenshots(
            self._should_capture(self._capture_screenshots, is_rescheduled)
        )

    def _should_capture(self, capture_mode: CaptureMode, is_rescheduled: bool) -> bool:
        if capture_mode in (CaptureMode.ALWAYS, CaptureMode.ON_FAILURE):
            return True
        elif capture_mode == CaptureMode.ON_RESCHEDULE and is_rescheduled:
            return True
        else:
            return False

    def _should_retain(self, capture_mode: CaptureMode, is_failed: bool) -> bool:
        if capture_mode in (CaptureMode.ALWAYS, CaptureMode.ON_RESCHEDULE):
            return True
        elif capture_mode == CaptureMode.ON_FAILURE and is_failed:
            return True
        else:
            return False

    async def on_step_end(self, event: Union[StepPassedEvent, StepFailedEvent]) -> None:
        if self._runtime_config.should_capture_screenshots():
            for context in self._runtime_config.get_browser_contexts():
                for page in context.pages:
                    screenshot_number = len(self._captured_screenshots) + 1
                    prefix = f"step{screenshot_number:02}_{event.step_result.step.name}_"
                    screenshot_path = create_tmp_file(prefix=prefix, suffix=".png")
                    await page.screenshot(path=screenshot_path)
                    self._captured_screenshots[event.step_result.step.name] = screenshot_path

    async def on_scenario_end(self,
                              event: Union[ScenarioPassedEvent, ScenarioFailedEvent]) -> None:
        is_failed = isinstance(event, ScenarioFailedEvent)

        if self._captured_trace:
            if self._should_retain(self._capture_trace, is_failed):
                trace_artifact = self._create_trace_artifact(self._captured_trace)
                event.scenario_result.attach(trace_artifact)
            else:
                self._captured_trace.unlink(missing_ok=True)

        captured_video = self._find_file(self._captured_video)
        if captured_video:
            if self._should_retain(self._capture_video, is_failed):
                video_artifact = self._create_video_artifact(captured_video)
                event.scenario_result.attach(video_artifact)
            else:
                captured_video.unlink(missing_ok=True)

        step_results = {x.step.name: x for x in event.scenario_result.step_results}
        for step_name, screenshot in self._captured_screenshots.items():
            if self._should_retain(self._capture_screenshots, is_failed):
                screenshot_artifact = self._create_screenshot_artifact(screenshot)
                step_result = step_results.get(step_name, event.scenario_result)
                step_result.attach(screenshot_artifact)
            else:
                screenshot.unlink(missing_ok=True)

    def _find_file(self, directory: Union[Path, None]) -> Union[Path, None]:
        if directory and directory.is_dir():
            for file in directory.iterdir():
                if file.is_file():
                    return file
        return None

    def _create_trace_artifact(self, trace_path: Path) -> FileArtifact:
        return FileArtifact(trace_path.name, "application/zip", trace_path)

    def _create_video_artifact(self, video_path: Path) -> FileArtifact:
        return FileArtifact(f"pw_video_{video_path.name}", "video/webm", video_path)

    def _create_screenshot_artifact(self, screenshot_path: Path) -> FileArtifact:
        return FileArtifact(screenshot_path.name, "image/png", screenshot_path)

    def on_cleanup(self, event: CleanupEvent) -> None:
        pass


class Playwright(PluginConfig):
    plugin = PlaywrightPlugin
    description = ("Integrates Playwright for automated browser testing "
                   "with customizable configuration options")

    browser: PlaywrightBrowser = PlaywrightBrowser.CHROMIUM
    headed: bool = False
    slowmo: int = 0

    remote: bool = False
    remote_endpoint: str = "ws://localhost:3000"

    capture_screenshots: CaptureMode = CaptureMode.NEVER
    capture_video: CaptureMode = CaptureMode.NEVER
    capture_trace: CaptureMode = CaptureMode.NEVER

    timeout: Union[int, None] = None
    navigation_timeout: Union[int, None] = None
    browser_timeout: Union[int, None] = None
