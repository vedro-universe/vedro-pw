from vedro import catched, given, scenario, then, when

from vedro_pw import expect

from .._utils import opened_html_page

# PageAssertions


@scenario("[PageAssertions] call async expect")
async def _():
    with given:
        title = "<title>"
        page = await opened_html_page(title=title)

    with when:
        res = await expect(page).to_have_title(title)

    with then:
        assert res is True


@scenario("[PageAssertions] call async expect that raises error")
async def _():
    with given:
        page = await opened_html_page(title="Actual Title")

    with when, catched() as exc_info:
        await expect(page).to_have_title("Wrong Title", timeout=1000)

    with then:
        assert exc_info.type is AssertionError


@scenario("[PageAssertions] try to call async expect with non-existing method")
async def _():
    with given:
        page = await opened_html_page(title="Test Page")

    with when, catched() as exc_info:
        await expect(page).non_existing()

    with then:
        assert exc_info.type is AttributeError
        assert str(exc_info.value) == "'PageAssertions' object has no attribute 'non_existing'"


# LocatorAssertions


@scenario("[LocatorAssertions] call async expect")
async def _():
    with given:
        element_id = "test-id"
        page = await opened_html_page(body=f'<div id="{element_id}">Test Element</div>')
        locator = page.locator(f"#{element_id}")

    with when:
        res = await expect(locator).to_have_id(element_id)

    with then:
        assert res is True


@scenario("[LocatorAssertions] call async expect that raises error")
async def _():
    with given:
        page = await opened_html_page(body='<div id="actual-id">Test Element</div>')
        locator = page.locator("#actual-id")

    with when, catched() as exc_info:
        await expect(locator).to_have_id("wrong-id", timeout=1000)

    with then:
        assert exc_info.type is AssertionError


@scenario("[LocatorAssertions] try to call async expect with non-existing method")
async def _():
    with given:
        page = await opened_html_page(body='<div>Test Element</div>')
        locator = page.locator("div")

    with when, catched() as exc_info:
        await expect(locator).non_existing()

    with then:
        assert exc_info.type is AttributeError
        assert str(exc_info.value) == "'LocatorAssertions' object has no attribute 'non_existing'"


# APIResponseAssertions

@scenario("[APIResponseAssertions] call async expect")
async def _():
    with given:
        page = await opened_html_page(title="Test")
        api_response = await page.request.get(page.url)

    with when:
        res = await expect(api_response).to_be_ok()

    with then:
        assert res is True


@scenario("[APIResponseAssertions] call async expect that raises error")
async def _():
    with given:
        page = await opened_html_page(title="Test")
        api_response = await page.request.get(page.url + "/non-existent-endpoint-404")

    with when, catched() as exc_info:
        await expect(api_response).to_be_ok()

    with then:
        assert exc_info.type is AssertionError


@scenario("[APIResponseAssertions] try to call async expect with non-existing method")
async def _():
    with given:
        page = await opened_html_page(title="Test")
        api_response = await page.request.get(page.url)

    with when, catched() as exc_info:
        await expect(api_response).non_existing()

    with then:
        assert exc_info.type is AttributeError
        assert str(exc_info.value) == (
            "'APIResponseAssertions' object has no attribute 'non_existing'"
        )
