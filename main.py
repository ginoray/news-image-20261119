#!/usr/bin/env python3
"""Entry program for the news-image-20261119 make.fun bounty.

The question the bounty asks — sum up the world news of Thursday,
19 November 2026 in one image — is answered by assets/entry.png: a
1024x1024 newspaper poster whose lead story is the first-ever
Xi–Trump–Putin trilateral summit in Shenzhen, with a GTA VI
launch-day feature, twelve short news cards, a UTC timeline of the
day and an also-today strip. The reporting behind it comes from
Reuters, AP, BBC, Yonhap, Nikkei Asia, Al Jazeera, Le Monde, WSJ
and The Hindu, each story checked against at least two of them.

The poster travels inside this repository as base64 text in
assets/entry.png.b64 (rendered by tools/build_image.py), which
keeps every file in the repo readable plain text. This program
decodes it, proves the result is a whole PNG inside the bounty's
limits — at most 1 MiB, at most 1024x1024, every chunk present
with a matching checksum, IEND last — and writes those exact
bytes to the output directory: /output, or $MAKEFUN_OUTPUT_DIR
when that is set. Standard library only, no network, and the
same bytes come out on every run.
"""

import base64
import binascii
import hashlib
import os
import struct
import sys
from pathlib import Path

LIMIT_BYTES = 1_048_576
LIMIT_SIDE = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"

HERE = Path(__file__).resolve().parent
ASSET_FILE = HERE / "assets" / "entry.png.b64"


def iter_chunks(data):
    """Yield (chunk_type, payload) while walking a PNG byte string.

    Raises ValueError on any structural problem: a short read, a
    chunk whose stored CRC does not match its contents, or trailing
    bytes after the final chunk.
    """
    pos = len(SIGNATURE)
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length
        if end + 4 > len(data):
            raise ValueError(f"truncated {ctype!r} chunk")
        payload = data[pos + 8:end]
        (stored_crc,) = struct.unpack(">I", data[end:end + 4])
        if binascii.crc32(ctype + payload) & 0xFFFFFFFF != stored_crc:
            raise ValueError(f"checksum mismatch in {ctype!r} chunk")
        yield ctype, payload
        pos = end + 4
    if pos != len(data):
        raise ValueError("extra bytes after the last chunk")


def inspect_png(data):
    """Return (width, height) of a whole PNG, or raise ValueError."""
    if data[:8] != SIGNATURE:
        raise ValueError("not a PNG file (bad signature)")
    kinds = []
    dims = None
    for ctype, payload in iter_chunks(data):
        kinds.append(ctype)
        if ctype == b"IHDR":
            dims = struct.unpack(">II", payload[:8])
    if not kinds or kinds[0] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    if kinds[-1] != b"IEND":
        raise ValueError("last chunk is not IEND; the image is truncated")
    return dims


def load_asset():
    """Decode the shipped base64 poster back into PNG bytes."""
    if not ASSET_FILE.is_file():
        raise ValueError(f"poster asset is missing: {ASSET_FILE}")
    text = ASSET_FILE.read_text(encoding="ascii").strip()
    try:
        return base64.b64decode(text, validate=True)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"poster asset is not valid base64: {exc}") from exc


def run():
    try:
        png = load_asset()
        width, height = inspect_png(png)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if len(png) > LIMIT_BYTES:
        print(f"error: poster is {len(png)} bytes; the limit is {LIMIT_BYTES}",
              file=sys.stderr)
        return 1
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        print(f"error: poster is {width}x{height}; the limit is "
              f"{LIMIT_SIDE}x{LIMIT_SIDE}", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(png)

    landed = target.read_bytes()
    if landed != png:
        print("error: the written file differs from the poster asset",
              file=sys.stderr)
        return 1
    try:
        inspect_png(landed)
    except ValueError as exc:
        print(f"error: the written file failed re-inspection: {exc}",
              file=sys.stderr)
        return 1
    digest = hashlib.sha256(png).hexdigest()[:16]
    print(f"Wrote {target} ({len(png)} bytes, {width}x{height}, sha256 {digest}…)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
