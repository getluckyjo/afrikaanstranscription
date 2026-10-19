# Commercial / hosted speech-to-text APIs that support Afrikaans (state as of 19 Oct 2026)

Scope note: all prices are list prices in USD unless marked, read from the provider's own pricing page on 18–19 Oct 2026. "Free tier" is marked **permanent** (recurring monthly allowance) or **trial** (one-time credit). Where a page could not be fetched or did not state something, it is listed under Gaps rather than guessed. Several Google/OpenAI model names below (Gemini 3.5 Transcribe, gpt-transcribe, MAI-Transcribe-2) are newer than my training data; everything about them comes from the fetched pages, not memory.

## Which providers list Afrikaans, and in which product / tier

### Takeaway
Afrikaans (af / af-ZA / afr) is officially supported by Google Cloud STT (Chirp, Chirp 2, Chirp 3 — Chirp 3 in Preview), Google Gemini (Gemini 3.5 Transcribe lists af-ZA; general Gemini models accept audio without a language list), Azure AI Speech (af-ZA), AWS Transcribe (af-ZA batch + streaming), OpenAI (whisper-1 via Whisper's 98-language list; newer gpt-transcribe models do not publish a list), Deepgram (Nova-3 only), AssemblyAI (Universal-2 only, not Universal-3.5 Pro), ElevenLabs Scribe v2, Rev.ai (async only), Gladia (Solaria-1 only), Groq-hosted Whisper, Microsoft MAI-Transcribe-2, Soniox, Cloudflare Workers AI Whisper, and Lelapa Vulavula (beta). Speechmatics and Mistral Voxtral do **not** support Afrikaans.

### Cited Findings
- **Google Cloud Speech-to-Text**: the supported-languages table lists Afrikaans (South Africa) af-ZA only for models `chirp`, `chirp_2` and `chirp_3` (locations seen: asia-southeast1, europe-west4, eu, us, us-central1); no `latest_long`, `latest_short`, `telephony` or `default` rows for Afrikaans — [Google STT supported languages](https://docs.cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages)
- Chirp 3 model page: Afrikaans af-ZA is listed as **Preview** (not GA) for StreamingRecognize, Recognize and BatchRecognize; Chirp 3 regions are `us` and `eu` multi-regions (GA) — [Chirp 3 model](https://docs.cloud.google.com/speech-to-text/v2/docs/chirp_3-model)
- **Google Gemini 3.5 Transcribe** (`gemini-3.5-transcribe` for files via the Interactions API, `gemini-3.5-transcribe-live` for streaming; public preview; launched 26 Aug 2026) lists Afrikaans (af-ZA) among its ~85 languages — [Gemini 3.5 Transcribe model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-transcribe); [Google blog launch post](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/)
- General Gemini audio understanding (2.5 Flash/Pro etc.) publishes **no** supported-language list; the docs show multilingual transcription demos and language detection by prompt — [Gemini audio docs](https://ai.google.dev/gemini-api/docs/audio)
- **Azure AI Speech** ("Azure Speech in Foundry Tools"): af-ZA appears in the speech-to-text locale table, in the fast-transcription column (supported), in the language-identification locale list, and in custom speech (plain-text adaptation only); post-stream refinement not supported for af-ZA — [Azure language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt)
- **Microsoft MAI-Transcribe-2** (available in Azure Voice Live / LLM speech, preview): model card lists Afrikaans first among 60 supported languages, with automatic language detection, speaker diarization and word-level timestamps — [MAI-Transcribe-2 model card PDF](https://microsoft.ai/pdf/MAI-Transcribe-2-Model-Card.pdf)
- **AWS Transcribe**: Afrikaans af-ZA supports batch and streaming; custom vocabulary (acronyms) batch+streaming; no digit formatting, no custom language models, no PII redaction, no Call Analytics. Note: the asterisk restriction excluding af-south-1 from streaming applies only to languages marked `streaming*`; af-ZA is unmarked — [AWS supported languages](https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html)
- **OpenAI**: speech-to-text guide lists models `gpt-transcribe` (recommended), `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-4o-transcribe-diarize`, `gpt-live-transcribe`; whisper-1 references the Whisper 98-language list; gpt-transcribe accepts ISO 639-1 codes but publishes no full list, and Afrikaans is not named on the page — [OpenAI STT guide](https://developers.openai.com/api/docs/guides/speech-to-text)
- Whisper's tokenizer LANGUAGES dict includes `"af": "afrikaans"`, so whisper-1 (and Groq/Cloudflare-hosted Whisper) accept Afrikaans — [openai/whisper tokenizer.py](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py)
- **Deepgram**: Afrikaans (`af`, `af-ZA`) is listed only for Nova-3 (`nova-3-general`); not Nova-2, not Flux; Whisper Cloud languages on a separate page — [Deepgram models & languages](https://developers.deepgram.com/docs/models-languages-overview)
- **AssemblyAI**: Afrikaans (`af`) is listed for Universal-2 only; it is absent from the Universal-3.5 Pro list; it sits in the "Moderate accuracy (>25% to ≤50% WER)" bucket — [AssemblyAI supported languages](https://www.assemblyai.com/docs/speech-to-text/pre-recorded-audio/supported-languages)
- **ElevenLabs Scribe v2**: Afrikaans (afr) listed, accuracy tier "Good" (>10% to ≤20% WER); Scribe v2 (batch), Scribe v2 Realtime and Scribe v2 Medical exist — [ElevenLabs STT docs](https://elevenlabs.io/docs/capabilities/speech-to-text)
- **Speechmatics**: Afrikaans is **not** among its 56 transcription languages — [Speechmatics supported languages](https://docs.speechmatics.com/introduction/supported-languages)
- **Rev.ai**: Afrikaans (`af`) listed for Async only (not streaming) — [Rev.ai languages](https://www.rev.ai/languages); Rev's FAQ says async supports 58+ languages — [search summary](https://docs.rev.ai/faq)
- **Gladia**: Afrikaans (`af`) is supported on Solaria-1 (not Solaria-3), with auto-discovery, code-switching and translation — [Gladia languages](https://docs.gladia.io/chapters/limits-and-specifications/languages)
- **Groq**: hosts `whisper-large-v3` and `whisper-large-v3-turbo`, described only as "Multilingual"; no language list on the page — [Groq STT docs](https://console.groq.com/docs/speech-to-text)
- **Mistral Voxtral**: Voxtral Mini Transcribe 2 / Voxtral Realtime support 13 languages (English, Chinese, Hindi, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Italian, Dutch); **no Afrikaans** — [Mistral Voxtral Transcribe 2 announcement](https://mistral.ai/news/voxtral-transcribe-2)
- **Lelapa AI Vulavula**: Afrikaans (`afr`) ASR, diarisation and LanguageID all **Beta**; isiZulu and RSA English are Production — [Vulavula language support](https://docs.lelapa.ai/overview/language-support)
- **Soniox**: Afrikaans (`af`) is listed as supported — [Soniox supported languages](https://soniox.com/docs/stt/concepts/supported-languages)
- **Cloudflare Workers AI** hosts `@cf/openai/whisper` and `@cf/openai/whisper-large-v3-turbo` (Whisper models, so Afrikaans via Whisper's list) — [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)

### Inferences
- The "frontier" options for Afrikaans in Oct 2026 are Gemini 3.5 Transcribe, MAI-Transcribe-2, ElevenLabs Scribe v2 and Chirp 3; the older generation (Whisper, Universal-2, Nova-3) still lists Afrikaans but with weaker published accuracy.
- Providers are quietly dropping Afrikaans from their newest tiers (AssemblyAI Universal-3.5 Pro, Gladia Solaria-3, Deepgram Flux) — a tool should pin the specific model that supports `af`.

### Gaps
- OpenAI does not publish a language list for gpt-transcribe / gpt-4o-transcribe; Afrikaans support there is unconfirmed (only whisper-1 is confirmed via the Whisper list).
- Deepgram Whisper Cloud language list and Soniox feature matrix were not fetched.

## Exact pricing and free tiers

### Takeaway
Pay-as-you-go batch prices for Afrikaans-capable models range from about $0.0005/min (Cloudflare Whisper) and $0.04/hr (Groq Whisper turbo) up to $0.016/min (Google STT V2 standard) and $1.00/hr (Azure real-time). Permanent monthly free allowances exist at Google (60 min, V1 only), Azure (5 hrs real-time), ElevenLabs (4.5 hrs Scribe v2), Groq (rate-limited free use), Cloudflare (10k neurons/day ≈ 3.5 hrs/day of Whisper) and Gemini (free tier, rate-limited, data used for training); AWS's 60 min/month lasts 12 months; Deepgram, AssemblyAI, Speechmatics, Rev.ai and Gladia give one-time credits.

### Cited Findings
- **Google STT V2**: Standard recognition $0.016/min for 0–500k min/month, $0.01 (500k–1M), $0.008 (1M–2M), $0.004 (2M+); Dynamic Batch recognition $0.003/min; the "Standard" model list on the page names default, command_and_search, latest_short, latest_long, phone_call, video, chirp (chirp_2/chirp_3 not explicitly named). V1: 0–60 min/month free, then $0.016/min with data logging or $0.024/min without logging — [Google STT pricing](https://cloud.google.com/speech-to-text/pricing)
- Google STT quotas: sync ≤ ~1 min, async ≤ ~480 min, streaming ≤ ~5 min, local file ≤ 10 MB, 480 audio-hours/day cap — [Google STT quotas](https://docs.cloud.google.com/speech-to-text/quotas)
- **Gemini API**: Gemini 3.5 Transcribe audio input $2.00 per 1M tokens, stated as $0.003 per audio minute; Gemini 3.5 Transcribe Live $3.50/1M ($0.005/min); Gemini 2.5 Flash audio input $1.00/1M; Gemini 2.5 Flash-Lite $0.30/1M; Gemini 2.5 Pro $1.25/1M (≤200k) / $2.50 (>200k). Free tier (free of charge) covers Gemini 3.5 Transcribe and Transcribe Live, 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro and newer Flash models; free-tier data is "used to improve our products", paid-tier is not — [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- Gemini audio tokenisation: 32 tokens per second = 1,920 tokens/min; up to 9.5 hours of audio per prompt (general models) — [Gemini audio docs](https://ai.google.dev/gemini-api/docs/audio)
- Gemini free-tier per-model RPM/RPD are only shown inside AI Studio; Tier 1 requires a linked billing account and has a $10 per rolling-10-minute spend cap — [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- **Azure AI Speech**: Free F0 = 5 audio hours/month real-time standard (shared with custom; batch not supported on F0) — permanent. Pay-as-you-go: real-time $1.00/hr; batch $0.18/hr (REST v3.2+); custom real-time $1.20/hr, custom batch $0.225/hr; enhanced add-ons (continuous language ID, diarization, pronunciation prosody) $0.30/hr per feature for real-time, "included with batch speech to text"; fast transcription and MAI-Transcribe-2 showed "N/A per hour" in the scrape (MAI Transcribe-2 is a limited-time promotion until 31 Dec 2026); commitment tiers $1,600/2,000 hrs, $6,500/10,000 hrs, $25,000/50,000 hrs — [Azure Speech pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)
- **AWS Transcribe** (us-east-1): batch $0.006/min, streaming $0.01/min, billed per second, no minimum; tiered discounts above 250k min (T2/T3 values not captured); free tier 60 min/month for 12 months from first request — **trial** — [AWS Transcribe pricing](https://aws.amazon.com/transcribe/pricing/)
- AWS limits: max audio file 28,800 s (8 hrs), 2 GB; job records kept 90 days — [AWS Transcribe endpoints & quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html)
- **OpenAI**: whisper-1 $0.006/min; gpt-4o-transcribe $0.006/min ($2.50/1M audio input tokens); gpt-4o-mini-transcribe $0.003/min ($1.25/1M); gpt-4o-transcribe-diarize $0.006/min; gpt-transcribe $0.0045/min; gpt-live-transcribe $0.017/min; no free tier — [OpenAI pricing](https://developers.openai.com/api/docs/pricing); gpt-transcribe model page confirms $0.0045/min — [gpt-transcribe model](https://developers.openai.com/api/docs/models/gpt-transcribe)
- **Deepgram**: Nova-3 monolingual pre-recorded $0.0043/min (Growth $0.0036), streaming $0.0048; Nova-3 multilingual pre-recorded $0.0052, streaming $0.0058; Whisper Cloud $0.0048/min; diarization included for pre-recorded, $0.0020/min for streaming; new accounts get $200 credit that does not expire — **trial credit** — [Deepgram pricing](https://deepgram.com/pricing)
- **AssemblyAI**: Universal-2 $0.15/hr; Universal-3.5 Pro $0.21/hr (no Afrikaans); streaming Universal-3.6 Pro $0.45/hr; diarization add-on +$0.02/hr async; $50 free credit at signup, no card — **trial credit** — [AssemblyAI pricing](https://www.assemblyai.com/pricing)
- **ElevenLabs**: Scribe v2 $0.22/hr on all plans (+$0.05/hr keyterm prompting, +$0.07/hr transcript editing); Scribe v2 Realtime $0.39/hr; included hours: Free 4 hr 30 min, Starter 27 hrs, Creator 100 hrs, Pro 450 hrs, Scale 1,359 hrs, Business 4,500 hrs (plan↔row mapping inferred from table order) — Free plan allowance is **permanent monthly** — [ElevenLabs API pricing](https://elevenlabs.io/pricing/api)
- **Speechmatics**: Standard $0.45/hr, Enhanced $0.75/hr batch; $100 signup credit valid 12 months — but no Afrikaans — [Speechmatics pricing](https://www.speechmatics.com/pricing)
- **Rev.ai**: Reverb foreign-language transcription $0.30/hr (English $0.20/hr); Whisper Large $0.005/min; 15-second minimum; free credits equivalent to 5 hours of Reverb ASR — **trial** — [Rev.ai pricing](https://www.rev.ai/pricing)
- **Gladia**: Solaria-1 async €0.27/hr (€0.0045/min), falling to €0.21/hr at 10,000+ hrs; Solaria-3 €0.16/hr (no Afrikaans); real-time €0.68/hr; diarization included (async only); €50 free credit valid one year — **trial** — [Gladia pricing](https://www.gladia.io/pricing)
- **Groq**: whisper-large-v3-turbo $0.04/hr, whisper-large-v3 $0.111/hr; requests under 10 s billed as 10 s; 25 MB file limit free tier / 100 MB dev tier — [Groq STT docs](https://console.groq.com/docs/speech-to-text); rate limits page shows whisper-large-v3(-turbo) at 20 RPM, 2,000 RPD, 7,200 audio-seconds/hour, 28,800 audio-seconds/day, labelled as Developer-plan base limits — [Groq rate limits](https://console.groq.com/docs/rate-limits); third-party guides report the same 7,200/28,800 numbers for the free plan — [search summary](https://www.grizzlypeaksoftware.com/articles/p/groq-api-free-tier-limits-in-2026-what-you-actually-get-uwysd6mb)
- **Cloudflare Workers AI**: 10,000 Neurons/day free, $0.011 per 1,000 Neurons above that; `@cf/openai/whisper-large-v3-turbo` = 46.63 Neurons/audio-minute ≈ $0.0005/min; limits reset daily 00:00 UTC — [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- **Mistral Voxtral**: Mini Transcribe V2 $0.003/min batch, Realtime $0.006/min — no Afrikaans — [Voxtral Transcribe 2](https://mistral.ai/news/voxtral-transcribe-2)
- **Lelapa Vulavula**: billed per API call, not per minute: Free 100 calls/month (permanent, no card), Dev Pass $9.99/month for 1,000 calls, SMME Pass $49/month for 10,000 calls, Enterprise 500k+ calls custom; what one transcription call covers in audio length is not defined — [Vulavula plans](https://docs.lelapa.ai/overview/plans.md); overage $0.005/call (Dev) and $0.003/call (SMME) per the public pricing page — [lelapa.ai pricing (via search)](https://lelapa.ai/about/pricing)

### Inferences
- For a genuinely free tool, the only recurring free capacity large enough to matter is Cloudflare Workers AI (10,000 neurons/day ÷ 46.63 ≈ 214 min/day ≈ 107 hrs/month of Whisper turbo), Groq (if the 7,200 s/hr free limit holds: up to 2 hrs of audio per wall-clock hour), Gemini free tier (rate-limited, training on your data), ElevenLabs Free (4.5 hrs/month) and Azure F0 (5 hrs/month, real-time API only).
- Gemini 3.5 Transcribe's stated $0.003/min is lower than 1,920 tokens/min × $2/1M = $0.00384/min; either the Transcribe model tokenises audio differently or the page rounds — treat $0.003–0.004/min as the range.

### Gaps
- Azure fast-transcription and MAI-Transcribe-2 per-hour prices rendered as "N/A" in the scrape (likely region/JS dependent); Azure batch transcription max file length not fetched.
- AWS T2/T3 batch tier prices and af-south-1 regional prices not captured.
- Soniox per-hour price not fetched. ElevenLabs plan monthly fees (Starter/Creator/...) not captured, only included hours.
- Gemini free-tier RPM/RPD for gemini-3.5-transcribe are only visible in AI Studio.
- Google $300 new-customer credit not verified in this research.

## Speaker diarization for Afrikaans

### Takeaway
Diarization is explicitly language-gated at Google (Chirp 3 diarization is limited to ~14 locales; Afrikaans excluded). AWS, Deepgram (Nova-3 batch), ElevenLabs, Gladia, Gemini 3.5 Transcribe, MAI-Transcribe-2 and Azure document diarization without a language restriction that would exclude Afrikaans; Lelapa offers Afrikaans diarisation in beta; AssemblyAI and OpenAI do not state language coverage for diarization.

### Cited Findings
- Google: every Afrikaans row (chirp, chirp_2, chirp_3 in all locations) shows Diarization = No; chirp_3 diarization rows exist only for zh-CN, en-IN/GB/US, fr-CA/FR, de-DE, hi-IN, it-IT, ja-JP, ko-KR, pt-BR, es-ES/US — [Google STT supported languages](https://docs.cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages); Chirp 3 page lists the same diarization language set — [Chirp 3 model](https://docs.cloud.google.com/speech-to-text/v2/docs/chirp_3-model)
- Gemini 3.5 Transcribe: speaker diarization on the unary endpoint, up to 8 speakers (3+ experimental), not combinable with custom vocabulary; no language restriction stated and af-ZA is in the language list — [Gemini 3.5 Transcribe](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-transcribe); launch post says up to three speakers reliably — [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/)
- General Gemini models list "speaker diarization" as a prompt-driven use case — [Gemini audio docs](https://ai.google.dev/gemini-api/docs/audio)
- AWS feature matrix: speaker diarization = batch, streaming, with **no** "not available for all languages" footnote (footnote 2 is attached to digits, custom LMs, PII, call summarisation only) — [AWS feature matrix](https://docs.aws.amazon.com/transcribe/latest/dg/feature-matrix.html)
- Azure: diarization is an enhanced add-on ($0.30/hr real-time, included in batch); the privacy doc says it works for real-time and batch for "two or more speakers"; no locale restriction stated — [Azure pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/); [Azure STT data privacy](https://learn.microsoft.com/en-us/legal/cognitive-services/speech-service/speech-to-text/data-privacy-security)
- MAI-Transcribe-2 adds speaker diarization and word-level timestamps across its 60 languages (Afrikaans included) — [MAI-Transcribe-2 model card](https://microsoft.ai/pdf/MAI-Transcribe-2-Model-Card.pdf)
- OpenAI: only `gpt-4o-transcribe-diarize` does diarization (segment-level start/end, up to 4 known-speaker reference clips, `chunking_strategy` needed over 30 s); no language list; not available in Realtime — [OpenAI STT guide](https://developers.openai.com/api/docs/guides/speech-to-text)
- Deepgram: diarization works with all Nova batch models (Nova-1/2/3) plus enhanced/base; not with Whisper Cloud; no language restriction stated — [Deepgram diarization](https://developers.deepgram.com/docs/diarization)
- AssemblyAI diarization page shows `universal-3-5-pro` and `universal-2` badges but no language list — [AssemblyAI speaker diarization](https://www.assemblyai.com/docs/speech-to-text/speaker-diarization)
- ElevenLabs Scribe v2: diarization up to 32 speakers; multichannel up to 5 channels — [ElevenLabs STT docs](https://elevenlabs.io/docs/capabilities/speech-to-text)
- Gladia: diarization included at no extra cost, async only; `max_speakers` is a hint; no language restriction stated — [Gladia pricing](https://www.gladia.io/pricing); [Gladia diarization](https://docs.gladia.io/chapters/pre-recorded-stt/speaker-diarization)
- Lelapa Vulavula: Afrikaans diarisation = Beta — [Vulavula language support](https://docs.lelapa.ai/overview/language-support)
- Groq Whisper endpoints: timestamps via `verbose_json`, no diarization mentioned — [Groq STT docs](https://console.groq.com/docs/speech-to-text)

### Inferences
- For meeting recordings in Afrikaans with speaker labels, the documented-safe choices are AWS Transcribe, Azure batch, Gemini 3.5 Transcribe, ElevenLabs Scribe v2, Deepgram Nova-3 and Gladia Solaria-1; Google Chirp 3 must be ruled out for diarized Afrikaans.

### Gaps
- No provider publishes diarization error rate for Afrikaans specifically.
- AssemblyAI, OpenAI gpt-4o-transcribe-diarize and Rev.ai do not state whether diarization works for Afrikaans.

## Accuracy evidence for Afrikaans

### Takeaway
The only per-language Afrikaans numbers found are vendor-published: ElevenLabs' FLEURS table (Scribe v1 17.0% WER, Gemini Flash 2 13.3%, Whisper Large v3 41.7%, Deepgram Nova-2 99.5%), ElevenLabs' tiering of Afrikaans as "Good" (10–20% WER) for Scribe v2, and AssemblyAI's own classification of Afrikaans as "Moderate" (25–50% WER) on Universal-2. No independent South African head-to-head or benchmark covering the 2026 models (Gemini 3.5 Transcribe, MAI-Transcribe-2, Chirp 3) by language was found.

### Cited Findings
- ElevenLabs Afrikaans page benchmark table (FLEURS WER): Scribe v1 17.0%, Deepgram Nova 2 99.5%, Gemini Flash 2 13.3%, Whisper Large v3 41.7%; the same page's headline claims "3.1% on FLEURS and 5.5% on Common Voice", which contradicts its own table (unresolved; vendor marketing) — [ElevenLabs Afrikaans STT page](https://elevenlabs.io/speech-to-text/afrikaans)
- ElevenLabs docs put Afrikaans in the "Good (>10% to ≤20% WER)" tier for Scribe v2 — [ElevenLabs STT docs](https://elevenlabs.io/docs/capabilities/speech-to-text)
- AssemblyAI lists Afrikaans under "Moderate accuracy (>25% to ≤50% WER)" for Universal-2 — [AssemblyAI supported languages](https://www.assemblyai.com/docs/speech-to-text/pre-recorded-audio/supported-languages)
- Gemini 3.5 Transcribe: FLEURS multilingual average 5.04% WER non-streaming / 5.50% streaming (top languages only); Artificial Analysis average 2.6% non-streaming / 4.0% streaming; only Chirp 3 is named as a comparator — [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/)
- MAI-Transcribe-2: claims lowest average FLEURS WER across its 60 languages (test split, inferred language) vs comparable systems and #2 on Artificial Analysis' English leaderboard; per-language numbers are in a chart, not extractable text — [MAI-Transcribe-2 model card](https://microsoft.ai/pdf/MAI-Transcribe-2-Model-Card.pdf)
- Mistral Voxtral Mini Transcribe 2 reports ~4% FLEURS WER across its top 10 languages (not Afrikaans) — [Voxtral Transcribe 2](https://mistral.ai/news/voxtral-transcribe-2)
- Academic (Deep Learning Indaba 2025 / PMLR 302, "Benchmarking Automatic Speech Recognition Models for African Languages", Nahabwe et al.): on NCHLT Afrikaans read speech, fine-tuning with 50 h of data reaches 2.11% WER (Whisper), 2.79% (XLS-R), 3.23% (W2v-BERT), 3.69% (MMS); with only 1 h: 26.38% / 38.62% / 22.70% / 22.23% — fine-tuned open models, not hosted APIs — [arXiv 2512.10968](https://arxiv.org/pdf/2512.10968)
- Artificial Analysis' speech-to-text leaderboard reports AA-WER (English-centric) e.g. Gemini 3.5 Transcribe 2.6%, Whisper Large v3 4.1–10.1% depending on host; no Afrikaans breakdown — [Artificial Analysis STT leaderboard](https://artificialanalysis.ai/speech-to-text/non-streaming)
- Web search for "Afrikaans speech-to-text benchmark Whisper Gemini WER" surfaced no independent Afrikaans comparison; the AfriVox-v2 and AfriSpeech-200 papers focus on other African languages/accented English — [search results](https://arxiv.org/pdf/2605.03590)

### Inferences
- Whisper-family hosts (OpenAI whisper-1, Groq, Cloudflare) are the cheapest but the only Afrikaans-specific numbers (41.7% WER on FLEURS for Whisper Large v3) suggest they are the weakest; LLM-based transcribers (Gemini) and Scribe v2 are the likeliest to be usable without fine-tuning.
- The 2.1% WER achievable by fine-tuning Whisper on 50 h of NCHLT Afrikaans suggests Afrikaans is not intrinsically hard — hosted providers' weak numbers reflect training-data share, not the language.

### Gaps
- No Afrikaans-specific WER for Gemini 3.5 Transcribe, Gemini 2.5, Chirp 3, MAI-Transcribe-2, Nova-3, Universal-2 (beyond the 25–50% bucket), gpt-4o-transcribe or Reverb.
- No South African developer/Reddit reports found in the searches run; FLEURS is read speech, not WhatsApp voice notes, so all numbers above overstate real-world accuracy.

## Code-switching (Afrikaans/English mixed) handling

### Takeaway
Explicit multi-language-within-one-file support exists at Gemini 3.5 Transcribe (auto-detects 85+ languages "including mid-session code-mixing"), Gladia Solaria-1 (code-switching listed for af), AWS (multi-language identification, batch and streaming), Azure (continuous language identification add-on; af-ZA in LID list), MAI-Transcribe-2 (automatic language detection for multilingual recordings) and OpenAI gpt-transcribe (multiple language hints). Deepgram's multilingual mode excludes Afrikaans, and Google Chirp 3's "auto" detects the single most prevalent language.

### Cited Findings
- Gemini 3.5 Transcribe: automatic detection across 85+ languages including mid-session code-mixing; "handles multi-language code-switching" — [Gemini 3.5 Transcribe](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-transcribe)
- Gladia: Afrikaans supports code-switching on Solaria-1; "For conversations mixing languages, use Solaria-1" — [Gladia languages](https://docs.gladia.io/chapters/limits-and-specifications/languages)
- AWS: multi-language identification available for batch and streaming — [AWS feature matrix](https://docs.aws.amazon.com/transcribe/latest/dg/feature-matrix.html); af-ZA listed as a language — [AWS supported languages](https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html)
- Azure: single language identification free; continuous language identification is a $0.30/hr add-on (included with batch); af-ZA is in the language-identification locale list — [Azure pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/); [Azure language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt)
- Google Chirp 3: `language_codes=["auto"]` "automatically infers and transcribes in the most prevalent language"; multiple expected locales can be passed; within-recording code-switching not stated — [Chirp 3 model](https://docs.cloud.google.com/speech-to-text/v2/docs/chirp_3-model)
- Deepgram Nova-3 `multi` covers only en, es, fr, de, hi, ru, pt, ja, it, nl — no Afrikaans — [Deepgram models & languages](https://developers.deepgram.com/docs/models-languages-overview)
- OpenAI gpt-transcribe accepts a `languages` array of hints "for multilingual audio and code-switching" — [gpt-transcribe model](https://developers.openai.com/api/docs/models/gpt-transcribe)
- MAI-Transcribe-2: "automatic language detection for multilingual recordings" — [MAI-Transcribe-2 model card](https://microsoft.ai/pdf/MAI-Transcribe-2-Model-Card.pdf)
- Lelapa: isiZulu model is code-switched; Afrikaans LanguageID is beta — [Vulavula language support](https://docs.lelapa.ai/overview/language-support)

### Inferences
- For Afrikaans/English code-switching, Gemini 3.5 Transcribe and Gladia Solaria-1 are the only providers that explicitly document in-file switching for a language set including Afrikaans; AWS/Azure LID switch at segment level.

### Gaps
- ElevenLabs Scribe v2 and AssemblyAI code-switching behaviour for Afrikaans not checked.

## Input constraints: formats and durations (WhatsApp OGG/Opus, meeting m4a/mp4/mp3)

### Takeaway
WhatsApp voice notes (OGG Opus) are accepted natively by Gemini (ogg and opus listed), ElevenLabs (OGG, Opus), Groq (ogg) and generally by the big clouds; OpenAI's documented list (mp3, mp4, mpeg, mpga, m4a, wav, webm) omits ogg/opus, so conversion is needed there. Max durations range from 25 MB file caps (OpenAI, Groq free) through 1 hour (Chirp 3 batch, Gemini 3.5 Transcribe) to 8–10 hours (AWS, ElevenLabs).

### Cited Findings
- Gemini audio: formats WAV, MP3, AIFF, AAC, OGG, FLAC, MPEG, M4A, L16, Opus, ALAW, MULAW, WebM; 9.5 hours per prompt; downsampled to 16 kbps mono — [Gemini audio docs](https://ai.google.dev/gemini-api/docs/audio)
- Gemini 3.5 Transcribe: 1 hour per request (30 min with diarization or word timestamps); live sessions 10 min — [Gemini 3.5 Transcribe](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-transcribe)
- Google Chirp 3: BatchRecognize ~1 min to 1 hour (20 min with word timestamps); generic V1/V2 async limit ~480 min; local uploads 10 MB — [Chirp 3 model](https://docs.cloud.google.com/speech-to-text/v2/docs/chirp_3-model); [Google STT quotas](https://docs.cloud.google.com/speech-to-text/quotas)
- OpenAI: 25 MB max file; formats mp3, mp4, mpeg, mpga, m4a, wav, webm (ogg/opus not listed); larger files must be compressed/chunked — [OpenAI STT guide](https://developers.openai.com/api/docs/guides/speech-to-text)
- Groq: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm; 25 MB free / 100 MB dev; URL input for larger; audio downsampled to 16 kHz mono — [Groq STT docs](https://console.groq.com/docs/speech-to-text)
- ElevenLabs: audio AAC, AIFF, OGG, MP3, Opus, WAV, WebM, FLAC, MP4, M4A plus video containers; 3 GB, up to 10 hours — [ElevenLabs STT docs](https://elevenlabs.io/docs/capabilities/speech-to-text)
- AWS: max 28,800 s (8 h), 2 GB per file — [AWS endpoints & quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html)
- Mistral Voxtral: up to 3 hours per batch request (no Afrikaans) — [Voxtral Transcribe 2](https://mistral.ai/news/voxtral-transcribe-2)

### Inferences
- A tool should normalise everything to 16 kHz mono (e.g. FLAC or MP3) with ffmpeg before upload; this sidesteps OpenAI's missing ogg support and the 25 MB caps, and matches what Groq/Gemini do internally anyway.

### Gaps
- AWS, Azure and Google input-format lists were not fetched in this pass (they are generally known to accept Ogg/Opus but this is unverified here).
- Azure batch and Deepgram/AssemblyAI/Rev.ai max durations not captured.

## Privacy, data retention and data residency (incl. South Africa)

### Takeaway
Paid API tiers at OpenAI, Google STT, Azure and (per docs) Gemini-paid do not train on customer audio by default; Gemini's **free** tier does. Only AWS (af-south-1 Cape Town, batch + streaming) and Azure (South Africa North, real-time + batch STT; no fast transcription) can keep Afrikaans audio inside South Africa; Azure processes data in the resource's region. Deepgram and AssemblyAI offer EU endpoints and training opt-outs; OpenAI offers ZDR for /v1/audio/transcriptions on approval.

### Cited Findings
- OpenAI: API data "is not used to train or improve OpenAI models" unless opted in; `/v1/audio/transcriptions` abuse-monitoring and application-state retention both "None"; the endpoint is Zero Data Retention eligible (requires approval); regional processing for audio transcription only in US and Europe (EEA + Switzerland) — [OpenAI your-data](https://developers.openai.com/api/docs/guides/your-data)
- Google STT: "By default, Cloud Speech-to-Text does not log customer audio data or transcripts"; data logging is opt-in per project in exchange for the lower price (V1: $0.016 with logging vs $0.024 without); logged data survives project deletion unless a deletion request is filed — [Google STT data logging](https://docs.cloud.google.com/speech-to-text/docs/data-logging); [Google STT pricing](https://cloud.google.com/speech-to-text/pricing)
- Gemini API: free-tier prompts are "used to improve our products"; paid tier "No" (except invite-only Contributor tier) — [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- Azure: real-time, fast transcription, pronunciation assessment and speech translation retain no customer data; batch audio/transcripts live in customer storage (or Microsoft storage with `timeToLive`); diarization voice signals are discarded after processing — [Azure STT data privacy](https://learn.microsoft.com/en-us/legal/cognitive-services/speech-service/speech-to-text/data-privacy-security)
- Azure regions: "Azure Speech stores and processes speech data in the region where you create your resource" (Voice Live excepted); `southafricanorth` supports real-time and batch transcription but **not** fast transcription, Whisper, custom training or post-stream refinement; MAI-Transcribe-2 via Voice Live in southafricanorth has "Global" processing scope (data leaves the region); LLM-speech/MAI-Transcribe is available only in centralindia, eastus, northeurope, southeastasia, westus, westus2 — [Azure Speech regions](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions)
- AWS Transcribe has batch endpoint `transcribe.af-south-1.amazonaws.com` and streaming endpoint `transcribestreaming.af-south-1.amazonaws.com` (Africa – Cape Town); Transcribe Medical batch also in af-south-1; job records retained 90 days — [AWS endpoints & quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html)
- AWS data-protection page covers the shared-responsibility model, TLS, VPC endpoints; it does not itself describe training use or an opt-out — [AWS Transcribe data protection](https://docs.aws.amazon.com/transcribe/latest/dg/data-protection.html)
- AssemblyAI: uploaded audio deletion begins at 24 h (max 48 h) without TTL/BAA; final transcripts deleted from 30 days; only contract-permitted, PII-redacted files are used for training and never for BAA, EU-server or opted-out customers; ZDR for streaming/dictation when opted out; EU servers selectable — [AssemblyAI data retention & training](https://www.assemblyai.com/docs/data-retention-and-model-training.md)
- Deepgram: Model Improvement Program can be disabled per request with `mip_opt_out=true`; EU endpoint `api.eu.deepgram.com`, Australian endpoint `api.au.deepgram.com`; retention periods referred to a separate "Your Data" page — [Deepgram data privacy & compliance](https://developers.deepgram.com/docs/data-privacy-compliance)
- Lelapa: enterprise path allows self-hosting the stack in your own cluster; no other residency statement — [Lelapa docs](https://docs.lelapa.ai/)

### Inferences
- A POPIA-sensitive deployment has two realistic in-country options: AWS Transcribe in af-south-1 (batch $0.006/min list in us-east-1; af-south-1 price not captured) and Azure batch in South Africa North ($0.18/hr list). Everything else processes abroad.
- Using Gemini's free tier for a public tool means users' voice notes are used for Google product improvement; the paid tier avoids this at ~$0.003–0.004/min.

### Gaps
- AWS AI-services opt-out policy (organisation-level opt-out from content use for service improvement) is not on the fetched page and is unverified here.
- Deepgram's actual retention periods ("Your Data at Deepgram" page), ElevenLabs' training/retention policy, Google STT retention window, Gladia and Rev.ai retention were not fetched.
- Azure af-ZA diarization in the South Africa North region is not explicitly confirmed.

## Cost scenario: 1,000 hours (60,000 minutes) of audio per month

### Takeaway
At list prices, 1,000 hrs/month of Afrikaans audio costs roughly $30 (Cloudflare Whisper) to $1,000 (Azure real-time); the most accurate-looking Afrikaans-capable options cluster at $150–$360/month (AssemblyAI Universal-2 $150, Gemini 3.5 Transcribe ~$180–230, Azure batch $180, ElevenLabs Scribe v2 $220, Deepgram Nova-3 $258, AWS batch $360).

### Cited Findings
(Each line = unit price from the cited page × 60,000 min or 1,000 hrs; arithmetic is mine.)
- Google STT V2 standard $0.016/min → **$960**; dynamic batch $0.003/min → **$180**; V1 without logging $0.024/min → **$1,440** — [Google STT pricing](https://cloud.google.com/speech-to-text/pricing)
- Gemini 3.5 Transcribe $0.003/min (page) → **$180**; by token math 1,920 tok/min × $2/1M = $0.00384/min → **$230**; Gemini 2.5 Flash audio-in $1/1M → $0.00192/min → **$115** + output tokens; Gemini 2.5 Flash-Lite $0.30/1M → **$35** + output — [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing); [Gemini audio docs](https://ai.google.dev/gemini-api/docs/audio)
- Azure real-time $1/hr → **$1,000**; batch $0.18/hr → **$180** (diarization/LID included in batch); 2,000-hr commitment $1,600/month → **$800 effective per 1,000 hrs** — [Azure pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)
- AWS batch $0.006/min → **$360**; streaming $0.01/min → **$600** (us-east-1 T1; cheaper tiers above 250k min) — [AWS pricing](https://aws.amazon.com/transcribe/pricing/)
- OpenAI whisper-1 / gpt-4o-transcribe / gpt-4o-transcribe-diarize $0.006/min → **$360**; gpt-4o-mini-transcribe $0.003/min → **$180**; gpt-transcribe $0.0045/min → **$270** — [OpenAI pricing](https://developers.openai.com/api/docs/pricing)
- Deepgram Nova-3 monolingual pre-recorded $0.0043/min → **$258**; multilingual $0.0052 → **$312**; Whisper Cloud $0.0048 → **$288** — [Deepgram pricing](https://deepgram.com/pricing)
- AssemblyAI Universal-2 $0.15/hr → **$150** (+$20 with diarization) — [AssemblyAI pricing](https://www.assemblyai.com/pricing)
- ElevenLabs Scribe v2 $0.22/hr → **$220** PAYG (Business plan includes 4,500 hrs; plan fee not captured) — [ElevenLabs API pricing](https://elevenlabs.io/pricing/api)
- Rev.ai Reverb foreign-language $0.30/hr → **$300** — [Rev.ai pricing](https://www.rev.ai/pricing)
- Gladia Solaria-1 €0.27/hr → **€270** (→ €210 at 10k+ hrs) — [Gladia pricing](https://www.gladia.io/pricing)
- Groq whisper-large-v3-turbo $0.04/hr → **$40**; whisper-large-v3 $0.111/hr → **$111** — [Groq STT docs](https://console.groq.com/docs/speech-to-text)
- Cloudflare Workers AI whisper-large-v3-turbo $0.0005/min → **$30**, minus ~107 free hrs/month from the 10k neurons/day allowance → **≈ $27** — [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- Lelapa Vulavula: not computable per minute; SMME Pass $49/month covers 10,000 calls — if one call = one voice note, that is $49 for 10,000 notes regardless of length (unverified assumption) — [Vulavula plans](https://docs.lelapa.ai/overview/plans.md)

### Inferences
- Within the free-tool constraint, the cheapest paths are Whisper-based (Cloudflare/Groq, ~$30–40 per 1,000 hrs) but with the worst published Afrikaans accuracy (41.7% WER for Whisper Large v3 on FLEURS); the price-to-accuracy sweet spot on published evidence is Gemini 3.5 Transcribe (~$180–230) or ElevenLabs Scribe v2 ($220, "Good" tier), with Azure batch ($180) if in-country processing matters.

### Gaps
- Gemini output-token cost per minute of transcript is not included above (depends on transcript length; roughly 150–200 words/min).
- MAI-Transcribe-2, Soniox and Azure fast-transcription per-hour prices were not obtainable, so they are absent from the scenario.
