from baby_steps import then, when
from vedro.core import Plugin

from vedro_pw import Playwright, PlaywrightPlugin


def test_plugin():
    with when:
        plugin = PlaywrightPlugin(Playwright)

    with then:
        assert isinstance(plugin, Plugin)
