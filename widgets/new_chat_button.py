from textual.message import Message
from textual.widgets import Button


class NewChatButton(Button):
    """Main button that starts a chat on the Language Pal App"""

    class Selected(Message):
        """Selected event"""

    def __init__(self):
        super().__init__("+ New chat", variant="primary", id="new_chat_button")

    def on_button_pressed(self, event: Button.Pressed):
        """Cmon do something"""
        event.stop()
        self.post_message(self.Selected())
