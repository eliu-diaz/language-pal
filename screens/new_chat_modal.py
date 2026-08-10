from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select


class NewChatModal(ModalScreen[dict | None]):
    """Modal screen to set up preferences for a new chat"""

    def compose(self) -> ComposeResult:
        with Container(id="new_chat_dialog"):
            with Horizontal(id="dialog_header"):
                yield Button("x", id="close_modal")

            yield Label("Voice")
            yield Select([("English", 1), ("French", 2)], id="voice")

            yield Label("Translate to:")
            yield Select([("English", 1), ("French", 2)], id="text")

            yield Button("Confirm", variant="primary", id="confirm")

    @on(Button.Pressed, "#close_modal")
    def whatever_method(self):
        self.notify("Wow, you're amazing")
        self.dismiss(None)

    @on(Button.Pressed, "#confirm")
    def whatever_other_method(self):
        self.notify("Wow, you're amazing")
        self.dismiss(
            {
                "voice": self.query_one("#voice", Select).value,
                "text": self.query_one("#text", Select).value,
            }
        )
