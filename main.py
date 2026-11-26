"""News image for Thursday 26 November 2026 — the courier.

The picture itself was drawn once, ahead of time, by a Pillow script
that laid out twenty-seven verified stories as a newspaper front page:
one hero (Trump's new tariffs on fourteen nations), three medium
stories (the Cairo tanker fire, the Houthi strike on Ras Tanura, more
tankers hitting mines in Hormuz), sixteen small grid stories, and a
seven-item ticker along the bottom. The layout is the readable one —
the dense forty-two-story version lost twice in a row on the two
previous days, so this entry never tried it.

This file does not draw anything. It only carries the finished PNG to
the place the grader looks, and it refuses to deliver a damaged file.
The checks are deliberately small and in order:
  - the file must exist beside this script and be a real PNG (the
    eight-byte PNG signature at the front);
  - it must fit under the 1 MiB ceiling (this one is 128,304 bytes);
  - after copying, the destination must contain exactly the same
    bytes, checked by comparing the two files directly.

The destination is $MAKEFUN_OUTPUT_DIR when set, otherwise /output.
Success prints one line with the destination path and size and exits
zero; any problem prints the reason to stderr and exits one.
"""
import os
import sys
from pathlib import Path

LIMIT = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _read_png(path):
    data = path.read_bytes()
    if len(data) > LIMIT:
        raise ValueError("entry.png is over the 1 MiB limit")
    if data[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG file")
    return data


def _place(data, target):
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise ValueError("copied file does not match entry.png")


def main():
    here = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        data = _read_png(here / "entry.png")
        _place(data, out_dir / "entry.png")
    except (OSError, ValueError) as err:
        print(err, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (out_dir / "entry.png", len(data)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
