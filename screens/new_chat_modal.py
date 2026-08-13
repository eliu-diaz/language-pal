from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select


class NewChatModal(ModalScreen[dict | None]):
    """Modal screen to set up preferences for a new chat"""

    LANGUAGES: ClassVar[list[tuple[str, str]]] = [
        ("English", "en"),
        ("French", "fr"),
        ("Spanish", "es"),
    ]

    voice_languages = LANGUAGES.copy()
    text_languages = LANGUAGES.copy()

    def compose(self) -> ComposeResult:
        with Container(id="new_chat_dialog"):
            with Horizontal(id="dialog_header"):
                yield Button("x", id="close_modal")

            yield Label("Voice")
            yield Select(self.voice_languages, id="voice")
            yield Label("Translate to:")
            yield Select(self.text_languages, id="text")

            yield Button("Confirm", variant="primary", id="confirm")

    @on(Button.Pressed, "#close_modal")
    def whatever_method(self):
        self.dismiss(None)

    @on(Button.Pressed, "#confirm")
    def whatever_other_method(self):
        voice_selection = self.query_one("#voice", Select).value
        text_selection = self.query_one("#text", Select).value
        if voice_selection == Select.NULL or text_selection == Select.NULL:
            self.notify("Pick a language for both fields", severity="warning")
            return

        if voice_selection == text_selection:
            self.notify("Please pick two different languages.", severity="warning")
            return

        self.dismiss(
            {
                "voice": self.query_one("#voice", Select).value,
                "text": self.query_one("#text", Select).value,
            }
        )
