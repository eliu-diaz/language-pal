
from textual.containers import VerticalScroll
from textual.widgets import Label, ListItem, ListView
from textual.app import ComposeResult

class RecentChats(VerticalScroll):
    """My Recent Chats Class"""

    def compose(self) -> ComposeResult:
        # Should be rendering a list of chats
        titleLabel = Label("Welcome to Language Pal!!", id="title_label")
        titleLabel.border_subtitle = "Select or start a new chat"

        yield titleLabel
        yield ListView(
            ListItem(Label("The quick brown fox jumps over the lazy dog.")),
            ListItem(Label("The quick brown fox jumps over the lazy dog.")),
            ListItem(Label("The quick brown fox jumps over the lazy dog."))
        )

