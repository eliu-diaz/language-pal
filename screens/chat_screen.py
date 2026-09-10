from typing import ClassVar

from RealtimeSTT.audio_recorder import AudioToTextRecorder
from textual import on, work
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Log
from textual.worker import Worker, get_current_worker

from logging_setup import cap_realtimestt_log
from speech_models import MODEL_SIZE, is_model_cached

MIC_LABEL = "\U0001f3a4"
# A plain geometric glyph, not an emoji: emoji-presentation squares (U+23F9 +
# VS16) render as a dark box in most terminals. Colour comes from the CSS.
STOP_LABEL = "\u25a0"


class ChatScreen(Screen[None]):
    # init=False: the button already composes with MIC_LABEL, and the watcher
    # would otherwise run before compose() has created it.
    is_listening: reactive[bool] = reactive(False, init=False)

    def __init__(self, selection: dict[str, str]) -> None:
        super().__init__()
        self.selection = selection
        self.recorder: AudioToTextRecorder | None = None
        self.listen_worker: Worker[None] | None = None

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
                yield Button(MIC_LABEL, id="record_voice_button")

        yield Footer()

    def watch_is_listening(self, listening: bool) -> None:
        """Keeps the mic button in sync with the recording state."""
        button = self.query_one("#record_voice_button", Button)
        button.label = STOP_LABEL if listening else MIC_LABEL
        button.set_class(listening, "-listening")

    @on(Button.Pressed, "#record_voice_button")
    async def record_button_pressed(self, event: Button.Pressed) -> None:
        if self.is_listening:
            await self.stop_listening()
        else:
            await self.start_listening()

    async def start_listening(self) -> None:
        chat_container = self.query_one("#main_chat_container", Container)

        # A missing model means a few hundred MB over the network behind that
        # spinner, so say so rather than looking hung.
        if not is_model_cached():
            self.notify(
                f"Downloading the {MODEL_SIZE} speech model (~480 MB). "
                "This happens once; run fetch_models.py to do it up front.",
                title="First run",
                timeout=10,
            )

        chat_container.loading = True
        try:
            await self.build_recorder().wait()
        finally:
            chat_container.loading = False

        self.is_listening = True
        self.listen_worker = self.fetch_user_voice()

    async def stop_listening(self) -> None:
        """Cancels the listen loop, then tears the recorder down for good."""
        self.is_listening = False

        # Cancel first so the loop sees the flag the moment shutdown wakes it.
        if self.listen_worker is not None:
            self.listen_worker.cancel()
            self.listen_worker = None

        button = self.query_one("#record_voice_button", Button)
        button.disabled = True
        try:
            await self.teardown_recorder().wait()
        finally:
            button.disabled = False

    @work(thread=True)
    def teardown_recorder(self) -> None:
        """shutdown() joins child processes, so keep it off the UI thread.

        It also sets the events wait_audio() blocks on, which is what
        releases the listen worker parked inside recorder.text().
        """
        recorder, self.recorder = self.recorder, None
        if recorder is not None:
            recorder.shutdown()

    @work(thread=True, exclusive=True)
    def build_recorder(self) -> None:
        """Blocking model load; runs off the UI thread."""
        self.recorder = AudioToTextRecorder(
            language=self.selection["voice"],
            device="cpu",
            compute_type="int8",
            spinner=False,
            model=MODEL_SIZE,
        )
        # The handler only exists once the recorder has been constructed.
        cap_realtimestt_log()

    def write_log_callback(self, text: str) -> None:
        self.query_one("#user_input_log", Log).write_line(text)

    def on_unmount(self) -> None:
        # When app is terminated or screen is popped, we should shutdown the recorder
        if self.listen_worker is not None:
            self.listen_worker.cancel()
            self.listen_worker = None
        if self.recorder:
            self.recorder.shutdown()
            self.recorder = None

    @work(thread=True, group="listen")
    def fetch_user_voice(self) -> None:
        """Blocking transcription loop; exits when cancelled or torn down."""
        worker = get_current_worker()
        recorder = self.recorder

        while recorder is not None and not worker.is_cancelled:
            text = recorder.text()
            # A shutdown releases text() with nothing useful; don't log that.
            if worker.is_cancelled or not text:
                break
            self.app.call_from_thread(self.write_log_callback, text)

    def action_go_back(self) -> None:
        self.notify("Going back!")
        self.post_message(self.GoBack())
