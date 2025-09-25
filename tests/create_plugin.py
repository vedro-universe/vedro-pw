from vedro import scenario, then, when
from vedro.core import Plugin

from vedro_pw import Playwright, PlaywrightPlugin


@scenario("create plugin")
def _():
    with when:
        plugin = PlaywrightPlugin(Playwright)

    with then:
        assert isinstance(plugin, Plugin)
