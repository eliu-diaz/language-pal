from pathlib import PurePath
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.widgets import Footer, Header

from models.recent_chat import RecentChat
from palette import INK_WASH_DARK, INK_WASH_LIGHT
from recent_chats import RecentChats
from screens.chat_screen import ChatScreen
from screens.new_chat_modal import NewChatModal
from widgets.new_chat_button import NewChatButton


class LanguagePalApp(App):
    """A Textual app to help with verbal language practice"""

    CSS_PATH: ClassVar[list[str | PurePath]] = [
        "styles/recent_chats.tcss",
        "styles/new_chat_modal.tcss",
        "styles/chat_screen.tcss",
    ]
    BINDINGS: ClassVar[list[BindingType]] = [("d", "toggle_dark", "Toggle dark mode")]
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

    def on_chat_screen_go_back(self, message: ChatScreen.GoBack) -> None:
        self.pop_screen()

    def on_new_chat_button_selected(self, message: NewChatButton.Selected) -> None:
        self.push_screen(NewChatModal(), self.handle_new_chat_modal_closure)

    def handle_new_chat_modal_closure(self, selection: dict | None) -> None:
        if selection:
            self.push_screen(ChatScreen())

    def handle_chat_closure(self) -> None:
        self.pop_screen()


if __name__ == "__main__":
    app = LanguagePalApp()
    app.run()
