import os
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.txt"
    data = source.read_bytes()
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.txt").write_bytes(data)


if __name__ == "__main__":
    main()
