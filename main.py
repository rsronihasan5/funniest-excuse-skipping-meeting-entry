"""Funniest Excuse for Skipping a Meeting — make.fun entry.

Writes one razor-sharp excuse line to /output/entry.txt (or $OUTPUT_DIR).
Standard library only. Never removes the output directory itself: it only
clears the directory's contents before writing.
"""

import os
import shutil
import sys

ENTRY = (
    "I read last Tuesday's minutes: 47 minutes, zero decisions, "
    "and the only action item went to Dave, who left in March. "
    "I'm skipping the sequel."
)

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Gate: 1-200 chars, not only whitespace, single line, no control chars."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry is %d chars, outside the %d-%d gate"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    return True


def clean_output_dir(path):
    """Remove only the *contents* of path. The directory itself is never removed."""
    os.makedirs(path, exist_ok=True)
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.islink(target) or os.path.isfile(target):
            os.unlink(target)
        elif os.path.isdir(target):
            shutil.rmtree(target)


def main():
    validate(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    clean_output_dir(out_dir)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(ENTRY)
    with open(out_path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != ENTRY:
        raise ValueError("read-back mismatch: written file differs from ENTRY")
    if os.path.getsize(out_path) != len(ENTRY.encode("utf-8")):
        raise ValueError("read-back mismatch: byte size differs from ENTRY")
    validate(written)
    print("wrote %s (%d chars)" % (out_path, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
