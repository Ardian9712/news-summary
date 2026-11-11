#!/usr/bin/env python3
"""Copy summary.txt (next to this script) into the make.fun output directory.

Entry: news-summary-01 -- best summary of 11 November 2026 world news.
The graded artifact is entry.txt in MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import shutil
import sys
from pathlib import Path

SUMMARY_NAME = "summary.txt"
OUTPUT_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
MAX_CHARS = 2000


def main():
    script_dir = Path(__file__).resolve().parent
    source = script_dir / SUMMARY_NAME
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR)
    target = output_dir / OUTPUT_NAME

    if not source.is_file():
        print(
            "error: {} is missing next to {}".format(SUMMARY_NAME, script_dir),
            file=sys.stderr,
        )
        print(
            "hint: keep summary.txt beside main.py in the entry folder",
            file=sys.stderr,
        )
        return 1

    # Guard: never publish an empty summary, which would score as no entry.
    if source.stat().st_size == 0:
        print(
            "error: {} is empty; add the 11 November 2026 summary".format(source),
            file=sys.stderr,
        )
        return 1

    # Guard: never publish an over-long summary, which breaks the entry limit.
    text = source.read_text(encoding="utf-8")
    if len(text) > MAX_CHARS:
        print(
            "error: {} is {} characters, over the {} limit".format(
                source, len(text), MAX_CHARS
            ),
            file=sys.stderr,
        )
        print("hint: trim stories until the summary fits", file=sys.stderr)
        return 1

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    except OSError as exc:
        print("error: could not write {}: {}".format(target, exc), file=sys.stderr)
        return 1

    print(
        "copied {} -> {} ({} characters, {} bytes)".format(
            source, target, len(text), target.stat().st_size
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
