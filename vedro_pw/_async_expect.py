from typing import Any, Optional, Union, cast, overload

from playwright.async_api import APIResponse
from playwright.async_api import APIResponseAssertions as _APIResponseAssertions  # type: ignore
from playwright.async_api import Expect as _Expect
from playwright.async_api import Locator
from playwright.async_api import LocatorAssertions as _LocatorAssertions  # type: ignore
from playwright.async_api import Page
from playwright.async_api import PageAssertions as _PageAssertions  # type: ignore
from vedro import effect

try:
    from playwright._impl._assertions import APIResponseAssertions as APIResponseAssertionsImpl
    from playwright._impl._assertions import LocatorAssertions as LocatorAssertionsImpl
    from playwright._impl._assertions import PageAssertions as PageAssertionsImpl
except ImportError as e:
    raise ImportError(
        "Could not import Playwright internal assertion implementations. "
        "This wrapper relies on Playwright internals that match the public async API. "
        "Make sure Playwright is installed and up to date."
    ) from e


__all__ = ("expect", "Expect",)


class EffectMixin:
    def __getattribute__(self, item: str) -> Any:
        attr = super().__getattribute__(item)
        if callable(attr) and not item.startswith("_"):
            return effect(attr)
        return attr


class PageAssertions(_PageAssertions, EffectMixin):
    pass


class LocatorAssertions(_LocatorAssertions, EffectMixin):
    pass


class APIResponseAssertions(_APIResponseAssertions, EffectMixin):
    pass


class Expect(_Expect):
    @overload
    def __call__(
        self, actual: Page, message: Optional[str] = None
    ) -> PageAssertions: ...

    @overload
    def __call__(
        self, actual: Locator, message: Optional[str] = None
    ) -> LocatorAssertions: ...

    @overload
    def __call__(
        self, actual: APIResponse, message: Optional[str] = None
    ) -> APIResponseAssertions: ...

    def __call__(self,
                 actual: Union[Page, Locator, APIResponse],
                 message: Optional[str] = None
                 ) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
        if isinstance(actual, Page):
            return PageAssertions(
                PageAssertionsImpl(actual._impl_obj,
                                   cast(float, self._timeout),
                                   message=message)
            )
        elif isinstance(actual, Locator):
            return LocatorAssertions(
                LocatorAssertionsImpl(actual._impl_obj,
                                      cast(float, self._timeout),
                                      message=message)
            )
        elif isinstance(actual, APIResponse):
            return APIResponseAssertions(
                APIResponseAssertionsImpl(actual._impl_obj,
                                          cast(float, self._timeout),
                                          message=message)
            )
        raise ValueError(f"Unsupported type: {type(actual)}")


expect = Expect()
