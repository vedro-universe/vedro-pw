from unittest.mock import call

from vedro import catched, given, scenario, then, when

from vedro_pw import expect

from ._utils import make_api_response, make_locator, make_method_mock, make_page, patch_class

# PageAssertions


@scenario("[PageAssertions] call async expect")
async def _():
    with given:
        page = make_page()
        page_assertions = make_method_mock(to_have_title=None)

        target = "vedro_pw._async_expect.PageAssertionsImpl"

    with when, patch_class(target, page_assertions):
        await expect(page).to_have_title("<title>")

    with then:
        assert page_assertions.mock_calls == [
            call.to_have_title(titleOrRegExp="<title>", timeout=None)
        ]


@scenario("[PageAssertions] call async expect that raises error")
async def _():
    with given:
        page = make_page()
        exception = AssertionError("Title mismatch")
        page_assertions = make_method_mock(to_have_title=exception)

        target = "vedro_pw._async_expect.PageAssertionsImpl"

    with when, patch_class(target, page_assertions), catched() as exc_info:
        await expect(page).to_have_title("<title>")

    with then:
        assert page_assertions.mock_calls == [
            call.to_have_title(titleOrRegExp="<title>", timeout=None)
        ]
        assert exc_info.value == exception


@scenario("[PageAssertions] try to call async expect with non-existing method")
async def _():
    with given:
        page = make_page()

    with when, catched() as exc_info:
        await expect(page).non_existing()

    with then:
        assert exc_info.type is AttributeError
        assert str(exc_info.value) == "'PageAssertions' object has no attribute 'non_existing'"


# LocatorAssertions


@scenario("[LocatorAssertions] call async expect")
async def _():
    with given:
        locator = make_locator()
        locator_assertions = make_method_mock(to_have_id=None)

        target = "vedro_pw._async_expect.LocatorAssertionsImpl"

    with when, patch_class(target, locator_assertions):
        await expect(locator).to_have_id("<id>")

    with then:
        assert locator_assertions.mock_calls == [
            call.to_have_id(id="<id>", timeout=None)
        ]


@scenario("[LocatorAssertions] call async expect that raises error")
async def _():
    with given:
        locator = make_locator()
        exception = AssertionError("ID mismatch")
        locator_assertions = make_method_mock(to_have_id=exception)

        target = "vedro_pw._async_expect.LocatorAssertionsImpl"

    with when, patch_class(target, locator_assertions), catched() as exc_info:
        await expect(locator).to_have_id("<id>")

    with then:
        assert locator_assertions.mock_calls == [
            call.to_have_id(id="<id>", timeout=None)
        ]
        assert exc_info.value == exception


@scenario("[LocatorAssertions] try to call async expect with non-existing method")
async def _():
    with given:
        locator = make_locator()

    with when, catched() as exc_info:
        await expect(locator).non_existing()

    with then:
        assert exc_info.type is AttributeError
        assert str(exc_info.value) == "'LocatorAssertions' object has no attribute 'non_existing'"


# APIResponseAssertions

@scenario("[APIResponseAssertions] call async expect")
async def _():
    with given:
        api_response = make_api_response()
        api_response_assertions = make_method_mock(to_be_ok=None)

        target = "vedro_pw._async_expect.APIResponseAssertionsImpl"

    with when, patch_class(target, api_response_assertions):
        await expect(api_response).to_be_ok()

    with then:
        assert api_response_assertions.mock_calls == [
            call.to_be_ok()
        ]


@scenario("[APIResponseAssertions] call async expect that raises error")
async def _():
    with given:
        api_response = make_api_response()
        exception = AssertionError("Response not OK")
        api_response_assertions = make_method_mock(to_be_ok=exception)

        target = "vedro_pw._async_expect.APIResponseAssertionsImpl"

    with when, patch_class(target, api_response_assertions), catched() as exc_info:
        await expect(api_response).to_be_ok()

    with then:
        assert api_response_assertions.mock_calls == [
            call.to_be_ok()
        ]
        assert exc_info.value == exception


@scenario("[APIResponseAssertions] try to call async expect with non-existing method")
async def _():
    with given:
        api_response = make_api_response()

    with when, catched() as exc_info:
        await expect(api_response).non_existing()

    with then:
        assert exc_info.type is AttributeError
        assert str(exc_info.value) == (
            "'APIResponseAssertions' object has no attribute 'non_existing'"
        )
