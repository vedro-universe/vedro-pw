from contextlib import asynccontextmanager
from typing import AsyncIterator

import jj
from jj.mock import Mocked, mocked
from vedro import given, scenario, then, when

from vedro_pw import expect, opened_browser_page


@asynccontextmanager
async def mocked_response(title: str, *, wait_for_requests: int = 1) -> AsyncIterator[Mocked]:
    matcher = jj.match("*")
    response = jj.Response(
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

    async with mocked(matcher, response) as mock:
        mock: Mocked
        yield mock
        await mock.wait_for_requests(wait_for_requests)


@scenario("open real page")
async def _():
    with given:
        page = await opened_browser_page()

        url = "http://localhost:8080/"
        title = "<title>"

    async with when, mocked_response(title) as mock:
        await page.goto(url)

    with then:
        assert await expect(page).to_have_url(url)
        assert await expect(page).to_have_title(title)

        assert len(mock.history) == 1
