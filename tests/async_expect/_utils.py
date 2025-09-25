from contextlib import contextmanager
from typing import Any, Generator
from unittest.mock import AsyncMock, Mock, patch

from playwright.async_api import APIResponse, Locator, Page

__all__ = ("make_page", "make_locator", "make_api_response", "patch_class", "make_method_mock",)


@contextmanager
def patch_class(target: str, inst: Any) -> Generator[Mock, None, None]:
    with patch(target, Mock(return_value=inst)) as patched:
        yield patched


def make_page() -> Page:
    return Mock(spec=Page, _impl_obj=Mock())


def make_locator() -> Locator:
    return Mock(spec=Locator, _impl_obj=Mock())


def make_api_response() -> APIResponse:
    return Mock(spec=APIResponse, _impl_obj=Mock())


def make_method_mock(**kwargs: Any) -> Mock:
    mock = Mock()
    for name, value in kwargs.items():
        setattr(mock, name, AsyncMock(side_effect=[value]))
    return mock
