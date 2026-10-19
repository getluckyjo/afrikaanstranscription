# Open-source / open-weight ASR models for Afrikaans (state as of October 2026)

Scope note: numbers below come from model cards, papers and vendor pages found 19 Oct 2026. WER figures are NOT directly comparable across sources (different test sets, normalisation, model versions). Dates are flagged where a source is older than 2025.

## Q1. How well do OpenAI Whisper models (large-v2, large-v3, turbo, medium, small) handle Afrikaans?

### Takeaway
Zero-shot Whisper is usable but mediocre on Afrikaans: the Whisper paper reports FLEURS WER of 36.7% (large-v2), 42.6% (large), 44.9% (medium), 61.1% (small), with only 4.1 hours of Afrikaans in Whisper's 680k-hour training set; independent 2025–2026 evaluations put zero-shot large-v3 at roughly 33–42% WER on read speech (FLEURS/CV) and 66–78% WER on South African corpora (Lwazi telephone, NCHLT). No per-language text figure for large-v3-turbo on Afrikaans was found.

### Cited Findings
- Whisper paper, Appendix D.2.4 Table 13 (WER % on FLEURS, Afrikaans column): tiny 91.2, base 81.5, small 61.1, medium 44.9, large 42.6, large-v2 36.7 (Dec 2022 paper; large-v3 and turbo post-date it) — [Radford et al., arXiv 2212.04356 (PDF, Table 13)](https://arxiv.org/pdf/2212.04356)
- Whisper's training data contains only 4.1 hours of Afrikaans (Appendix E training-data table) — [Radford et al., arXiv 2212.04356](https://arxiv.org/pdf/2212.04356); also cited by Stellenbosch authors: "The training data includes 4.1 hours of Afrikaans, but also thousands of hours from related languages" (Dutch, German) — [arXiv 2501.06478](https://arxiv.org/pdf/2501.06478)
- Whisper's Common Voice 9 table (Table 11) has no Afrikaans column, so the paper gives no Common Voice Afrikaans result — [Radford et al., arXiv 2212.04356](https://arxiv.org/pdf/2212.04356)
- OpenAI README gives large-v3/large-v2 per-language WER only as an image chart (no text values); it states turbo is "an optimized version of large-v3" with faster transcription and minimal accuracy loss, and is not trained for translation — [openai/whisper README](https://github.com/openai/whisper/blob/main/README.md)
- Model sizes/VRAM/speed from the README: tiny 39M (~1 GB, ~10x), base 74M (~1 GB, ~7x), small 244M (~2 GB, ~4x), medium 769M (~5 GB, ~2x), large 1550M (~10 GB, 1x), turbo 809M (~6 GB, ~8x) (relative speed measured on A100, English) — [openai/whisper README](https://github.com/openai/whisper/blob/main/README.md)
- Turbo is "a finetuned version of a pruned Whisper large-v3 ... the number of decoding layers have reduced from 32 to 4" — [openai/whisper-large-v3-turbo model card](https://huggingface.co/openai/whisper-large-v3-turbo)
- Zero-shot whisper-large-v3 on Afrikaans (BuzzASR paper baselines, combined FLEURS + Common Voice 25 test set, normalised): WER 33.04%, CER 10.88%; FLEURS-only CER 11.74%, CV25-only CER 9.6% — [BuzzASR/afrikaans model card](https://huggingface.co/BuzzASR/afrikaans); [BuzzASR paper arXiv 2609.09554 Tables 7–8](https://arxiv.org/pdf/2609.09554)
- Zero-shot Whisper-v3 on South African test sets (WER/CER): Lwazi 66.05/34.32, NCHLT 77.61/24.22, Common Voice 19 35.85/9.9 (Table F.1) — [Voice of a Continent, arXiv 2505.18436](https://arxiv.org/html/2505.18436)
- Vendor comparison (ElevenLabs, undated, no methodology): Whisper Large v3 41.7% WER on FLEURS Afrikaans vs Scribe v1 17.0%, Gemini Flash 2 13.3%, Deepgram Nova 2 99.5% — [ElevenLabs Afrikaans STT page](https://elevenlabs.io/speech-to-text/afrikaans) (treat as marketing)
- Zero-shot Whisper medium on Afrikaans preschool child narratives: 88.1% WER (small: 90.3%) — [Stellenbosch/Edinburgh, arXiv 2501.06478](https://arxiv.org/pdf/2501.06478)
- Fluister model card notes stock Whisper "produces Dutch spellings" for Afrikaans — [digiphyte/fluister-turbo-transformers](https://huggingface.co/digiphyte/fluister-turbo-transformers)
- Fleurs-SLU paper Appendix A.5 lists Whisper-v3-Large and SeamlessM4Tv2-Large Afrikaans ASR figures, but the extracted table cells are garbled ("13.18.8" / "12.613.6"), so exact values could not be read reliably — [arXiv 2501.06117](https://arxiv.org/pdf/2501.06117)

### Inferences
- The 36.7% (large-v2, 2022) → ~33% (large-v3, 2026 BuzzASR baseline) FLEURS/CV range suggests large-v3 improved Afrikaans only modestly; large-v3 on CV25 is much cleaner (CER 9.6) than on spontaneous SA speech.
- The jump from ~35% WER (read speech) to 66–78% WER (Lwazi/NCHLT) shows zero-shot Whisper will struggle badly on telephone-quality and local-accent audio, which is the WhatsApp voice-note regime.
- Expect turbo to roughly track large-v3 on Afrikaans (same encoder), but nobody has published an Afrikaans-specific turbo number.

### Gaps
- No published per-language text value for large-v3 or large-v3-turbo on FLEURS/CV Afrikaans from OpenAI (only an image chart).
- No zero-shot WER (only CER) from BuzzASR for large-v3 on FLEURS-only.

## Q2. Afrikaans-fine-tuned Whisper / wav2vec2 models on Hugging Face

### Takeaway
At least four open Afrikaans-capable Whisper fine-tunes exist with published numbers: BuzzASR/afrikaans (large-v3, MIT; 16.0% WER combined FLEURS+CV25, 4.2% on CV25), digiphyte/fluister-turbo (large-v3-turbo, MIT; 8.6% WER on NCHLT read speech, explicitly trained for Afrikaans–English code-switching), Sunbird SunflowerASR-51 (large-v3, Apache-2.0, gated; 9.6% WER on its 729-clip Afrikaans test), plus the "Simba" models from the Voice of a Continent paper (12–17% WER on NCHLT/CV-19; availability unclear). No credible wav2vec2 Afrikaans fine-tune with published numbers surfaced.

### Cited Findings
- BuzzASR/afrikaans: fine-tuned from openai/whisper-large-v3 ("simple fine-tuning", Whisper tokenizer, ASR only), part of a 102-model suite; MIT licence; ~2B params F16; results (normalised CER/WER %): FLEURS 7.67/22.36, Common Voice 25 1.03/4.21, combined 5.35/16.01; zero-shot large-v3 combined CER 10.88; ~2x CER reduction; monolingual; no code-switching mention — [BuzzASR/afrikaans](https://huggingface.co/BuzzASR/afrikaans)
- BuzzASR paper (Findings of EMNLP 2026, arXiv 2609.09554): training data = FLEURS (~10 h/language) + Common Voice capped at 90 h/language + text-only Goldfish data; Afrikaans combined-test WER: full fine-tune (FFT) 17.39, simple FT (SFT) 16.01, SFT-MTL 24.15, Whisper zero-shot 33.04, Omnilingual 1B 21.53, Omnilingual 7B 16.34, MMS 22.74, Cohere 74.79, Qwen3 73.34; CER: FFT 6.72, SFT 5.35, Whisper 10.88, Omni-1B 6.69, Omni-7B 5.24, MMS 6.74 — [arXiv 2609.09554 Tables 7–8](https://arxiv.org/pdf/2609.09554)
- digiphyte/fluister-turbo-transformers: fine-tune of whisper-large-v3-turbo for "Afrikaans and South African English", code-switching merged into base weights; training data andreoosthuizen/afrikaans-30s (CC-BY-4.0) + NCHLT afr and eng (CC-BY-3.0); NCHLT read-speech test WER: Afrikaans 0.086, English 0.017; MIT; 0.8B params; recommends language="af" for mixed conversations; known gaps: SA place names/surnames, proper nouns, numbers, rare/technical terms; variants: digiphyte/fluister-turbo (CTranslate2/faster-whisper), WhisperKit Core ML — [digiphyte/fluister-turbo-transformers](https://huggingface.co/digiphyte/fluister-turbo-transformers)
- Fluister MLX/CT2 build reports Afrikaans WER 0.092 on the andreoosthuizen/afrikaans-30s test split (CT2 int8) — [digiphyte/fluister-turbo-mlx](https://huggingface.co/digiphyte/fluister-turbo-mlx); a fluister-medium variant exists without a published WER — [digiphyte/fluister-medium](https://huggingface.co/digiphyte/fluister-medium)
- Sunbird/SunflowerASR-51-african-languages: Whisper large-v3 (1.55B) fine-tuned on 51 African languages; Afrikaans training 51.6 h from Common Voice, FLEURS, ASR Africa Data Efficiency Benchmark and Afrikaans-30s; Afrikaans test (729 clips) WER 0.096 / CER 0.039 (4th best of 51); on SimbaBench Afrikaans 0.312 WER vs Simba-S 0.145 and Gemini 2.5 Pro 0.158; Apache-2.0; gated; paper "Group Relative Policy Optimisation Improves Multilingual Speech Recognition in Low-Resource Languages" not yet released — [Sunbird/SunflowerASR-51-african-languages](https://huggingface.co/Sunbird/SunflowerASR-51-african-languages)
- Sunbird also publishes a faster-whisper (CTranslate2 fp16) conversion; pass language="af", do not rely on auto language detection; gated; Apache-2.0 — [Sunbird/faster-whisper-51-african-languages](https://huggingface.co/Sunbird/faster-whisper-51-african-languages)
- Simba ASR models (Voice of a Continent, May 2025) Afrikaans WER/CER: Simba-S Lwazi 15.62/4.99, NCHLT 12.39/2.01, CV-19 16.97/7.47; Simba-W Lwazi 29.22/11.0, NCHLT 20.82/3.81, CV-19 27.87/11.27; Simba-X worst (102.96 WER Lwazi) — [arXiv 2505.18436](https://arxiv.org/html/2505.18436)
- Other HF repos found but without published Afrikaans metrics: jonahdvt/whisper-fleurs-large-afri (Whisper large fine-tuned on FLEURS African languages) — [commit page](https://huggingface.co/jonahdvt/whisper-fleurs-large-afri/commit/05c5ca603d200e7dea06c55f70a478f1447b42d5); Professor/whisper-medium-afrispeech and whisper-small-afrispeech are for African-accented English (AfriSpeech), not Afrikaans — [Professor/whisper-medium-afrispeech](https://huggingface.co/Professor/whisper-medium-afrispeech)
- Stellenbosch child-speech work (ICASSP 2025): Whisper medium fine-tuned on 5 min of Afrikaans child speech reaches 47.4% dev WER (small: 54.4%); LoRA improves Afrikaans 47.4→41.1%; best combined system 29.8% dev WER; the paper also tried XLS-R and found it worse than Whisper in this setting — [arXiv 2501.06478](https://arxiv.org/pdf/2501.06478)

### Inferences
- Fluister is the only model explicitly built for the WhatsApp-style use case (spontaneous Afrikaans + SA English + code-switching, turbo-sized, with faster-whisper and Core ML builds). Its 8.6% WER is on read NCHLT speech, so expect worse on noisy voice notes.
- BuzzASR's 4.2% on CV25 is partly in-domain (trained on CV); the combined 16% is the more honest number.
- All three main candidates (BuzzASR, Fluister, Sunflower) are Whisper large-v3 derived, so they share the same runtime tooling (transformers, faster-whisper, whisper.cpp after conversion).

### Gaps
- No wav2vec2/XLS-R Afrikaans fine-tune with a published WER was found on Hugging Face (searches for "wav2vec2 afrikaans" surfaced none with metrics).
- Simba model weights' availability/licence not confirmed.
- Lelapa's "Lelapa-X-ASR Afrikaans" datasheet (April 2024, call-centre data) returned HTTP 403, so its architecture/WER could not be read — [datasheet URL](https://lelapa.ai/wp-content/uploads/2024/04/Lelapa-Datasheet-Lelapa-X-ASR-Afrikaans.pdf)

## Q3. Other open multilingual models (MMS, SeamlessM4T, Omnilingual ASR, NVIDIA Canary/Parakeet, Gemma, Kyutai, Voxtral, Moonshine)

### Takeaway
Meta's models are the only non-Whisper open families with confirmed Afrikaans support: MMS-1B-all (CC-BY-NC, ~22–26% WER on CV, but 92–119% on Lwazi/NCHLT), SeamlessM4T-v2 (28% WER NCHLT, 19.5% CV-19 zero-shot, best non-fine-tuned option on SA data) and Omnilingual ASR (Nov 2025, 300M–7B, Afrikaans in the ">50 h" tier; 16.3% WER for the 7B on BuzzASR's test). NVIDIA Canary-1B-v2/Parakeet-TDT-0.6B-v3 (25 European languages), Mistral Voxtral Transcribe 2 (13 languages), Kyutai STT (en/fr) and Moonshine (English only) do not list Afrikaans; Gemma 4 claims multilingual ASR without a language list.

### Cited Findings
- facebook/mms-1b-all: supports "afr"; 1.0B params; CC-BY-NC 4.0; language adapters loaded via model.load_adapter(); Open ASR Leaderboard mean WER 22.54 (English); paper May 2023 — [facebook/mms-1b-all](https://huggingface.co/facebook/mms-1b-all)
- MMS Afrikaans on SA test sets (WER/CER): Lwazi 92.06/37.59, NCHLT 118.72/31.86, CV-19 26.29/6.7 — [arXiv 2505.18436](https://arxiv.org/html/2505.18436); MMS Afrikaans on BuzzASR combined FLEURS+CV25 test: WER 22.74, CER 6.74 — [arXiv 2609.09554](https://arxiv.org/pdf/2609.09554)
- MMS paper per-language table shows an "Afrikaans 6.3 6.3 CC LM" row (metric column header not recoverable from the PDF extract; likely CER on FLEURS with/without LM) — [arXiv 2305.13516](https://arxiv.org/pdf/2305.13516)
- SeamlessM4T-v2 supports Afrikaans (afr, Latin) as source speech; Afrikaans WER/CER: Lwazi 37.91/16.47, NCHLT 27.96/4.63, CV-19 19.52/9.18 — [arXiv 2505.18436](https://arxiv.org/html/2505.18436); SeamlessM4T docs language table (mirror) — [seamless_communication docs mirror](https://www.dagshub.com/DagsHub-Science/seamless_communication/src/main/docs/m4t)
- Omnilingual ASR (Meta FAIR, released 10 Nov 2025): wav2vec2-style SSL encoders at 300M/1B/3B/7B (OmniASR-W2V-0.3B = 317M, 1B = 965M, 3B = 3046M) plus CTC and LLM decoders; trained on 4.3M hours; Afrikaans (afr_Latn) is listed in the "H" (high-resource, >50 h training data) bucket; CER <10 for 78% of 1,600 languages — [arXiv 2511.09690](https://arxiv.org/html/2511.09690v1); release reported as Apache-2.0 on GitHub/Hugging Face — [the-decoder](https://the-decoder.com/metas-omnilingual-asr-brings-speech-recognition-to-1600-languages/), [OpenSourceForU](https://www.opensourceforu.com/2025/11/metas-omnilingual-asr-brings-1600-languages-to-open-source-speech-ai/)
- Omnilingual ASR Afrikaans on BuzzASR combined test: Omni 1B WER 21.53 / CER 6.69; Omni 7B WER 16.34 / CER 5.24 — [arXiv 2609.09554](https://arxiv.org/pdf/2609.09554); Omnilingual LLM 7B on AfriSwitch code-switched Afrikaans: 30.43% WER — [arXiv 2608.26434](https://arxiv.org/pdf/2608.26434)
- NVIDIA parakeet-tdt-0.6b-v3 (Aug 2025): 25 languages, all European; Afrikaans not included; CC-BY-4.0; ~0.6B params — [nvidia/parakeet-tdt-0.6b-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3); canary-1b-v2 same 25-language list — [nvidia/canary-1b-v2](https://huggingface.co/nvidia/canary-1b-v2)
- Mistral Voxtral Transcribe 2 (Feb 2026): 13 languages (EN, ZH, HI, ES, AR, FR, PT, RU, DE, JA, KO, IT, NL), no Afrikaans — [dsebastien notes on Voxtral Transcribe 2](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Voxtral+Transcribe+2); Voxtral Mini 3B (Jul 2025) docs name EN/ES/FR/PT/HI/DE/NL/IT — [HF Voxtral docs](https://huggingface.co/docs/transformers/model_doc/voxtral)
- Kyutai STT: checkpoint naming is "stt-2.6b-en_fr" (English/French); the model card itself returned HTTP 401 during this research — [kyutai/stt-2.6b-en_fr-trfs](https://huggingface.co/kyutai/stt-2.6b-en_fr-trfs)
- Google Gemma 4 E2B/E4B/12B are "trained for multilingual speech recognition" but the audio docs give no language list; Afrikaans not mentioned; Gemma 3n introduced audio input — [ai.google.dev Gemma audio docs](https://ai.google.dev/gemma/docs/capabilities/audio); a third-party tutorial calls Gemma 3n's multilingual transcription "poor" — [debuggercafe](https://debuggercafe.com/fine-tuning-gemma-3n-for-speech-transcription/)
- Moonshine streaming models (34M/123M/245M) are English-only — [UsefulSensors/moonshine-streaming-tiny](https://huggingface.co/UsefulSensors/moonshine-streaming-tiny)
- Open ASR Leaderboard multilingual track covers German, French, Italian, Spanish, Portuguese (v4, March 2026 renamed "ASR Leaderboard", 86 systems); no Afrikaans — [arXiv 2510.06961](https://arxiv.org/abs/2510.06961v2)
- MLR benchmark of African ASR (2026): MMS and W2v-BERT are more data-efficient in very low-resource regimes, XLS-R scales better with more data, Whisper is best in mid-resource conditions — [Nahabwe et al., PMLR v302](https://proceedings.mlr.press/v302/nahabwe26a.html)
- AfriSwitch finding: "Coverage is not competence" — Omnilingual 7B nominally supports 1,600+ languages but is beaten on 11/12 languages by a smaller Africa-targeted system — [arXiv 2608.26434](https://arxiv.org/pdf/2608.26434)

### Inferences
- MMS's CC-BY-NC licence rules it out for a product unless the tool is strictly non-commercial; Omnilingual ASR (Apache-2.0 per press) and SeamlessM4T-v2 (CC-BY-NC for the models) need licence checks before shipping.
- Zero-shot, SeamlessM4T-v2 (28% NCHLT) beats zero-shot Whisper-v3 (78% NCHLT) on South African audio, but fine-tuned Whisper variants (9–16%) beat both.
- Omnilingual 7B (16.3%) matches BuzzASR's fine-tuned Whisper (16.0%) zero-shot, which makes it a strong no-fine-tuning option if GPU memory for 7B is available.

### Gaps
- No Afrikaans-specific WER/CER from Meta's own Omnilingual or MMS release materials (only third-party evaluations).
- Omnilingual ASR licence not verified from the model card (fetch returned 401).
- Gemma 4 / Kyutai Afrikaans support unverified.

## Q4. Afrikaans speech datasets for evaluation and fine-tuning

### Takeaway
Roughly 250 hours of Afrikaans audio exist across public corpora; the practically usable labelled sets are NCHLT Afrikaans (56 h read speech, CC BY 3.0), andreoosthuizen/afrikaans-30s (~50 h spontaneous community/religious speech, CC-BY-4.0), FLEURS (~10 h train), Lwazi (telephone, 4–10 h), while Common Voice Afrikaans is tiny (0.76 validated hours, CC0). AfriSwitch adds 0.68 h of code-switched Afrikaans test data.

### Cited Findings
- NCHLT Afrikaans Speech Corpus: ~56 h orthographically transcribed broadband speech, test suite of 8 speakers, 16 kHz 16-bit, 4.6 GB, licence field CC BY 3.0 Unported, click-through download agreement — [SADiLaR repo 20.500.12185/280](https://repo.sadilar.org/handle/20.500.12185/280); third-party listing: 210 speakers (98 F / 112 M) — [alphaneural NCHLT listing](https://app.alphaneural.io/datasets/aconeil/nchlt)
- NCHLT project target was ~50 h per official language; NCHLT auxiliary data adds 20–170 h per language (Afrikaans amount not retrieved: PMC page blocked the fetch) — [PMC8814303](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8814303/); SADiLaR hosts an "NCHLT Afrikaans Auxiliary Speech Corpus" — [SADiLaR 20.500.12185/522](https://repo.sadilar.org/handle/20.500.12185/522)
- NCHLT Speech II Corpus: built from aligned National Parliament audio with Hansard transcriptions, XML with timing and GOP scores, 16 kHz WAV, CC BY 3.0 ZA (languages covered not confirmed) — [SADiLaR signposting record](https://repo.sadilar.org/signposting/describedby/5c608f14-7eba-4c83-8f56-36762f403124)
- Lwazi Afrikaans ASR corpus (CSIR Meraka, 2 Apr 2013): telephone speech, CC BY 2.5 ZA, 195 MB zip; corpus-level: 11 languages, ~4–10 h per language — [SADiLaR 20.500.12185/434](https://repo.sadilar.org/handle/20.500.12185/434); [arXiv 2505.18436](https://arxiv.org/html/2505.18436)
- Common Voice Scripted Speech 25.0 Afrikaans (Mar 2026): 978 clips, 1.65 h recorded, 0.76 h validated, 66 speakers, 21,367-sentence text corpus, CC0-1.0, re-hosting forbidden; v24: 0.72 h validated; v23: 0.6 h — [Mozilla Data Collective CV 25 Afrikaans](https://datacollective.mozillafoundation.org/datasets/cmn29hngy0188mm07kzspi4d4)
- FLEURS: ~10 h training per language, plus dev/test (used as the standard Afrikaans benchmark by BuzzASR, Whisper, ElevenLabs) — [arXiv 2609.09554](https://arxiv.org/pdf/2609.09554); SIB-Fleurs Afrikaans split 406 train / 86 val / 95 test utterances — [arXiv 2501.06117](https://arxiv.org/pdf/2501.06117)
- andreoosthuizen/afrikaans-30s: ~56 h raw / ~50 h processed (46.6 train / 5.0 val / 5.0 test), 6,816 rows, 30-s chunks at 16 kHz, informal spontaneous speech (sermons, announcements, conversations from NG Kranzkloof and NG Westville congregations), varied accents and background noise, "minimal" English words, CC-BY-4.0, card says commercial use allowed but also "research only" — [afrikaans-30s dataset card](https://huggingface.co/datasets/andreoosthuizen/afrikaans-30s)
- Voice of a Continent tallies 255.3 h of Afrikaans audio across sources, incl. VoxLingua107 97.46 h (unlabelled) and a >3 h TTS corpus — [arXiv 2505.18436](https://arxiv.org/html/2505.18436)
- AfriSwitch (Aug 2026): 61.36 h total, Afrikaans 0.68 h / 198 utterances, avg 4.64 switch points per utterance, CMI 13.43; released at huggingface.co/datasets/intronhealth/AfriSwitch — [arXiv 2608.26434](https://arxiv.org/pdf/2608.26434)
- SADiLaR "AwezaMed ASR test data": 1 h broadband test corpus in Afrikaans, English, isiXhosa, isiZulu — [SADiLaR 20.500.12185/688](https://repo.sadilar.org/handle/20.500.12185/688?show=full); an "Afrikaans Radio News Speech Corpus" is also listed — [SADiLaR 20.500.12185/241](https://repo.sadilar.org/handle/20.500.12185/241)
- AfriSpeech-Parliament (test-only, ~36 h, Ghana/Kenya/Nigeria/South Africa) targets accented English, not Afrikaans — [intronhealth/afrispeech-parliament](https://huggingface.co/datasets/intronhealth/afrispeech-parliament)
- Sunbird aggregated 51.6 h Afrikaans from CV + FLEURS + ASR Africa Data Efficiency Benchmark + afrikaans-30s — [SunflowerASR card](https://huggingface.co/Sunbird/SunflowerASR-51-african-languages)

### Inferences
- NCHLT (read, clean) + afrikaans-30s (spontaneous, noisy) is the natural ~100 h fine-tuning pair; Fluister already used exactly this recipe.
- Common Voice Afrikaans is too small to be a serious fine-tuning set; it is useful only as a small clean test set.
- The NCHLT CC BY 3.0 and afrikaans-30s CC-BY-4.0 licences allow derivative models for a free tool with attribution; the afrikaans-30s "research only" line conflicts with its "commercial use allowed" line and needs clarification with the author.

### Gaps
- Afrikaans hours in the NCHLT auxiliary corpus and the Afrikaans Radio News corpus were not retrieved.
- Size of the Lwazi Afrikaans set in hours/speakers is not stated on the SADiLaR record.

## Q5. Afrikaans–English code-switching and informal voice-note speech

### Takeaway
Code-switched Afrikaans is measurably harder: on AfriSwitch's in-the-wild conversational Afrikaans, the best zero-shot systems score 26% WER (ElevenLabs 26.04, Sahara V2.5 26.45) and open Omnilingual 7B scores 30.4%, versus ~9–16% for fine-tuned models on read speech. Among open models only Fluister explicitly trains for Afrikaans/English mixing; most benchmark data (NCHLT, FLEURS, CV) is monolingual read speech.

### Cited Findings
- AfriSwitch Afrikaans zero-shot WER: Sahara V2 59.14, Sahara V2.5 26.45, Omnilingual LLM 7B 30.43, Gemini 3.6 36.90, ElevenLabs Scribe 26.04; Afrikaans mean across systems 35.79% (one of the three easiest languages in the benchmark); every system was given the matrix-language label, so numbers are an upper bound on unprompted performance — [arXiv 2608.26434](https://arxiv.org/pdf/2608.26434)
- AfriSwitch notes WER under-weights embedded English tokens because the matrix language dominates; it releases switch-level English span tags so point-of-interest error rates can be computed — [arXiv 2608.26434](https://arxiv.org/pdf/2608.26434)
- Fluister: trained with Afrikaans/English code-switching "merged into the base weights"; recommends forcing language="af" rather than auto-detect for mixed conversations; South African English transcribed accurately; weak on SA place names, surnames, numbers — [digiphyte/fluister-turbo-transformers](https://huggingface.co/digiphyte/fluister-turbo-transformers)
- afrikaans-30s (the main spontaneous-speech training set) contains only "minimal" English insertions — [afrikaans-30s dataset card](https://huggingface.co/datasets/andreoosthuizen/afrikaans-30s)
- Existing South African code-switched corpora (soap-opera corpus) pair English with isiZulu, isiXhosa, Setswana, Sesotho; Sepedi–English (SPCS); none includes Afrikaans — [arXiv 2505.18436](https://arxiv.org/html/2505.18436); the 2018 unified SA code-switching system covered the same five languages, not Afrikaans — [arXiv 1807.10949](https://arxiv.org/pdf/1807.10949)
- Stellenbosch: zero-shot Whisper medium on spontaneous Afrikaans child narratives 88.1% WER; 5 min in-domain data + adult data gives the largest gains; best system 29.8% dev WER — [arXiv 2501.06478](https://arxiv.org/pdf/2501.06478)
- Sunbird warns not to rely on automatic language detection with its 51-language model — [Sunbird/faster-whisper-51-african-languages](https://huggingface.co/Sunbird/faster-whisper-51-african-languages)

### Inferences
- Whisper's single language token forces a choice; forcing "af" (as Fluister recommends) keeps Afrikaans orthography while still emitting embedded English words, whereas auto-detect can flip whole segments to English or Dutch.
- The 26–36% code-switched WER range is a realistic ceiling for a voice-note tool without in-domain fine-tuning; collecting even a few hours of transcribed voice notes is likely to matter more than model choice (consistent with the Stellenbosch and AfriSwitch findings).

### Gaps
- No open model reports WER on Afrikaans–English code-switched speech other than Omnilingual 7B via AfriSwitch; no Whisper/Fluister/BuzzASR numbers on AfriSwitch exist yet.
- No public Afrikaans WhatsApp-voice-note-style dataset was found.

## Q6. South African-specific ASR efforts (Lelapa/Vulavula, Botlhale, Stellenbosch/CSIR/SADiLaR, Masakhane)

### Takeaway
Lelapa AI's Vulavula is the only SA-built API with documented Afrikaans transcription (code "afr"; 100 free calls per key, then $9.99/1,000 calls), but it is closed, API-only. Botlhale AI sells enterprise call-centre STT for 11 SA languages without public docs. Academic work is Stellenbosch (Whisper fine-tuning for Afrikaans child speech) and CSIR/NWU/SADiLaR (corpora, not models); Masakhane has no Afrikaans ASR output that could be found.

### Cited Findings
- Vulavula transcription covers isiZulu, Sesotho, Afrikaans, South African English and African French; Afrikaans code "afr"; built-in language ID if none given; sync endpoint https://vulavula-services.lelapa.ai/api/v2alpha/transcribe/sync/file; 100 free calls per key, keys expire every 90 days — [docs.lelapa.ai quickstart](https://docs.lelapa.ai/overview/quickstart-tutorials); plans $9.99/mo (1,000 calls), $49/mo (10,000), $499/mo (500,000), overage $0.005–0.003/call — [docs.lelapa.ai plans](https://docs.lelapa.ai/overview/plans.md); beta docs warn of 503s while models wake — [lelapa.ai/docs](https://lelapa.ai/docs/)
- Lelapa site: Vulavula "currently available in English, Afrikaans, isiZulu and Sesotho" — [lelapa.ai](https://www.lelapa.ai)
- Lelapa published a "Lelapa-X-ASR Afrikaans" datasheet (Apr 2024) built from South African call-centre audio (content not retrievable, HTTP 403) — [datasheet URL](https://lelapa.ai/wp-content/uploads/2024/04/Lelapa-Datasheet-Lelapa-X-ASR-Afrikaans.pdf)
- Botlhale AI: models support 11 South African languages, speech-to-text/TTS/NLU for enterprise call centres, SaaS pricing per agent seat or audio minute (June 2025) — [Daba Finance](https://dabafinance.com/en/news/south-africas-botlhale-ai-builds-speech-tech-for-african-languages); bots accept voice notes in SA languages (2023) — [The Post](https://thepost.co.za/business/jobs/2023-01-14-elon-musk-who-here-are-mzansis-young-and-rising-tech-stars)
- Stellenbosch/Edinburgh (ICASSP 2025; follow-up arXiv 2507.13205): Whisper fine-tuning for Afrikaans and isiXhosa preschool narratives; CER 28% Afrikaans / 34% isiXhosa for 5-minute models — [arXiv 2501.06478](https://arxiv.org/pdf/2501.06478); [arXiv 2507.13205](https://arxiv.org/pdf/2507.13205)
- CSIR Meraka + NWU produced Lwazi (telephone, 11 languages) and NCHLT (broadband, ~200 speakers/language); SADiLaR hosts them — [NWU repository](https://repository.nwu.ac.za/items/3c509b93-92d3-488e-836a-33ef419adabc/full); [SADiLaR Lwazi Afrikaans](https://repo.sadilar.org/handle/20.500.12185/434)
- Intron Health (Nigeria) authored AfriSwitch and evaluates "Sahara V2/V2.5" (Africa-optimised production systems) with 26.45% WER on code-switched Afrikaans — [arXiv 2608.26434](https://arxiv.org/pdf/2608.26434)
- Sunbird AI (Uganda) released the open SunflowerASR-51 covering Afrikaans — [Sunbird card](https://huggingface.co/Sunbird/SunflowerASR-51-african-languages)
- Systematic review of African low-resource ASR (Oct 2025) — [arXiv 2510.01145](https://arxiv.org/pdf/2510.01145)

### Inferences
- For a free tool, the SA commercial APIs are a cost-per-call dependency with no open weights; open Whisper fine-tunes (Fluister/BuzzASR/Sunflower) are the only zero-marginal-cost route.
- Vulavula's free tier (100 calls) is enough for a benchmark comparison but not for production.

### Gaps
- No published WER for Vulavula or Botlhale Afrikaans.
- No Masakhane Afrikaans ASR artefact found; no 2025–2026 SADiLaR-hosted Afrikaans ASR model found.

## Q7. Speaker diarization for meetings (pyannote, NeMo, WhisperX)

### Takeaway
pyannote speaker-diarization-3.1 (MIT, gated, pure PyTorch, runs on CPU by default) is language-agnostic in design and is what WhisperX wraps; WhisperX itself needs <8 GB VRAM for large-v2 and claims 70x real-time, but it has no Afrikaans wav2vec2 alignment model, so word-level timestamps for Afrikaans need a substitute (e.g. Dutch "nl" or a custom phoneme model).

### Cited Findings
- pyannote/speaker-diarization-3.1: MIT licence, gated (accept conditions + HF token for segmentation-3.0 too); 16 kHz mono input; pipelines run on CPU by default, movable to CUDA; DER (no collar, overlap scored): AMI headset 18.8, DIHARD-3 21.7, VoxConverse 11.3, AISHELL-4 12.2, AliMeeting 24.4; no languages or speed/memory stated — [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
- WhisperX: BSD-2-Clause; "requires <8GB gpu memory for large-v2 with beam_size=5"; "70x realtime with large-v2" batched; diarization optional (--diarize) via pyannote (community-1 model, CC-BY-4.0) and "far from perfect"; default alignment models exist for en/fr/de/es/it via torchaudio plus a Hugging Face list; unsupported languages need a phoneme-based wav2vec2 model — [m-bain/whisperX README](https://github.com/m-bain/whisperX)
- WhisperX DEFAULT_ALIGN_MODELS_HF contains "nl" (jonatasgrosman/wav2vec2-large-xlsr-53-dutch) and ~40 others but no "af" — [whisperx/alignment.py](https://raw.githubusercontent.com/m-bain/whisperX/main/whisperx/alignment.py)
- pyannote community: a known slowdown existed with Speaker-Diarization-3.0 in WhisperX due to faster-whisper/pyannote dependency conflicts — [whisperx on RunPod guide](https://www.runpod.io/articles/guides/whisperx-on-runpod)

### Inferences
- Diarization quality should be roughly language-independent (it uses speaker embeddings, not text); the 19–25% DER on meeting corpora (AMI/AliMeeting) is the realistic expectation for recorded meetings.
- Pipeline plan: faster-whisper (Fluister/BuzzASR CT2 weights) → pyannote 3.1 → word/segment-level speaker assignment; skip WhisperX forced alignment or map "af" to the Dutch wav2vec2 model as a hack and validate.

### Gaps
- No pyannote 3.1 real-time factor or VRAM figure was found on the model card.
- NVIDIA NeMo diarization (Sortformer/MSDD) was not covered by any retrieved source.

## Q8. Hardware: VRAM, speed, CPU and browser feasibility

### Takeaway
Whisper large-v3 needs ~10 GB VRAM in fp16 PyTorch but ~4.5 GB in faster-whisper fp16; turbo needs ~6 GB (PyTorch) or ~2.5 GB fp16 / ~1.5 GB int8 (faster-whisper) and runs ~2–8x faster than large-v3 at near-identical accuracy. CPU-only large-v3 is impractically slow (~150 s per audio minute on a desktop i9); turbo is viable on a 6 GB laptop GPU. In-browser, whisper.cpp WASM only runs up to "small" with a 120 s audio cap, and transformers.js WebGPU ports of turbo exist but have no published Afrikaans speed numbers.

### Cited Findings
- OpenAI README VRAM/speed: large ~10 GB (1x), turbo ~6 GB (~8x), medium ~5 GB (~2x), small ~2 GB (~4x) — [openai/whisper README](https://github.com/openai/whisper/blob/main/README.md)
- faster-whisper LibriSpeech run (unnamed NVIDIA GPU): large-v3-turbo fp16 19.2 s / 2,537 MB, int8 19.6 s / 1,545 MB, vs large-v3 fp16 52.0 s / 4,521 MB — [codersera Whisper Large local setup 2026](https://codersera.com/blog/whisper-large-local-setup-guide-2026/amp/)
- RTX 3060 Laptop 6 GB + i7-12650H, French audio, int8, faster-whisper: turbo 46 s sequential / 18.7 s batched (batch 10), large-v3 231 s / 43 s; batched WER 7.7% (turbo) vs 7.9% (large-v3) — [dev.to GPU ranking citing NilaierMusic benchmark](https://dev.to/thurmon_demich/best-gpu-for-whisper-in-2026-6-cards-speed-ranked-5ci3)
- Long-form comparison: turbo 13.40% WER vs large-v3 13.20% while running 129.5x vs 55.3x real time — [whispernotes blog](https://whispernotes.app/blog/introducing-whisper-large-v3-turbo)
- CPU vs GPU: large-v3 ~150 s per minute of audio on a Core i9-14900K vs ~12 s on an RTX 4070 — [jisaku.com benchmark](https://jisaku.com/posts/ai-bench-faster-whisper-speed-2026)
- RTX 4070 large-v3: faster-whisper ~12x real time vs whisper.cpp CUDA ~8x; whisper.cpp wins on Apple Metal — [promptquorum comparison](https://www.promptquorum.com/es/power-local-llm/local-whisper-stt-comparison-2026)
- whisper.cpp WASM example: runs models up to "small" inclusive ("past that point memory requirements and performance are unsatisfactory"), audio capped at 120 s, tiny model ~74 MB — [whisper.wasm README](https://github.com/fraxy-v/whisper.cpp/blob/master/examples/whisper.wasm); Firefox WASM memory capped at 256 MiB by default — [@fugood/whisper.node README](https://cdn.jsdelivr.net/npm/@fugood/whisper.node@1.0.22/README.md); WASM builds lack GPU acceleration — [offlinetts 2026 overview](https://offlinetts.com/blog/browser-speech-recognition-whisper-comparison/)
- transformers.js: Whisper via automatic-speech-recognition pipeline with device:'webgpu' and q4 dtype, falls back to WASM; community ONNX ports of large-v3-turbo exist — [LogRocket voice agent guide](https://blog.logrocket.com/voice-ai-agent-browser/); [benderrodriguez/whisper-large-v3-turbo-webgpu](https://huggingface.co/benderrodriguez/whisper-large-v3-turbo-webgpu)
- Moonshine (the usual tiny-browser option) is English-only — [UsefulSensors/moonshine-streaming-tiny](https://huggingface.co/UsefulSensors/moonshine-streaming-tiny)
- Fluister ships CTranslate2 (server/desktop), MLX and WhisperKit Core ML builds (iOS/macOS on-device) — [digiphyte/fluister-turbo-transformers](https://huggingface.co/digiphyte/fluister-turbo-transformers)

### Inferences
- A turbo-sized Afrikaans fine-tune (Fluister, 0.8B) in faster-whisper int8 fits in ~1.5–2.5 GB VRAM and transcribes a 1-minute voice note in a few seconds on any 6 GB consumer GPU, or in tens of seconds on a modern CPU; that is the pragmatic server target for a free tool.
- Browser-only Afrikaans transcription is not realistic at large/turbo quality today: WASM tops out at "small" (61% zero-shot WER on Afrikaans) and WebGPU turbo requires a ~1.6 GB download plus a WebGPU-capable device.

### Gaps
- No primary benchmark of turbo/large-v3 real-time factor on a desktop RTX 3060/4060 or on CPU via whisper.cpp was found; figures above are from secondary blogs.
- No speed numbers for any Afrikaans model in transformers.js/WebGPU.

## Q9. Realistic effort and data to fine-tune Whisper for Afrikaans, and typical WER improvement

### Takeaway
Fine-tuning Whisper for Afrikaans is a small-team task: the standard HF recipe (Whisper small, ~8 h data, 5,000 steps, 5–10 h on a single Colab-class GPU) roughly halves WER, and the 2026 Afrikaans results show 50–75% relative WER reductions with 50–100 h of CC-licensed data (large-v3 33%→16% combined FLEURS/CV with ≤100 h; 51.6 h → 9.6% on Sunbird's test; NCHLT+afrikaans-30s → 8.6% on NCHLT). Even 5 minutes of in-domain audio gave large gains in the Stellenbosch study, so collecting a few hours of real voice notes is the highest-leverage step.

### Cited Findings
- HF fine-tuning tutorial: Whisper small (244M, ~1 GB), Common Voice 11 Hindi ~8 h train (6,540 clips), 5,000 steps, ~5–10 h training on a Colab-class GPU, WER 63.5% → 32.0%; tips: gradient checkpointing, fp16, halve batch size + gradient accumulation on OOM — [HF blog: Fine-Tune Whisper](https://huggingface.co/blog/fine-tune-whisper)
- BuzzASR: "simple fine-tuning" of large-v3 with FLEURS (~10 h) + Common Voice capped at 90 h/language, ≤6 epochs with early stopping on FLEURS validation WER; Afrikaans combined WER 33.04 → 16.01 (SFT) / 17.39 (FFT) — [arXiv 2609.09554](https://arxiv.org/pdf/2609.09554); [BuzzASR/afrikaans](https://huggingface.co/BuzzASR/afrikaans)
- Sunbird: 51.6 h Afrikaans in a 51-language large-v3 fine-tune → 9.6% WER / 3.9% CER on its test set — [SunflowerASR card](https://huggingface.co/Sunbird/SunflowerASR-51-african-languages)
- Fluister: large-v3-turbo fine-tuned on afrikaans-30s (~50 h) + NCHLT afr/eng (~56 h + English) → 8.6% WER NCHLT Afrikaans, 1.7% NCHLT English — [digiphyte/fluister-turbo-transformers](https://huggingface.co/digiphyte/fluister-turbo-transformers)
- Stellenbosch (child speech, Whisper medium, up to 5k steps): 5 min in-domain data → 47.4% WER (from 88.1% zero-shot); LoRA 47.4 → 41.1%; pre-training on 52 h out-of-domain NCHLT adult speech then 5 min child data → 42.6%; NCHLT-adult-only model scored 94.5% on child speech (domain mismatch); 5 min of in-domain adult speech "nearly matches" 52 h of out-of-domain adult speech; semi-supervised pseudo-labels of unlabelled child audio gave 2–3% further; best combined 29.8% dev — [arXiv 2501.06478](https://arxiv.org/pdf/2501.06478)
- Other low-resource references: Whisper large-v2 PEFT on Javanese 89.40% → 13.77% — [Nusamandiri journal](https://ejournal.nusamandiri.ac.id/index.php/pilar/article/view/4633); LoRA on Whisper-tiny Vietnamese improves WER by 38.49 points, beating full fine-tuning by 1.45 — [arXiv 2309.10299](https://arxiv.org/html/2309.10299v1); Maltese with 3.77 h from 6 speakers barely moved (107.6 → 105.7 raw WER), showing speaker diversity matters — [titaniumbones/whisper-base-mt-commonvoice](https://friendli.ai/models/titaniumbones/whisper-base-mt-commonvoice)
- BuzzASR tokenizer analysis: Whisper's multilingual BPE needs 1.77 tokens/word for Afrikaans vs 0.92 with a per-language tokenizer (1.93x compression gain) — [arXiv 2609.09554 Table 6](https://arxiv.org/pdf/2609.09554)

### Inferences
- Because three independent groups already published MIT/Apache Afrikaans fine-tunes of large-v3/turbo in 2026, the cheapest path is to start from Fluister or BuzzASR and do a short second-stage fine-tune (LoRA or full) on a few hours of transcribed voice notes/meetings, rather than training from stock Whisper.
- Budget: one 16–24 GB GPU (or 8 GB with LoRA/8-bit and gradient checkpointing for turbo/medium), ~100 h of CC-licensed audio already available, a day or two of compute, plus the manual work of transcribing 2–5 h of in-domain audio (the step with the highest payoff per the Stellenbosch results).
- Expected outcome on real voice notes: from ~30–40% zero-shot to roughly 15–25% WER; sub-10% is only demonstrated on clean read speech.

### Gaps
- No source reports fine-tuning WER on actual WhatsApp/meeting audio for Afrikaans; the 8–16% figures are on read or semi-clean data.
- No published training-time/GPU figures for the 2026 Afrikaans fine-tunes (BuzzASR, Fluister, Sunbird).
