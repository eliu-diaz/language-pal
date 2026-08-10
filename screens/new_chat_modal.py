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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.dismiss(
                {
                    "voice": self.query_one("#voice", Select).value,
                    "text": self.query_one("#text", Select).value,
                }
            )
        elif event.button.id == "close_modal":
            self.dismiss(None)
