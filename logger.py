"""
Session logging for the Lecture Summarizer app.
Logs are stored as a JSON array in logs/sessions.json.
"""

import json
import os
import uuid
from datetime import datetime, timezone

_LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
_LOG_FILE = os.path.join(_LOG_DIR, "sessions.json")


def _ensure_log_dir() -> None:
    """Create the logs/ directory if it doesn't exist."""
    os.makedirs(_LOG_DIR, exist_ok=True)


def _read_log() -> list:
    """Read and return all log entries. Returns empty list on error."""
    if not os.path.exists(_LOG_FILE):
        return []
    try:
        with open(_LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _write_log(entries: list) -> None:
    """Atomically write log entries to the JSON file."""
    _ensure_log_dir()
    tmp_path = _LOG_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, _LOG_FILE)


def log_session(
    session_id: str | None = None,
    input_chars: int = 0,
    processing_seconds: float = 0.0,
) -> dict:
    """
    Append a new session entry to logs/sessions.json.

    Args:
        session_id:          UUID string for this session (generated if None).
        input_chars:         Number of characters in the input text.
        processing_seconds:  Wall-clock time taken for summarization.

    Returns:
        The newly created log entry dict.
    """
    entry = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "input_chars": input_chars,
        "processing_seconds": processing_seconds,
        "session_id": session_id or str(uuid.uuid4()),
    }
    entries = _read_log()
    entries.append(entry)
    _write_log(entries)
    return entry


def get_logs() -> list:
    """Return all past log entries, newest first."""
    return list(reversed(_read_log()))
