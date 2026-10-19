#!/usr/bin/env python3
"""Run pyannote speaker diarization 3.1 on meeting clips and compute DER.

Prerequisites:
  1. Accept the terms of pyannote/speaker-diarization-3.1 and
     pyannote/segmentation-3.0 on Hugging Face.
  2. export HF_TOKEN=...
  3. Reference RTTM files (one per clip, same stem) for DER; without them the
     script only writes hypothesis RTTMs under results/rttm/.

Usage:
    python benchmark/diarize.py data/test/wav/manifest.jsonl --source inperson online \
        --ref-dir data/test/rttm
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--source", nargs="*", help="only clips whose `source` is in this list")
    ap.add_argument("--ref-dir", type=Path, help="directory of reference .rttm files")
    ap.add_argument("--out-dir", type=Path, default=Path("results/rttm"))
    ap.add_argument("--device", default="cuda" if os.environ.get("CUDA_VISIBLE_DEVICES", "") != "" else "cpu")
    args = ap.parse_args()

    try:
        import torch
        from pyannote.audio import Pipeline
    except ImportError:
        print("pip install pyannote.audio torch", file=sys.stderr)
        return 1

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("set HF_TOKEN (gated model)", file=sys.stderr)
        return 1

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)
    pipeline.to(torch.device(args.device))
    args.out_dir.mkdir(parents=True, exist_ok=True)

    metric = None
    if args.ref_dir:
        from pyannote.database.util import load_rttm
        from pyannote.metrics.diarization import DiarizationErrorRate
        metric = DiarizationErrorRate()

    with args.manifest.open() as f:
        rows = [json.loads(l) for l in f if l.strip()]
    if args.source:
        rows = [r for r in rows if r.get("source") in args.source]

    for row in rows:
        audio = Path(row["audio"])
        t0 = time.time()
        diarization = pipeline(str(audio))
        wall = time.time() - t0
        hyp_path = args.out_dir / f"{audio.stem}.rttm"
        with hyp_path.open("w") as out:
            diarization.write_rttm(out)
        n_spk = len(diarization.labels())
        msg = f"{audio.name}: {n_spk} speakers, {wall:.1f}s"
        if metric is not None:
            ref_path = args.ref_dir / f"{audio.stem}.rttm"
            if ref_path.exists():
                ref = next(iter(load_rttm(str(ref_path)).values()))
                der = metric(ref, diarization)
                msg += f", DER {100*der:.1f}%"
            else:
                msg += ", no reference RTTM"
        print(msg)

    if metric is not None:
        print(f"\nOverall DER: {100*abs(metric):.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
