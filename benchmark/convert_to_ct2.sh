#!/usr/bin/env bash
# Convert a transformers-format Whisper fine-tune to CTranslate2 for faster-whisper.
# Needed for BuzzASR/afrikaans; the Fluister and Sunbird repos already ship CT2 builds.
#
# Usage: benchmark/convert_to_ct2.sh [HF_REPO] [OUT_DIR] [QUANT]
set -euo pipefail

REPO="${1:-BuzzASR/afrikaans}"
OUT="${2:-models/buzzasr-afrikaans-ct2}"
QUANT="${3:-int8_float16}"

mkdir -p "$(dirname "$OUT")"
ct2-transformers-converter \
  --model "$REPO" \
  --output_dir "$OUT" \
  --quantization "$QUANT" \
  --copy_files tokenizer.json preprocessor_config.json \
  --force

echo "converted $REPO -> $OUT ($QUANT)"
