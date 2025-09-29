from vedro import scenario, then, when

from vedro_pw import expect, opened_browser_page


@scenario("open browser page")
async def _():
    with when:
        page = await opened_browser_page()

    with then:
        assert await expect(page).to_have_url("about:blank")
