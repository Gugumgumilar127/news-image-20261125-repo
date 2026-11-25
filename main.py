#!/usr/bin/env python3
"""news-image-20261125 entry: deliver the day's-news image.

The repository ships the finished front-page image as the asset
``entry.png`` (JPEG bytes under a .png name, which the competition
allows: the file is identified by its first bytes). The grader runs
this program with the repository mounted READ-ONLY
(``python3 -P -s /bot/main.py``), so this program never renders and
never writes next to itself: it only copies the shipped asset to
``MAKEFUN_OUTPUT_DIR`` (default ``/output``) and verifies the copy.

Standard library only; no sibling modules are imported, so the run
works under ``-P -s`` with no writable repo and no network. Before
the copy is accepted it is verified: JPEG magic bytes FF D8, the
trailing end-of-image marker FF D9, size at most 1 MiB, and a copy
whose size equals the shipped asset's.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1024 * 1024


def jpeg_dimensions(data):
    """Return (width, height) parsed from a JPEG byte string.

    Walk the marker segments that follow the SOI marker, using
    each segment's own length field to hop to the next one, until
    a Start Of Frame segment (SOF0 0xC0 or SOF2 0xC2) is found.
    That segment carries precision, height and width. Standalone
    markers such as RSTn, TEM, SOI and EOI carry no length field,
    and extra 0xFF bytes before a marker are padding to skip.
    Raise IOError when no frame header can be located.
    """
    if len(data) < 2 or data[:2] != b"\xff\xd8":
        raise IOError("not a JPEG: missing start-of-image marker")
    pos = 2
    total = len(data)
    while pos < total:
        if data[pos] != 0xFF:
            raise IOError("corrupt JPEG: expected marker prefix")
        while pos < total and data[pos] == 0xFF:
            pos += 1
        if pos >= total:
            break
        marker = data[pos]
        pos += 1
        if marker == 0x00:
            continue
        if marker == 0x01 or 0xD0 <= marker <= 0xD9:
            if marker == 0xD9:
                break
            continue
        if pos + 2 > total:
            raise IOError("corrupt JPEG: truncated segment header")
        seg_len = (data[pos] << 8) | data[pos + 1]
        if seg_len < 2 or pos + seg_len > total:
            raise IOError("corrupt JPEG: invalid segment length")
        if marker in (0xC0, 0xC2):
            if seg_len < 7:
                raise IOError("corrupt JPEG: frame segment too short")
            height = (data[pos + 3] << 8) | data[pos + 4]
            width = (data[pos + 5] << 8) | data[pos + 6]
            if width <= 0 or height <= 0:
                raise IOError("corrupt JPEG: invalid frame dimensions")
            return (width, height)
        pos += seg_len
    raise IOError("corrupt JPEG: no start-of-frame segment found")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    asset = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(asset, target)

    with open(asset, "rb") as fh:
        asset_data = fh.read()
    with open(target, "rb") as fh:
        data = fh.read()

    # The copy must be the asset's bytes: a size mismatch means a
    # truncated copy, so fail loudly instead of submitting it.
    if len(data) != len(asset_data):
        raise IOError("copied image size differs from the shipped asset")
    # Equal size is not proof of an identical copy: compare the
    # SHA-256 digest of the copy against the shipped asset's, so a
    # same-size but altered copy also fails loudly here.
    asset_digest = hashlib.sha256(asset_data).hexdigest()
    copy_digest = hashlib.sha256(data).hexdigest()
    if copy_digest != asset_digest:
        raise IOError("copied image hash differs from the shipped asset")
    # Enforce the 1 MiB size cap: an oversized image would be
    # rejected, so fail loudly here instead of submitting it.
    if len(data) > MAX_BYTES:
        raise IOError("copied image exceeds the 1 MiB size limit")
    # Verify the copy really is a JPEG: a genuine JPEG starts with
    # the magic bytes 0xFF 0xD8 (start of image) ...
    if data[:2] != b"\xff\xd8":
        raise IOError("copied image is not a JPEG: wrong magic bytes")
    # ... and ends with the end-of-image marker 0xFF 0xD9; a
    # truncated copy still starts correctly but lacks this marker.
    if len(data) < 2 or data[-2:] != b"\xff\xd9":
        raise IOError(
            "copied image is not a complete JPEG: "
            "missing end-of-image marker"
        )
    # The front-page image is square by design: parse the frame
    # header from the copied bytes and require exactly 1024x1024,
    # so a wrong-sized or header-corrupt asset fails here too.
    width, height = jpeg_dimensions(data)
    if (width, height) != (1024, 1024):
        raise IOError(
            "copied image has wrong dimensions: "
            "expected 1024x1024, got %dx%d" % (width, height)
        )

    print("entry.png: %d bytes" % len(data))
    print("dimensions: %dx%d" % (width, height))
    print("output: %s" % target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
