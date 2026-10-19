# Benchmark results

Record every run here. Append the markdown table from `benchmark/score.py --markdown`, and fill in the laptop timing and decision sections.

## Test set

| Field | Value |
|---|---|
| Date | |
| Clips | |
| Total audio (min) | |
| Hours by source (online / inperson / voicenote / read) | |
| Share code-switched | |
| Eval hold-out | 20% |

## Published numbers (for sanity checks)

| Model | Published Afrikaans WER | Test set |
|---|---|---|
| digiphyte/fluister-turbo | 8.6% | NCHLT read speech |
| Sunbird SunflowerASR-51 | 9.6% | own 729-clip test |
| BuzzASR/afrikaans | 16.0% | FLEURS + Common Voice 25 |
| whisper-large-v3 (stock) | 33.0% / 66–78% | FLEURS+CV / Lwazi, NCHLT |
| Best zero-shot on code-switched speech (AfriSwitch) | ~26% | AfriSwitch |

## GPU runs

_Paste `score.py --markdown` output here._

## Laptop timing (Step 3.7)

| Machine | CPU / GPU | RAM | Model | Runtime | Compute type | x real time | Peak RAM |
|---|---|---|---|---|---|---|---|
| Recent MacBook (Apple Silicon) | | | fluister-turbo | whisper.cpp Metal | q8_0 | | |
| Mid-range Windows laptop | | | fluister-turbo | faster-whisper CPU | int8 | | |
| Mid-range Windows laptop | | | fluister-medium | faster-whisper CPU | int8 | | |
| Cheapest expected user laptop | | | fluister-medium | faster-whisper CPU | int8 | | |

## Diarization

| Clip set | Model | DER | Notes |
|---|---|---|---|
| inperson | pyannote 3.1 | | |
| online (system audio only) | pyannote 3.1 | | |

## Decision

- Default model:
- Low-end model:
- Cloud fallback required for: 
- Known weak spots to address in the Phase 2 fine-tune:
