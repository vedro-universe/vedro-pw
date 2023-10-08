from typing import Type

from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import ArgParsedEvent, ArgParseEvent, StartupEvent

__all__ = ("Playwright", "PlaywrightPlugin",)


class PlaywrightPlugin(Plugin):
    def __init__(self, config: Type["Playwright"]) -> None:
        super().__init__(config)
        # self._headless: bool = False

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
            .listen(ArgParsedEvent, self.on_arg_parsed)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        # event.arg_parser.add_argument("--pw-headless", action="store_true",
        #                               default=self._headless, help="<desc>")
        pass

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        # self._headless = event.args.pw_headless
        pass

    def on_startup(self, event: StartupEvent) -> None:
        pass


class Playwright(PluginConfig):
    plugin = PlaywrightPlugin
    description = "<desc>"
