import asyncio
from typing import ClassVar

from textual import on, work
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.containers import Container
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Log


class ChatScreen(Screen[None]):
    class GoBack(Message):
        """Used to send a go_back message to main.py"""

    BINDINGS: ClassVar[list[BindingType]] = [("ctrl+b", "go_back", "Go back")]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="main_chat_container"):
            with Container(id="voice_field"):
                yield Label("User Input")
                yield Log(id="user_input_log")

            with Container(id="translation_field"):
                yield Label("Translation")
                yield Log(id="translation_log")

            with Container(id="record_row"):
                yield Button("\U0001f3a4", id="record_voice_button")

        yield Footer()

    @on(Button.Pressed, "#record_voice_button")
    def record_button_pressed(self, event: Button.Pressed):
        pass  # TODO: When ready to start speech-to-text

    def on_mount(self) -> None:
        self.notify("On ready finished!")
        self.fetch_user_voice()

    @work
    async def fetch_user_voice(self) -> None:
        log = self.query_one("#user_input_log", Log)
        log.write_line("Starting voice recognition...")

        while True:
            await asyncio.sleep(3)
            log.write_line("3 seconds later! UI Stayed responsive!")

    def action_go_back(self) -> None:
        self.notify("Going back!")
        self.post_message(self.GoBack())
