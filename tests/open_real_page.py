from jj.mock import get_remote_mock_url
from vedro import given, scenario, then, when

from vedro_pw import expect, opened_browser_page

from ._utils import mocked_html_page


@scenario("open real page")
async def _():
    with given:
        page = await opened_browser_page()

        url = get_remote_mock_url()
        title = "<title>"

        mock = await mocked_html_page(title=title)

    with when:
        await page.goto(url)

    with then:
        assert await expect(page).to_have_url(f"{url}/")
        assert await expect(page).to_have_title(title)

        history = await mock.fetch_history()
        assert len(history) == 1
