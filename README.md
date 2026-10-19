# Watsejy (watsejy.co.za)

**Wat sê jy?** Local-first Afrikaans speech-to-text for meetings and WhatsApp voice notes.

This repository currently holds **Phase 0**: the research, the legal groundwork, and the benchmark harness that decides which Afrikaans model ships in the app. Nothing here processes user audio in production yet.

## Layout

```
reports/      Feasibility research and the phased build plan (read these first)
research_notes/  Raw research notes behind the report
benchmark/    Scripts to normalise audio, run candidate models, and score WER/CER/DER
data/         Test-set manifests. Audio and transcripts are git-ignored (personal data)
docs/         Benchmark results and decisions
legal/        POPIA/RICA checklist, consent and licence templates, privacy notice draft
```

## Phase 0 goals

1. Legal basics in place before any real audio is handled (see `legal/CHECKLIST.md`).
2. A 2–5 hour consented test set of real Afrikaans meetings and voice notes (see `data/README.md`).
3. Benchmark results for every candidate model on that test set (see `benchmark/README.md`), plus timing on real laptops.
4. A decision on the default model and model size, recorded in `docs/benchmarks.md`.

## Quick start (benchmark machine with a GPU)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
sudo apt-get install -y ffmpeg

# 1. Put raw audio under data/raw/ and write data/test/manifest.jsonl (see data/README.md)
python benchmark/normalize.py data/test/manifest.jsonl --out-dir data/test/wav

# 2. Smoke test one model on three clips
python benchmark/transcribe.py --model digiphyte/fluister-turbo --manifest data/test/manifest.jsonl --max-clips 3

# 3. Run every candidate in benchmark/models.yaml and score them
python benchmark/run_all.py --manifest data/test/manifest.jsonl
python benchmark/score.py results/*.jsonl --markdown >> docs/benchmarks.md
```

Candidate models and why they were chosen are in `benchmark/models.yaml`. The research behind the choices is in `reports/Afrikaans transcription tool feasibility.md`; the step-by-step plan is in `reports/Build steps.md`.

## Licences

Model weights have their own licences (Fluister: MIT; BuzzASR: MIT; Sunbird: Apache-2.0, gated; pyannote: MIT, gated). Training corpora carry attribution requirements listed in `legal/ATTRIBUTION.md`.
