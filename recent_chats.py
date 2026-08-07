from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, ListItem, ListView

from models.recent_chat import RecentChat


class RecentChats(VerticalScroll):
    """My Recent Chats Class"""

    def __init__(self, recent_chats: list[RecentChat]):
        super().__init__()
        self.recent_chats = recent_chats

    def compose(self) -> ComposeResult:
        # Should be rendering a list of chats
        titleLabel = Label("Welcome to Language Pal!!", id="title_label")
        titleLabel.border_subtitle = "Select or start a new chat"

        yield titleLabel

        if self.recent_chats:
            yield ListView(
                ListItem(Label("The quick brown fox jumps over the lazy dog.")),
                ListItem(Label("The quick brown fox jumps over the lazy dog.")),
                ListItem(Label("The quick brown fox jumps over the lazy dog.")),
            )
        else:
            label = Label(
                "No chats to display, tap on the 'New Chat' button to get started.",
                id="no-chats-label",
            )
            yield label
