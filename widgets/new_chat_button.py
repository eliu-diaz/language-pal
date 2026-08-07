from textual.widgets import Button
from textual.app import ComposeResult

class NewChatButton(Button):
    def __init__(self):
        super().__init__("+ New chat", variant="primary", id="new_chat_button")
