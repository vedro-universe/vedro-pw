# vedro-pw

[![Codecov](https://img.shields.io/codecov/c/github/vedro-universe/vedro-pw/main.svg?style=flat-square)](https://codecov.io/gh/vedro-universe/vedro-pw)
[![PyPI](https://img.shields.io/pypi/v/vedro-pw.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-pw/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-pw?style=flat-square)](https://pypi.python.org/pypi/vedro-pw/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-pw.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-pw/)

The `vedro-pw` plugin allows you to use [Playwright](https://playwright.dev/) within your [Vedro](https://vedro.io/) scenarios for end-to-end testing of web applications.

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

Use the provided context functions in your scenarios to interact with Playwright:

- `launched_browser`: Launches a local or remote browser based on the configuration.
- `created_browser_context`: Creates a new browser context.
- `opened_browser_page`: Opens a new page in the browser context.

### Basic Example

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

## Command-Line Options

The plugin adds several command-line arguments for flexibility:

| Option                 | Description                                                             | Default               |
|------------------------|-------------------------------------------------------------------------|-----------------------|
| `--pw-browser`         | Browser to use (`chromium`, `firefox`, `webkit`)                        | `chromium`            |
| `--pw-headed`          | Run browser in headed mode                                              | `False`               |
| `--pw-slowmo`          | Delay operations by specified milliseconds                              | `0`                   |
| `--pw-remote`          | Connect to a remote browser instance                                    | `False`               |
| `--pw-remote-endpoint` | WebSocket endpoint for remote browser                                   | `ws://localhost:3000` |
| `--pw-screenshots`     | Screenshot capturing (`always`, `on-failure`, `on-reschedule`, `never`) | `never`               |
| `--pw-video`           | Video recording (`always`, `on-failure`, `on-reschedule`, `never`)      | `never`               |
| `--pw-trace`           | Trace recording (`always`, `on-failure`, `on-reschedule`, `never`)      | `never`               |
| `--pw-device`          | Emulate a specific device                                               | `None`                |

### Example Usage

```shell
$ vedro run --pw-browser=firefox --pw-headed --pw-screenshots=on-failure --save-artifacts
```

### Capture Modes

`CaptureMode` determines when to capture artifacts:

- `never`: Do not capture.
- `on-failure`: Capture only when a scenario fails.
- `on-reschedule`: Capture when a scenario is rescheduled.
- `always`: Always capture.

Artifacts like screenshots, videos, and traces are attached to the scenario results and can be used in reports.
