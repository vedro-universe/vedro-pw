# vedro-pw

[![Codecov](https://img.shields.io/codecov/c/github/vedro-universe/vedro-pw/main.svg?style=flat-square)](https://codecov.io/gh/vedro-universe/vedro-pw)
[![PyPI](https://img.shields.io/pypi/v/vedro-pw.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-pw/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-pw?style=flat-square)](https://pypi.python.org/pypi/vedro-pw/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-pw.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-pw/)

The Playwright Plugin integrates [Playwright](https://playwright.dev/) with [Vedro](https://vedro.io/), enabling automated browser testing with a wide range of configurable options.

## Installation

<details open>
<summary>Quick</summary>
<p>

For a quick installation, you can use a plugin manager as follows:

```shell
$ vedro plugin install vedro-pw
```

</p>
</details>

<details>
<summary>Manual</summary>
<p>

To install manually, follow these steps:

1. Install the package using pip:

```shell
$ pip3 install vedro-pw
```

2. Next, activate the plugin in your `vedro.cfg.py` configuration file:

```python
# ./vedro.cfg.py
import vedro
import vedro_pw


class Config(vedro.Config):
    class Plugins(vedro.Config.Plugins):
        class Playwright(vedro_pw.Playwright):
            enabled = True
```

</p>
</details>

## Usage

### Basic Scenario Example

Here's a simple Vedro scenario that opens the Playwright homepage and verifies the page title.

```python
import vedro
from vedro_pw import opened_browser_page

class Scenario(vedro.Scenario):
    subject = "Open Playwright homepage"

    async def given(self):
        self.page = await opened_browser_page()

    async def when(self):
        await self.page.goto("https://playwright.dev/")

    async def then(self):
        assert await self.page.title() == "Playwright"
```
