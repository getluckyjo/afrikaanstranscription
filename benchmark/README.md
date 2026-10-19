# Benchmark harness (Phase 0, Step 3)

Decides which Afrikaans model ships, and at what size, by measuring every candidate on our own test set.

## Steps

1. **Build the test set** as described in `data/README.md`. You need `data/test/manifest.jsonl` with `audio`, `text`, `source` and `codeswitch` per clip.
2. **Normalise audio** to 16 kHz mono WAV:
   ```bash
   python benchmark/normalize.py data/test/manifest.jsonl --out-dir data/test/wav
   ```
3. **Convert BuzzASR** (transformers format) to CTranslate2 once:
   ```bash
   bash benchmark/convert_to_ct2.sh
   ```
4. **Accept gated models** on Hugging Face (Sunbird faster-whisper-51, pyannote 3.1 and segmentation-3.0) and `export HF_TOKEN=...`.
5. **Run all models on the GPU box**:
   ```bash
   python benchmark/run_all.py --manifest data/test/wav/manifest.jsonl
   python benchmark/score.py results/*.jsonl --markdown >> docs/benchmarks.md
   ```
6. **Diarization** on the meeting clips (needs reference RTTM files for a DER number):
   ```bash
   python benchmark/diarize.py data/test/wav/manifest.jsonl --source inperson online --ref-dir data/test/rttm
   ```
7. **Laptop timing** (Step 3.7 in the build plan). On each of the three reference machines:
   ```bash
   python benchmark/run_all.py --manifest data/test/wav/manifest.jsonl \
       --only fluister-turbo fluister-medium --device cpu --compute-type int8
   ```
   On Apple Silicon, also time whisper.cpp with Metal (see below). Record real-time factor and peak RAM in `docs/benchmarks.md`.

## whisper.cpp (desktop app runtime)

The desktop app will run whisper.cpp, so the chosen model must be converted to GGML and timed there too:

```bash
git clone https://github.com/ggml-org/whisper.cpp && cd whisper.cpp && cmake -B build && cmake --build build -j
# Fluister CT2 repos do not include PyTorch weights; convert from the transformers repo:
python models/convert-h5-to-ggml.py /path/to/digiphyte--fluister-turbo-transformers /path/to/openai--whisper-large-v3-turbo ./models
./build/bin/quantize models/ggml-model.bin models/ggml-fluister-turbo-q8_0.bin q8_0
./build/bin/whisper-cli -m models/ggml-fluister-turbo-q8_0.bin -l af -f data/test/wav/<clip>.wav
```

`convert-h5-to-ggml.py` needs the transformers-format weights (`digiphyte/fluister-turbo-transformers`) plus a checkout of the original Whisper repo for the mel filters. If `fluister-medium` is chosen, ask the author for its transformers weights or convert from the CT2 build via transformers first.

## What "good" looks like

| Subset | Expectation from research | Decision rule |
|---|---|---|
| Voice notes, monolingual | 15–25% WER | Ship if the best model is under ~25% |
| Code-switched | 25–36% WER | Flag for the in-domain fine-tune in Phase 2 |
| Read speech (FLEURS) | ~9–22% WER | Sanity check against published numbers |
| Diarization | ~20% DER on meeting benchmarks | Drives how much "merge/split" UI the review screen needs |
| Laptop speed | ≥ 2x real time on a mid-range laptop | Otherwise default to `fluister-medium` or require cloud fallback |

All numbers above come from `reports/Afrikaans transcription tool feasibility.md`.
