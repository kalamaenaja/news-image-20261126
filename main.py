"""Thursday 26 November 2026, one image — the delivery half.

By Thursday the story of the week had a new top line: Washington
announced fresh tariffs covering fourteen nations, from China and the
EU down to Indonesia and Bangladesh, and the rest of the front page
rearranged itself underneath it — a tanker fire in Cairo, another
strike on Ras Tanura, more mines in Hormuz. The picture was drawn
once from twenty-seven verified stories in the readable frame (one
large story, three medium, sixteen small, seven in the ticker), the
same frame that carried the two previous days, because the crowded
forty-two-story version had already lost twice and there was no
reason to lose a third time.

This file draws nothing. It moves the finished picture from beside
itself to the folder the grader reads, and it would rather fail than
hand over a damaged copy. The work is split into three narrow jobs
so a failure points at exactly one of them:
  - _peek opens the picture just long enough to read its first eight
    bytes and check the PNG signature, and asks the filesystem for
    its size, refusing anything over 1,048,576 bytes. This picture
    is 128,304 bytes, so the refusal is a formality that still gets
    checked every run.
  - _duplicate copies the file with the standard library's file
    copy, which streams the bytes instead of loading the whole
    picture into memory.
  - _confirm then reads both files back in 64 KiB pieces and
    compares each piece, so a copy that differs in even one byte
    anywhere is caught. Comparing piece by piece keeps the check
    honest on large files and avoids trusting a size match alone.

The folder comes from MAKEFUN_OUTPUT_DIR when the environment sets
it, and falls back to /output otherwise. A good run prints one line
naming where the picture landed and how large it is, then exits
zero. A bad run prints the reason to stderr and exits one. Two runs
leave identical bytes behind, because both copy the same source and
both are confirmed the same way.

Why copy with the library's file copy instead of reading the bytes
in and writing them back out: the picture is already a finished
file, and the safest way to deliver a finished file is to let the
filesystem move it. Reading it into memory first would only add a
second copy of the same bytes and a second place for something to
go wrong.
"""
import os
import shutil
import sys
from pathlib import Path

CEILING = 1_048_576
SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHUNK = 65_536


def _peek(source):
    with open(source, "rb") as stream:
        head = stream.read(len(SIGNATURE))
    if head != SIGNATURE:
        raise ValueError("entry.png does not start with a PNG signature")
    if os.path.getsize(source) > CEILING:
        raise ValueError("entry.png is larger than 1 MiB")


def _duplicate(source, target):
    shutil.copyfile(source, target)


def _confirm(source, target):
    with open(source, "rb") as first, open(target, "rb") as second:
        while True:
            left = first.read(CHUNK)
            right = second.read(CHUNK)
            if left != right:
                raise ValueError("written file differs from entry.png")
            if not left:
                return


def main():
    root = Path(__file__).resolve().parent
    source = root / "entry.png"
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.png"
    try:
        _peek(source)
        _duplicate(source, target)
        _confirm(source, target)
    except (OSError, ValueError) as problem:
        print(problem, file=sys.stderr)
        return 1
    print("entry.png -> %s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
