#!/usr/bin/env python3
"""Copy the entry text verbatim to the output directory.

Locates entry.txt next to this file, reads its bytes unchanged, and
writes them verbatim to entry.txt in the output directory
($MAKEFUN_OUTPUT_DIR, or /output when unset). Stdlib only, no network.
"""

import os
import tempfile
from pathlib import Path


def source_path() -> Path:
    """Path of the entry text shipped beside this program."""
    return Path(__file__).resolve().parent / "entry.txt"


def output_dir() -> Path:
    """Output directory: $MAKEFUN_OUTPUT_DIR, or /output when unset."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def copy_entry() -> int:
    """Copy the entry bytes verbatim to <output_dir>/entry.txt.

    Writes via a temporary file in the same directory and renames it
    into place, so a reader never sees a partial entry. Returns the
    number of bytes written.
    """
    source = source_path()
    if not source.is_file():
        raise FileNotFoundError(f"entry text not found: {source}")
    data = source.read_bytes()
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.txt"
    fd, tmp_name = tempfile.mkstemp(dir=out, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
        os.replace(tmp_name, target)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return len(data)


def main() -> None:
    copy_entry()


if __name__ == "__main__":
    main()
