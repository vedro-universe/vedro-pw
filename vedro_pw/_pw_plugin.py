import os
from pathlib import Path
from typing import Dict, Type, Union

from playwright.async_api import Page
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
from ._utils import show_pw_trace

__all__ = ("Playwright", "PlaywrightPlugin",)


class PlaywrightPlugin(Plugin):
    """
    Integrates Playwright with Vedro for browser-based testing.

    This plugin provides configurations for browser type, screenshot capturing,
    video recording, trace capturing, and more. It manages the Playwright runtime
    configurations and collects artifacts during test execution.
    """

    def __init__(self, config: Type["Playwright"], *,
                 runtime_config: RuntimeConfig = _runtime_config) -> None:
        """
        Initialize the PlaywrightPlugin with the provided configuration.

        :param config: The Playwright configuration class.
        :param runtime_config: The runtime configuration for Playwright.
        """
        super().__init__(config)
        self._runtime_config = runtime_config
        self._browser: PlaywrightBrowser = config.browser
        self._device: Union[str, None] = config.device
        self._headed: bool = config.headed
        self._slowmo: int = config.slowmo

        self._remote: bool = config.remote
        self._remote_endpoint: str = config.remote_endpoint

        self._capture_screenshots: CaptureMode = config.capture_screenshots
        self._capture_video: CaptureMode = config.capture_video
        self._capture_trace: CaptureMode = config.capture_trace
        self._open_last_trace: bool = False

        self._timeout: Union[int, None] = config.timeout
        self._navigation_timeout: Union[int, None] = config.navigation_timeout
        self._browser_timeout: Union[int, None] = config.browser_timeout

        self._prev_scenario_id: Union[str, None] = None
        self._captured_trace: Union[Path, None] = None
        self._captured_video: Union[Path, None] = None
        self._captured_screenshots: Dict[str, Path] = {}

    def subscribe(self, dispatcher: Dispatcher) -> None:
        """
        Subscribe to the necessary Vedro events for managing Playwright configurations.

        :param dispatcher: The event dispatcher to register listeners on.
        """
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
                  .listen(ArgParsedEvent, self.on_arg_parsed) \
                  .listen(ScenarioRunEvent, self.on_scenario_run) \
                  .listen(StepPassedEvent, self.on_step_end) \
                  .listen(StepFailedEvent, self.on_step_end) \
                  .listen(ScenarioPassedEvent, self.on_scenario_end) \
                  .listen(ScenarioFailedEvent, self.on_scenario_end) \
                  .listen(CleanupEvent, self.on_cleanup)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        """
        Handle the event when command-line arguments are being parsed.

        Adds Playwright-specific arguments to the argument parser.

        :param event: The ArgParseEvent instance containing the argument parser.
        """
        group = event.arg_parser.add_argument_group("Playwright")

        group.add_argument("--pw-browser", action="store",
                           type=PlaywrightBrowser, choices=PlaywrightBrowser,
                           default=self._browser,
                           help=f"Specify the browser to use (default: {self._browser})")
        group.add_argument("--pw-slowmo", action="store", type=int, default=self._slowmo,
                           help=("Slow down Playwright operations by the specified milliseconds "
                                 f"(default: {self._slowmo})"))

        mode_group = group.add_mutually_exclusive_group()
        mode_group.add_argument("--pw-headed", action="store_true", default=None,
                                help=f"Run the browser in headed mode (default: {self._headed})")
        mode_group.add_argument("--pw-headless", action="store_true", default=None,
                                help=("Run the browser in headless mode "
                                      f"(default: {not self._headed})"))

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

        group.add_argument("--pw-device", action="store", default=self._device,
                           help="Emulate a specific device (e.g., 'iPhone 15 Pro' or 'Pixel 7')")

        group.add_argument("--pw-debug", action="store_true", default=False,
                           help="Enable Playwright debug mode by setting PWDEBUG=1")

        group.add_argument("--pw-open-last-trace", action="store_true",
                           default=self._open_last_trace,
                           help="Open the most recent Playwright trace (if available)")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        """
        Handle the event after command-line arguments have been parsed.

        Sets runtime configuration values based on the parsed arguments.

        :param event: The ArgParsedEvent instance containing parsed arguments.
        :raises ValueError: If the `--pw-slowmo` value is negative.
        """
        if event.args.pw_headless is not None:
            self._runtime_config.headed = False
        elif event.args.pw_headed is not None:
            self._runtime_config.headed = True
        else:
            self._runtime_config.headed = self._headed

        self._runtime_config.browser_name = event.args.pw_browser
        self._runtime_config.device_name = event.args.pw_device

        slomo = event.args.pw_slowmo
        if slomo < 0:
            raise ValueError("Slowmo must be a non-negative integer")
        self._runtime_config.slowmo = slomo

        self._runtime_config.remote = event.args.pw_remote
        self._runtime_config.remote_endpoint = event.args.pw_remote_endpoint

        self._capture_screenshots = event.args.pw_screenshots
        self._capture_video = event.args.pw_video
        self._capture_trace = event.args.pw_trace

        if self._runtime_config.remote and self._capture_video != CaptureMode.NEVER:
            print("Playwright cannot capture video when using a remote browser for some reason")

        if event.args.pw_debug:
            os.environ["PWDEBUG"] = "1"

        self._open_last_trace = event.args.pw_open_last_trace

        if self._timeout is not None:
            self._runtime_config.timeout = self._timeout
        if self._navigation_timeout is not None:
            self._runtime_config.navigation_timeout = self._navigation_timeout
        if self._browser_timeout is not None:
            self._runtime_config.browser_timeout = self._browser_timeout

    async def on_scenario_run(self, event: ScenarioRunEvent) -> None:
        """
        Handle the event when a scenario begins execution.

        Configures trace, video, and screenshot capturing based on the scenario's state.

        :param event: The ScenarioRunEvent instance.
        """
        is_rescheduled = (event.scenario_result.scenario.unique_id == self._prev_scenario_id)
        self._prev_scenario_id = event.scenario_result.scenario.unique_id

        self._captured_trace = None
        self._runtime_config.should_capture_trace = False
        if self._should_capture(self._capture_trace, is_rescheduled):
            self._runtime_config.should_capture_trace = True
            self._captured_trace = create_tmp_file(prefix="pw_trace_", suffix=".zip")
            self._runtime_config.trace_options = {
                "path": self._captured_trace,
                "screenshots": True,
                "snapshots": True,
            }

        self._captured_video = None
        self._runtime_config.should_capture_video = False
        if self._should_capture(self._capture_video, is_rescheduled):
            self._runtime_config.should_capture_video = True
            self._captured_video = create_tmp_dir(prefix="pw_video_")
            self._runtime_config.video_options = {
                "record_video_dir": self._captured_video,
                # "record_video_size": None,
            }

        self._captured_screenshots = {}
        self._runtime_config.should_capture_screenshots = (
            self._should_capture(self._capture_screenshots, is_rescheduled)
        )

    def _should_capture(self, capture_mode: CaptureMode, is_rescheduled: bool) -> bool:
        """
        Determine if an artifact should be captured based on the capture mode.

        :param capture_mode: The mode specifying when to capture the artifact.
        :param is_rescheduled: Whether the scenario has been rescheduled.
        :return: True if the artifact should be captured, False otherwise.
        """
        if capture_mode in (CaptureMode.ALWAYS, CaptureMode.ON_FAILURE):
            return True
        elif capture_mode == CaptureMode.ON_RESCHEDULE and is_rescheduled:
            return True
        else:
            return False

    def _should_retain(self, capture_mode: CaptureMode, is_failed: bool) -> bool:
        """
        Determine if a captured artifact should be retained based on the capture mode.

        :param capture_mode: The mode specifying when to retain the artifact.
        :param is_failed: Whether the scenario or step has failed.
        :return: True if the artifact should be retained, False otherwise.
        """
        if capture_mode in (CaptureMode.ALWAYS, CaptureMode.ON_RESCHEDULE):
            return True
        elif capture_mode == CaptureMode.ON_FAILURE and is_failed:
            return True
        else:
            return False

    async def on_step_end(self, event: Union[StepPassedEvent, StepFailedEvent]) -> None:
        """
        Handle the event when a step completes execution.

        Captures screenshots of the current state of the browser, if configured.

        :param event: The StepPassedEvent or StepFailedEvent instance.
        """
        if not self._runtime_config.should_capture_screenshots:
            return

        step_name = event.step_result.step.name
        for context in self._runtime_config.get_browser_contexts():
            for page in context.pages:
                try:
                    screenshot_path = await self._capture_screenshot(page, step_name)
                except Exception as e:
                    event.step_result.add_extra_details(f"Failed to capture screenshot: {e!r}")
                else:
                    self._captured_screenshots[step_name] = screenshot_path

    async def _capture_screenshot(self, page: Page, step_name: str) -> Path:
        """
        Capture a screenshot of the current browser page and save it to a temporary file.

        This method generates a unique file name based on the step number and step name,
        saves the screenshot to a temporary file, and returns the file path.

        :param page: The Playwright `Page` instance to capture the screenshot from.
        :param step_name: The name of the step, used in the screenshot file name.
        :return: The path to the temporary file where the screenshot is saved.
        :raises playwright.async_api.Error: If the screenshot capture fails.
        """
        screenshot_number = len(self._captured_screenshots) + 1
        prefix = f"step{screenshot_number:02}_{step_name}_"
        screenshot_path = create_tmp_file(prefix=prefix, suffix=".png")

        await page.screenshot(path=screenshot_path)

        return screenshot_path

    async def on_scenario_end(self,
                              event: Union[ScenarioPassedEvent, ScenarioFailedEvent]) -> None:
        """
        Handle the event when a scenario completes execution.

        Attaches any captured artifacts (trace, video, screenshots) to the scenario result.

        :param event: The ScenarioPassedEvent or ScenarioFailedEvent instance.
        """
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
        """
        Find the first file in the given directory.

        :param directory: The directory to search for files.
        :return: The Path to the first file, or None if no files are found.
        """
        if directory and directory.is_dir():
            for file in directory.iterdir():
                if file.is_file():
                    return file
        return None

    def _create_trace_artifact(self, trace_path: Path) -> FileArtifact:
        """
        Create a FileArtifact for a captured trace.

        :param trace_path: The Path to the trace file.
        :return: A FileArtifact representing the trace.
        """
        return FileArtifact(trace_path.name, "application/zip", trace_path)

    def _create_video_artifact(self, video_path: Path) -> FileArtifact:
        """
        Create a FileArtifact for a captured video.

        :param video_path: The Path to the video file.
        :return: A FileArtifact representing the video.
        """
        return FileArtifact(f"pw_video_{video_path.name}", "video/webm", video_path)

    def _create_screenshot_artifact(self, screenshot_path: Path) -> FileArtifact:
        """
        Create a FileArtifact for a captured screenshot.

        :param screenshot_path: The Path to the screenshot file.
        :return: A FileArtifact representing the screenshot.
        """
        return FileArtifact(screenshot_path.name, "image/png", screenshot_path)

    def on_cleanup(self, event: CleanupEvent) -> None:
        """
        Handle the cleanup event to finalize the Playwright test session.

        If the `--pw-open-last-trace` option is enabled and a trace was captured,
        this method attempts to open the Playwright trace viewer for the last captured trace.

        :param event: The CleanupEvent instance triggered during cleanup.
        """
        if not self._open_last_trace:
            return

        if self._captured_trace is None:
            event.report.add_summary("No Playwright trace was captured")
            return

        try:
            show_pw_trace(self._captured_trace)
        except Exception as e:
            event.report.add_summary(f"Failed to show Playwright trace: {e}")
        else:
            event.report.add_summary(f"Opened Playwright trace '{self._captured_trace}'")


