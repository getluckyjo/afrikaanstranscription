#!/usr/bin/env python3
"""Convert every clip in a manifest to 16 kHz mono 16-bit PCM WAV with ffmpeg.

Writes a new manifest next to the output directory with `audio` pointing at the
normalised WAV files, so the rest of the pipeline never touches the originals.

Usage:
    python benchmark/normalize.py data/test/manifest.jsonl --out-dir data/test/wav
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def normalise(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--out-manifest", type=Path, help="default: <out-dir>/manifest.jsonl")
    args = ap.parse_args()

    out_manifest = args.out_manifest or (args.out_dir / "manifest.jsonl")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    base = args.manifest.parent

    rows_out = []
    with args.manifest.open() as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            src = Path(row["audio"])
            if not src.is_absolute():
                src = base / src
            if not src.exists():
                print(f"line {line_no}: missing audio {src}", file=sys.stderr)
                return 1
            dst = args.out_dir / (src.stem + ".wav")
            normalise(src, dst)
            row = dict(row)
            row["audio"] = str(dst.resolve())
            row["original_audio"] = str(src.resolve())
            rows_out.append(row)
            print(f"ok  {src.name} -> {dst.name}")

    with out_manifest.open("w") as f:
        for row in rows_out:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows_out)} rows to {out_manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
