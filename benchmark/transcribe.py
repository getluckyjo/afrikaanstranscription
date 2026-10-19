#!/usr/bin/env python3
"""Transcribe every clip in a manifest with one faster-whisper model.

Writes results/<name>.jsonl with one row per clip: reference text, hypothesis,
audio duration, wall-clock seconds and real-time factor. Score with score.py.

Usage:
    python benchmark/transcribe.py --model digiphyte/fluister-turbo \
        --manifest data/test/wav/manifest.jsonl --name fluister-turbo

    # CPU laptop timing run
    python benchmark/transcribe.py --model digiphyte/fluister-medium --device cpu \
        --compute-type int8 --manifest data/test/wav/manifest.jsonl --name fluister-medium-cpu
"""
import argparse
import json
import sys
import time
from pathlib import Path

import soundfile as sf
from faster_whisper import WhisperModel
from tqdm import tqdm


def read_manifest(path: Path):
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def audio_seconds(path: str) -> float:
    info = sf.info(path)
    return info.frames / float(info.samplerate)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="HF repo id with a CTranslate2 build, local dir, or size alias")
    ap.add_argument("--manifest", type=Path, required=True, help="normalised manifest (16 kHz mono WAV)")
    ap.add_argument("--name", help="output name; default derived from --model")
    ap.add_argument("--out-dir", type=Path, default=Path("results"))
    ap.add_argument("--language", default="af")
    ap.add_argument("--beam-size", type=int, default=5)
    ap.add_argument("--no-vad", action="store_true")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--compute-type", default="int8_float16")
    ap.add_argument("--max-clips", type=int, help="smoke test on the first N clips")
    args = ap.parse_args()

    name = args.name or args.model.rstrip("/").split("/")[-1]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.out_dir / f"{name}.jsonl"

    t0 = time.time()
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    load_s = time.time() - t0
    print(f"loaded {args.model} in {load_s:.1f}s (device={args.device}, compute={args.compute_type})")

    rows = list(read_manifest(args.manifest))
    if args.max_clips:
        rows = rows[: args.max_clips]

    total_audio = 0.0
    total_wall = 0.0
    with out_path.open("w") as out:
        for row in tqdm(rows, desc=name):
            dur = audio_seconds(row["audio"])
            t1 = time.time()
            segments, info = model.transcribe(
                row["audio"],
                language=args.language,
                beam_size=args.beam_size,
                vad_filter=not args.no_vad,
            )
            segs = [
                {"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}
                for s in segments
            ]
            wall = time.time() - t1
            hyp = " ".join(s["text"] for s in segs).strip()
            total_audio += dur
            total_wall += wall
            out.write(json.dumps({
                "audio": row["audio"],
                "ref": row.get("text", ""),
                "hyp": hyp,
                "segments": segs,
                "source": row.get("source"),
                "codeswitch": row.get("codeswitch"),
                "duration_s": round(dur, 2),
                "wall_s": round(wall, 2),
                "rtf": round(wall / dur, 3) if dur else None,
                "model": args.model,
                "name": name,
                "language": args.language,
                "compute_type": args.compute_type,
                "device": args.device,
            }, ensure_ascii=False) + "\n")

    speed = total_audio / total_wall if total_wall else 0
    print(f"{name}: {len(rows)} clips, {total_audio/60:.1f} min audio in {total_wall:.1f}s "
          f"({speed:.1f}x real time). Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