class Playwright(PluginConfig):
    """
    Configuration class for the PlaywrightPlugin.

    Provides default settings for browser automation, including browser type,
    device emulation, trace capturing, video recording, and screenshot capturing.
    """

    plugin = PlaywrightPlugin
    description = ("Integrates Playwright for automated browser testing "
                   "with customizable configuration options")

    # Specifies the browser to use (CHROMIUM, FIREFOX, WEBKIT, or RANDOM)
    # Docs: https://playwright.dev/python/docs/browsers
    browser: PlaywrightBrowser = PlaywrightBrowser.CHROMIUM

    # Specifies the device to emulate (e.g., "iPhone 15 Pro" or "Pixel 7").
    # If set to None, no device emulation will be applied.
    # Docs: https://playwright.dev/docs/emulation
    device: Union[str, None] = None

    # Determines whether the browser should run in headed (True) or headless (False) mode.
    # Headless mode does not display a visible browser window.
    headed: bool = False

    # Introduces a delay (in milliseconds) to slow down browser operations.
    # Useful for debugging or observing the browser behavior during tests.
    slowmo: int = 0

    # Determines if the browser session should connect to a remote instance.
    # Set to True to use a remote browser, otherwise the browser will be launched locally.
    remote: bool = False

    # Specifies the WebSocket endpoint URL for connecting to a remote browser.
    # This is only used when `remote` is set to True.
    remote_endpoint: str = "ws://localhost:3000"

    # Controls whether screenshots are captured during the test run.
    # Screenshots are created after every step, providing visual feedback for execution.
    # Docs: https://playwright.dev/python/docs/screenshots
    capture_screenshots: CaptureMode = CaptureMode.NEVER

    # Controls whether videos of the browser session are recorded.
    # Docs: https://playwright.dev/python/docs/videos
    capture_video: CaptureMode = CaptureMode.NEVER

    # Controls whether traces of browser interactions are captured.
    # Docs: https://playwright.dev/python/docs/trace-viewer-intro
    capture_trace: CaptureMode = CaptureMode.NEVER

    # Specifies the default maximum time (in milliseconds) for browser operations.
    # This timeout applies to all methods that support the `timeout` option.
    # It is passed to context.set_default_timeout(timeout)
    # If set to `None`, Playwright's default timeout is used.
    timeout: Union[int, None] = None

    # Specifies the maximum navigation timeout (in milliseconds) for browser navigation operations.
    # This timeout applies to navigation-related methods, such as `page.goto()`.
    # It is passed to context.set_default_navigation_timeout(navigation_timeout)
    # If set to `None`, Playwright's default navigation timeout is used.
    navigation_timeout: Union[int, None] = None

    # Specifies the maximum time (in milliseconds) to wait for the browser instance to start.
    # This timeout applies when launching a browser using `browser_type.launch(timeout=timeout)`.
    # Defaults to 30,000 milliseconds (30 seconds). Pass `0` to disable the timeout.
    browser_timeout: Union[int, None] = None
