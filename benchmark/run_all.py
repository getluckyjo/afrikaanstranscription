#!/usr/bin/env python3
"""Run every model in models.yaml over the manifest, then print the score table.

Usage:
    python benchmark/run_all.py --manifest data/test/wav/manifest.jsonl
    python benchmark/run_all.py --manifest ... --only fluister-turbo fluister-medium
    python benchmark/run_all.py --manifest ... --device cpu --compute-type int8   # laptop timing
"""
import argparse
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--config", type=Path, default=HERE / "models.yaml")
    ap.add_argument("--only", nargs="*", help="model names to run")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--compute-type")
    ap.add_argument("--max-clips", type=int)
    ap.add_argument("--out-dir", type=Path, default=Path("results"))
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    defaults = cfg.get("defaults", {})
    compute = args.compute_type or defaults.get("compute_type", "int8_float16")

    ran = []
    for m in cfg["models"]:
        if args.only and m["name"] not in args.only:
            continue
        model_path = m["model"]
        if m.get("requires_conversion") and not Path(model_path).exists():
            print(f"skip {m['name']}: run benchmark/convert_to_ct2.sh {m['requires_conversion']} {model_path} first")
            continue
        suffix = "" if args.device == "auto" else f"-{args.device}"
        name = m["name"] + suffix
        cmd = [
            sys.executable, str(HERE / "transcribe.py"),
            "--model", model_path,
            "--manifest", str(args.manifest),
            "--name", name,
            "--out-dir", str(args.out_dir),
            "--language", str(defaults.get("language", "af")),
            "--beam-size", str(defaults.get("beam_size", 5)),
            "--device", args.device,
            "--compute-type", compute,
        ]
        if not defaults.get("vad_filter", True):
            cmd.append("--no-vad")
        if args.max_clips:
            cmd += ["--max-clips", str(args.max_clips)]
        print("\n$ " + " ".join(cmd))
        rc = subprocess.call(cmd)
        if rc != 0:
            print(f"FAILED {name} (exit {rc})", file=sys.stderr)
            continue
        ran.append(args.out_dir / f"{name}.jsonl")

    if ran:
        print("\n=== Scores ===")
        subprocess.call([sys.executable, str(HERE / "score.py"), *map(str, ran)])
        print("\nMarkdown table:  python benchmark/score.py " + " ".join(map(str, ran)) + " --markdown")
    return 0


if __name__ == "__main__":
    sys.exit(main())
