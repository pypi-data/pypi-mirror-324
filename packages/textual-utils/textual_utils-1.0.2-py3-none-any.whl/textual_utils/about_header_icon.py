from textual.app import App
from textual.events import Click
from textual.widgets import Header
from textual.widgets._header import HeaderIcon

from textual_utils.app_metadata import AppMetadata
from textual_utils.screens import AboutScreen


class AboutHeaderIcon(HeaderIcon):
    def __init__(self, icon: str, app_metadata: AppMetadata) -> None:
        super().__init__()

        self.icon = icon
        self.app_metadata = app_metadata

    async def on_click(self, _event: Click) -> None:
        self.app.push_screen(AboutScreen(self.app_metadata))


async def mount_about_header_icon(
    current_app: App,
    icon: str,
    app_metadata: AppMetadata,
) -> None:
    header_icon = current_app.query_one(HeaderIcon)
    header_icon.remove()

    header = current_app.query_one(Header)
    about_header_icon = AboutHeaderIcon(icon, app_metadata)
    await header.mount(about_header_icon)
