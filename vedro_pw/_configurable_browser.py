from typing import Any, Optional

from playwright.async_api import Browser, BrowserContext, Page
from vedro import defer

from ._runtime_config import RuntimeConfig
from ._runtime_config import runtime_config as _runtime_config
from .options import DeviceOptions

__all__ = ("ConfigurableBrowser",)


class ConfigurableBrowser(Browser):
    """
    Extends the Playwright `Browser` to provide configurable options and runtime integration.

    This class integrates device options and runtime configurations, such as timeouts,
    video recording, and tracing, into the creation of browser contexts and pages.
    """

    def __init__(self, impl_obj: Browser, *,
                 device_options: Optional[DeviceOptions] = None,
                 runtime_config: RuntimeConfig = _runtime_config) -> None:
        """
        Initialize the ConfigurableBrowser.

        :param impl_obj: The underlying Playwright `Browser` instance.
        :param device_options: Optional device-specific options for emulation.
        :param runtime_config: The runtime configuration for the browser.
        """
        super().__init__(impl_obj._impl_obj)
        self._runtime_config = runtime_config
        self._device_options = device_options or {}

    async def new_context(self, **kwargs: Any) -> BrowserContext:
        """
        Create a new browser context with integrated runtime configurations.

        This method applies device options, runtime settings, and captures
        artifacts such as videos or traces if configured.

        :param kwargs: Additional options to override or extend the context settings.
        :return: A new `BrowserContext` instance with the configured options.
        """
        options = {
            **self._device_options,
            **kwargs
        }

        if self._runtime_config.should_capture_video:
            video_options = self._runtime_config.video_options
            options["record_video_dir"] = video_options["record_video_dir"]

        context = await super().new_context(**options)
        defer(context.close)
        defer(self._runtime_config.remove_browser_context, context)

        default_timeout = self._runtime_config.timeout
        if default_timeout is not None:
            context.set_default_timeout(default_timeout)
        navigation_timeout = self._runtime_config.navigation_timeout
        if navigation_timeout is not None:
            context.set_default_navigation_timeout(navigation_timeout)

        if self._runtime_config.should_capture_trace:
            trace_options = self._runtime_config.trace_options
            await context.tracing.start(screenshots=trace_options["screenshots"],
                                        snapshots=trace_options["snapshots"])
            defer(context.tracing.stop, path=trace_options["path"])

        self._runtime_config.add_browser_context(context)

        return context

    async def new_page(self, **kwargs: Any) -> Page:
        """
        Create a new browser page within a newly created context.

        This method creates a new context and opens a single page within it.

        :param kwargs: Additional options to override or extend the context settings.
        :return: A new `Page` instance within the created context.
        """
        context = await self.new_context(**kwargs)
        return await context.new_page()
