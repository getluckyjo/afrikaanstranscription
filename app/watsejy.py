#!/usr/bin/env python3
"""Watsejy command line: transcribe Afrikaans audio on your Mac.

Examples:
    python app/watsejy.py ~/Downloads/PTT-20261019-WA0003.opus
    python app/watsejy.py meeting.m4a --speakers
    python app/watsejy.py meeting.m4a --speakers --num-speakers 4 --formats txt,md,srt
    python app/watsejy.py *.opus --out-dir ~/Watsejy/out

Outputs are written next to the input (or to --out-dir) as <name>.txt / .md / .srt / .json.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--speakers", action="store_true", help="label speakers (needs HF_TOKEN)")
    ap.add_argument("--num-speakers", type=int, help="fix the number of speakers if you know it")
    ap.add_argument("--engine", choices=["mlx", "ct2"], help="default: mlx on Apple Silicon, else ct2 (CPU)")
    ap.add_argument("--model", help="Hugging Face repo or local path; default Fluister turbo")
    ap.add_argument("--language", default="af")
    ap.add_argument("--formats", default="txt,md", help="comma list of txt,md,srt,json")
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--quiet", action="store_true", help="do not print the transcript")
    args = ap.parse_args()

    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
    writers = {"txt": lambda t: t.to_txt(), "md": lambda t: t.to_md(), "srt": lambda t: t.to_srt(), "json": lambda t: t.to_json()}
    bad = [f for f in formats if f not in writers]
    if bad:
        print(f"unknown format(s): {', '.join(bad)}", file=sys.stderr)
        return 2

    rc = 0
    for f in args.files:
        try:
            t = engine.transcribe(
                f, engine=args.engine, model=args.model, language=args.language,
                speakers=args.speakers, num_speakers=args.num_speakers,
                progress=lambda m: print(f"  {m}", file=sys.stderr),
            )
        except Exception as e:  # keep going with the next file
            print(f"FAILED {f}: {e}", file=sys.stderr)
            rc = 1
            continue

        out_dir = args.out_dir or f.resolve().parent
        out_dir.mkdir(parents=True, exist_ok=True)
        for fmt in formats:
            (out_dir / f"{f.stem}.{fmt}").write_text(writers[fmt](t), encoding="utf-8")
        speed = t.duration_s / t.elapsed_s if t.elapsed_s else 0
        print(f"{f.name}: {engine._hms(t.duration_s)} audio in {t.elapsed_s:.0f}s ({speed:.1f}x real time)"
              + (f", {len(t.speakers)} speakers" if t.speakers else "") + f" -> {out_dir}", file=sys.stderr)
        if not args.quiet:
            print(t.to_txt())
    return rc


if __name__ == "__main__":
    sys.exit(main())
