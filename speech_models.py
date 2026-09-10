"""Whisper model names and cache checks.

faster-whisper downloads weights from HuggingFace on first use, into
~/.cache/huggingface/hub. The multilingual `small` model is roughly 480 MB, so
on a fresh clone that download happens the first time the user taps the mic —
a long, silent stall behind a spinner. Pre-fetching it with fetch_models.py
moves that cost to setup time, and is_model_cached() lets the UI tell the user
which of the two is about to happen.
"""

from faster_whisper.utils import download_model

# Multilingual, not the `.en` build: passing a `language` other than English to
# an English-only model raises at construction.
MODEL_SIZE = "small"


def is_model_cached(size: str = MODEL_SIZE) -> bool:
    """Reports whether the weights are already on disk, without downloading."""
    try:
        download_model(size, local_files_only=True)
    except Exception:
        return False
    return True


def fetch_model(size: str = MODEL_SIZE) -> str:
    """Downloads the weights if missing and returns the local path."""
    return download_model(size)
