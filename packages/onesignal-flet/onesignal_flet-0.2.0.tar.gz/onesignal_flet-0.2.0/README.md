# Flet OneSignal

---

## Description

Flutter OneSignal package integration for Python Flet

[Flet OneSignal](https://pub.dev/packages?q=flet_onesignal) in the official package repository for Dart and Flutter apps.

---

## Installation

**Using POETRY**

```console
$ poetry add onesignal-flet
```

**Using PIP**

```console
$ pip install onesignal-flet
```

---

## Example configuration in the `pyproject.toml` file.

[More in ](https://flet.dev/blog/pyproject-toml-support-for-flet-build-command/) Support for flet build command.

```toml
[tool.poetry]
name = "example-flet-app"
version = "0.1.0"
description = ""
authors = ["brunobrown <brunobrown.86@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"
flet = "^0.25.2"
onesignal_flet = {git = "https://github.com/brunobrown/onesignal-flet.git", rev = "main"}

[tool.flet.flutter.dependencies]
flet_onesignal = "^0.0.1"
# OR ABSOLUTE PATH TO FLUTTER/FLET INTEGRATION PACKAGE. EXAMPLE:
#flet_onesignal.path = "/home/<user>/path/to/package/flet_onesignal"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


```

### Example of in-app usage

```Python
import flet as ft
from onesignal_flet.control import OneSignal

ONESIGNAL_APP_ID = ''   # https://onesignal.com     <---


def main(page: ft.Page):
    one_signal = OneSignal(app_id=ONESIGNAL_APP_ID)

    title = ft.Text(
        value='OneSignal - Test',
        size=20,
    )

    message = ft.Text(
        value='Push notification message here',
        size=20,
    )

    container = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                title,
                ft.Container(
                    width=page.width * 0.3,
                    content=ft.Divider(color=ft.Colors.BLACK),
                ),
                message
            ]
        )
    )

    page.add(
        one_signal,
        container
    )


if __name__ == "__main__":
    ft.app(target=main)

```
