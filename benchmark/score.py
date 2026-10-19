#!/usr/bin/env python3
"""Score transcription results: WER and CER overall and per subset.

Applies the same text normaliser to reference and hypothesis (lowercase, strip
punctuation, collapse whitespace) so models are compared fairly. Subsets are
taken from the `source` and `codeswitch` fields in the manifest.

Usage:
    python benchmark/score.py results/*.jsonl
    python benchmark/score.py results/*.jsonl --markdown >> docs/benchmarks.md
"""
import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import jiwer

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "").lower()
    text = text.replace("’", "'").replace("‘", "'")
    text = _PUNCT.sub(" ", text)
    return _WS.sub(" ", text).strip()


def score_pairs(pairs):
    refs = [normalise(r) for r, _ in pairs]
    hyps = [normalise(h) for _, h in pairs]
    keep = [(r, h) for r, h in zip(refs, hyps) if r]
    if not keep:
        return None
    refs, hyps = zip(*keep)
    return {
        "n": len(refs),
        "wer": jiwer.wer(list(refs), list(hyps)),
        "cer": jiwer.cer(list(refs), list(hyps)),
    }


def load(path: Path):
    with path.open() as f:
        return [json.loads(l) for l in f if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", nargs="+", type=Path)
    ap.add_argument("--markdown", action="store_true", help="print a markdown table")
    args = ap.parse_args()

    table = []
    for path in args.results:
        rows = load(path)
        if not rows:
            continue
        name = rows[0].get("name", path.stem)
        overall = score_pairs([(r["ref"], r["hyp"]) for r in rows])
        by_source = defaultdict(list)
        by_cs = defaultdict(list)
        for r in rows:
            by_source[r.get("source") or "unknown"].append((r["ref"], r["hyp"]))
            by_cs["codeswitch" if r.get("codeswitch") else "mono"].append((r["ref"], r["hyp"]))
        audio = sum(r.get("duration_s", 0) for r in rows)
        wall = sum(r.get("wall_s", 0) for r in rows)
        table.append({
            "name": name,
            "overall": overall,
            "by_source": {k: score_pairs(v) for k, v in by_source.items()},
            "by_cs": {k: score_pairs(v) for k, v in by_cs.items()},
            "speed": (audio / wall) if wall else None,
            "device": rows[0].get("device"),
            "compute_type": rows[0].get("compute_type"),
        })

    sources = sorted({s for t in table for s in t["by_source"]})

    def pct(x):
        return "–" if x is None else f"{100*x:.1f}"

    if args.markdown:
        head = ["Model", "WER %", "CER %"] + [f"WER {s}" for s in sources] + ["WER mono", "WER code-switch", "x realtime", "device"]
        print("| " + " | ".join(head) + " |")
        print("|" + "---|" * len(head))
        for t in sorted(table, key=lambda t: t["overall"]["wer"] if t["overall"] else 9):
            o = t["overall"] or {}
            cells = [t["name"], pct(o.get("wer")), pct(o.get("cer"))]
            cells += [pct((t["by_source"].get(s) or {}).get("wer")) for s in sources]
            cells += [pct((t["by_cs"].get("mono") or {}).get("wer")), pct((t["by_cs"].get("codeswitch") or {}).get("wer"))]
            cells += [f"{t['speed']:.1f}" if t["speed"] else "–", f"{t['device']}/{t['compute_type']}"]
            print("| " + " | ".join(cells) + " |")
        print()
    else:
        for t in sorted(table, key=lambda t: t["overall"]["wer"] if t["overall"] else 9):
            o = t["overall"] or {}
            print(f"{t['name']:28s} WER {pct(o.get('wer')):>6}  CER {pct(o.get('cer')):>6}  "
                  f"n={o.get('n')}  speed={t['speed'] and round(t['speed'],1)}x")
            for s in sources:
                v = t["by_source"].get(s)
                if v:
                    print(f"    {s:14s} WER {pct(v['wer']):>6}  n={v['n']}")
            for k in ("mono", "codeswitch"):
                v = t["by_cs"].get(k)
                if v:
                    print(f"    {k:14s} WER {pct(v['wer']):>6}  n={v['n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
