#!/usr/bin/env python3
"""One-image news digest — make.fun entry for news-image-20261119.

"What happened in the world on Thursday, 19 November 2026?" — this
program answers with a single picture: assets/entry.png, a 1024x1024
newspaper-style poster with the day's lead story (the first-ever
Xi–Trump–Putin trilateral summit in Shenzhen), a GTA VI launch-day
feature, twelve news cards, a UTC timeline of the day and an "also
today" strip, compiled from that day's reporting by Reuters, AP,
BBC, Yonhap, Nikkei Asia, Al Jazeera, Le Monde, WSJ and The Hindu.

The poster itself is rendered by tools/build_image.py (kept in this
repository so the picture can be rebuilt and audited) and stored
base64-encoded in assets/entry.png.b64, so the repository stays plain
text end to end. This entrypoint is the program the grader runs: it
decodes the poster, validates it against the bounty's limits (a whole
PNG, at most 1 MiB, at most 1024x1024) and writes it, byte for byte,
to the output directory — /output by default, or $MAKEFUN_OUTPUT_DIR
when set. It uses only the Python standard library, touches no
network, and writes identical bytes on every run.
"""

import base64
import hashlib
import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576  # 1 MiB
MAX_DIM = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB\x60\x82"  # the final chunk of every whole PNG

ROOT = Path(__file__).resolve().parent
ASSET = ROOT / "assets" / "entry.png.b64"


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Read (width, height) from a PNG's IHDR chunk."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("asset is not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("asset has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def validate(data: bytes) -> None:
    if len(data) > MAX_BYTES:
        raise ValueError(f"poster is {len(data)} bytes; the limit is {MAX_BYTES}")
    if not data.endswith(PNG_IEND):
        raise ValueError("poster does not end with the PNG IEND chunk; it is truncated")
    width, height = png_dimensions(data)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"poster is {width}x{height}; the limit is {MAX_DIM}x{MAX_DIM}")


def main() -> int:
    if not ASSET.is_file():
        print(f"error: missing poster asset at {ASSET}", file=sys.stderr)
        return 1
    try:
        data = base64.b64decode(ASSET.read_text(encoding="ascii").strip(), validate=True)
    except (ValueError, UnicodeDecodeError) as exc:
        print(f"error: poster asset is not valid base64: {exc}", file=sys.stderr)
        return 1
    try:
        validate(data)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    with target.open("wb") as fh:
        fh.write(data)

    written = target.read_bytes()
    if written != data:
        print("error: written file differs from the asset", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()[:16]
    width, height = png_dimensions(written)
    print(f"Wrote {target} ({len(written)} bytes, {width}x{height}, sha256 {digest}…)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
