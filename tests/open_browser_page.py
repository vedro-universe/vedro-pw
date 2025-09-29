import jj
from jj.mock import Mocked, mocked
from vedro import given, scenario, then, when

from vedro_pw import expect, opened_browser_page


@scenario("open blank page")
async def _():
    with when:
        page = await opened_browser_page()

    with then:
        assert await expect(page).to_have_url("about:blank")


def mocked_response(title: str) -> Mocked:
    return mocked(
        matcher=jj.match("*"),
        response=jj.Response(
            body=f"""
                <html>
                    <title>{title}</title>
                    <body>
                        <h1>Hello, World!</h1>
                    </body>
                </html>
            """,
            headers={"content-type": "text/html"}
        )
    )


@scenario("open real page")
async def _():
    with given:
        page = await opened_browser_page()

        title = "<title>"

    async with when, mocked_response(title) as mock:
        await page.goto("http://localhost:8080")
        await mock.wait_for_requests(1)

    with then:
        assert await expect(page).to_have_url("http://localhost:8080/")
        assert await expect(page).to_have_title(title)
