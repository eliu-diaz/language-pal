from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from models.recent_chat import RecentChat
from palette import INK_WASH_DARK, INK_WASH_LIGHT
from recent_chats import RecentChats
from screens.new_chat_modal import NewChatModal
from widgets.new_chat_button import NewChatButton


class LanguagePalApp(App):
    """A Textual app to help with verbal language practice"""

    CSS_PATH = ["styles/recent_chats.tcss", "styles/new_chat_modal.tcss"]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    recent_chats: list[RecentChat] = list()

    def __init__(self):
        super().__init__()
        self.register_theme(INK_WASH_LIGHT)
        self.register_theme(INK_WASH_DARK)
        self.theme = "ink-wash-dark"

    def compose(self) -> ComposeResult:
        yield Header()
        yield RecentChats(self.recent_chats)
        yield NewChatButton()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "ink-wash-dark" if self.theme == "ink-wash-light" else "ink-wash-light"
        )

    def on_new_chat_button_selected(self, message: NewChatButton.Selected) -> None:
        def handle_new_chat_modal_closure(selection: dict | None) -> None:
            self.notify(f"Data selected was: {selection}")

        self.push_screen(NewChatModal(), handle_new_chat_modal_closure)


if __name__ == "__main__":
    app = LanguagePalApp()
    app.run()
