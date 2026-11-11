#!/usr/bin/env python3
"""Copy summary.txt (next to this script) into the make.fun output directory."""

import os
import shutil
import sys
from pathlib import Path

SUMMARY_NAME = "summary.txt"
OUTPUT_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


def resolve_output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR


def main():
    script_dir = Path(__file__).resolve().parent
    source = script_dir / SUMMARY_NAME
    target_dir = Path(resolve_output_dir())
    target = target_dir / OUTPUT_NAME

    if not source.is_file():
        print("error: {} not found".format(source), file=sys.stderr)
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print("copied {} -> {}".format(source, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
