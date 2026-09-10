"""Keeps RealtimeSTT's debug log from growing without bound.

RealtimeSTT hardcodes `logging.FileHandler('realtimesst.log')` at DEBUG level
(core/initialization.py) with no rotation, so the file only ever appends. That
is fine in normal use — roughly a hundred lines a minute — but
core/transcription_api.py has a `while recorder.transcribe_count > 0` loop that
logs once per 0.1s poll. If the transcription child process dies without
answering, the count never decrements and that loop spins forever, writing
about a megabyte an hour. Orphaned recorders once left a 10 GB file behind.

Swapping in a RotatingFileHandler puts a hard ceiling on the damage while
keeping the debug trail.
"""

import logging
from logging.handlers import RotatingFileHandler

LOG_FILENAME = "realtimesst.log"
LOGGER_NAME = "realtimestt"
MAX_BYTES = 5_000_000
BACKUP_COUNT = 1


def cap_realtimestt_log() -> None:
    """Replaces RealtimeSTT's unbounded file handler with a rotating one.

    Call after constructing AudioToTextRecorder — the handler does not exist
    until then. Safe to call repeatedly; the swap is idempotent.
    """
    logger = logging.getLogger(LOGGER_NAME)

    for handler in list(logger.handlers):
        if isinstance(handler, RotatingFileHandler):
            return
        if not isinstance(handler, logging.FileHandler):
            continue
        if not handler.baseFilename.endswith(LOG_FILENAME):
            continue

        rotating = RotatingFileHandler(
            handler.baseFilename,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
        )
        rotating.setLevel(handler.level)
        rotating.setFormatter(handler.formatter)

        logger.removeHandler(handler)
        handler.close()
        logger.addHandler(rotating)
        return
