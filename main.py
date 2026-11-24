#!/usr/bin/env python3
"""Copy the pre-drawn 24 November 2026 news image to the output directory.

The image (entry.png, 1024x1024) sits next to this script in the repo. This
program only copies it: it checks the PNG magic bytes, enforces the 1 MiB
size cap, and writes the exact same bytes to $MAKEFUN_OUTPUT_DIR/entry.png
every run, so the two grader runs are byte-identical. No network, no
randomness, no environment reads beyond the output directory variable.
"""
import hashlib
import os
import sys

MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        fail("entry.png not found next to main.py")

    with open(source, "rb") as fh:
        data = fh.read()

    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if not data.startswith(PNG_MAGIC):
        fail("entry.png does not start with the PNG magic bytes")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
