#!/usr/bin/env python3
"""Publish the 11 November 2026 world-news summary as this entry's artifact.

The make.fun news-summary-01 grader reads a single file, entry.txt, from the
directory named by MAKEFUN_OUTPUT_DIR (falling back to /output).  This program
copies the hand-written summary that sits beside it into that directory after
checking it satisfies the contest's size rules, so a bad edit can never ship.
"""

import os
import shutil
import sys
from pathlib import Path

SUMMARY_FILE = "summary.txt"
ENTRY_FILE = "entry.txt"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
OUTPUT_FALLBACK = "/output"

MIN_CHARS = 1
MAX_CHARS = 2000


def load_summary(path: Path) -> str:
    """Read summary.txt, refusing to continue when it cannot be used."""
    if not path.exists():
        sys.exit(
            "error: {} not found in {}; the entry needs its summary file".format(
                SUMMARY_FILE, path.parent
            )
        )
    if not path.is_file():
        sys.exit("error: {} is not a regular file".format(path))

    raw = path.read_bytes()
    if not raw.strip():
        sys.exit(
            "error: {} holds no non-whitespace text; the gate scores that as no entry".format(
                path
            )
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        sys.exit(
            "error: {} is not valid UTF-8 ({}); save it as UTF-8 and retry".format(
                path, exc
            )
        )
    return text


def check_length(text: str, path: Path) -> None:
    """Refuse any summary the sealed gate would reject for size."""
    length = len(text)
    if length < MIN_CHARS:
        sys.exit("error: {} is empty; write the summary first".format(path))
    if length > MAX_CHARS:
        sys.exit(
            "error: {} is {} characters, {} over the {} character cap; "
            "drop a story rather than truncating".format(
                path, length, length - MAX_CHARS, MAX_CHARS
            )
        )


def publish(text: str, destination: Path) -> None:
    """Write the summary bytes to destination, creating the folder if needed."""
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(text.encode("utf-8"))
    except OSError as exc:
        sys.exit("error: cannot write {}: {}".format(destination, exc))


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SUMMARY_FILE
    target = Path(os.environ.get(OUTPUT_ENV_VAR) or OUTPUT_FALLBACK) / ENTRY_FILE

    if not os.access(here, os.R_OK):
        sys.exit("error: {} is not readable".format(here))

    text = load_summary(source)
    check_length(text, source)
    publish(text, target)

    # A stale entry.txt from an earlier run must not be mistaken for this one.
    if target.read_bytes() != text.encode("utf-8"):
        sys.exit("error: {} does not match {} after writing".format(target, source))

    print(
        "wrote {} ({} characters, {} bytes) from {}".format(
            target, len(text), target.stat().st_size, source
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
