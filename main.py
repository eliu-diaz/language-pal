from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from palette import INK_WASH_DARK, INK_WASH_LIGHT
from recent_chats import RecentChats
from widgets.new_chat_button import NewChatButton


class LanguagePalApp(App):
    """A Textual app to help with verbal language practice"""

    CSS_PATH = ["styles/recent_chats.tcss"]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.register_theme(INK_WASH_LIGHT)
        self.register_theme(INK_WASH_DARK)
        self.theme = "ink-wash-dark"

    def compose(self) -> ComposeResult:
        yield Header()
        yield RecentChats()
        yield NewChatButton()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "ink-wash-dark" if self.theme == "ink-wash-light" else "ink-wash-light"
        )


if __name__ == "__main__":
    app = LanguagePalApp()
    app.run()
