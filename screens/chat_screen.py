from typing import ClassVar

from RealtimeSTT.audio_recorder import AudioToTextRecorder
from textual import on, work
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.containers import Container
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Log


class ChatScreen(Screen[None]):
    def __init__(self, selection: dict[str, str]) -> None:
        super().__init__()
        self.selection = selection
        self.recorder: AudioToTextRecorder | None = None

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
    async def record_button_pressed(self, event: Button.Pressed) -> None:
        chat_container = self.query_one("#main_chat_container", Container)

        if self.recorder is None:
            chat_container.loading = True
            try:
                await self.build_recorder().wait()
                self.fetch_user_voice()
            finally:
                chat_container.loading = False

    @work(thread=True, exclusive=True)
    def build_recorder(self) -> None:
        """Blocking model load; runs off the UI thread."""
        self.recorder = AudioToTextRecorder(
            language=self.selection["voice"],
            device="cpu",
            compute_type="int8",
            spinner=False,
            model="small",
        )

    def write_log_callback(self, text: str) -> None:
        self.query_one("#user_input_log", Log).write_line(text)

    def on_unmount(self) -> None:
        # When app is terminated or screen is popped, we should shutdown the recorder
        if self.recorder:
            self.recorder.shutdown()

    @work(thread=True)
    def fetch_user_voice(self) -> None:
        while True:
            self.recorder.text(self.write_log_callback)

    def action_go_back(self) -> None:
        self.notify("Going back!")
        self.post_message(self.GoBack())
