import jj
from jj.mock import Mocked, get_remote_mock_url, mocked
from playwright.async_api import Page
from vedro import defer

from vedro_pw import opened_browser_page

__all__ = ("mocked_html_page", "opened_html_page",)


async def mocked_html_page(*, title: str = "", body: str = "") -> Mocked:
    matcher = jj.match("GET", "/")
    response = jj.Response(
        body=f"""
            <html>
                <title>{title}</title>
                <body>
                    {body}
                </body>
            </html>
        """,
        headers={"content-type": "text/html"}
    )

    mock = await mocked(matcher, response)

    defer(mock.__aexit__, None, None, None)

    return mock


async def opened_html_page(*, title: str = "", body: str = "") -> Page:
    await mocked_html_page(title=title, body=body)

    page = await opened_browser_page()
    await page.goto(get_remote_mock_url())
    return page
