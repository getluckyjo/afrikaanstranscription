# Build steps: Watsejy (watsejy.co.za), a local-first Afrikaans meeting transcriber

Step-by-step plan for a desktop app that listens to online or in-person meetings, transcribes Afrikaans (and Afrikaans-English code-switching) on the user's own machine, separates speakers, and lets the user name each speaker at the end. WhatsApp voice notes are handled by file sharing, and a WhatsApp bot is an optional late addition. Based on the research in `Afrikaans transcription tool feasibility.md`; see that report for sources and numbers.

Target architecture:

```
Desktop app (Mac, Windows; Linux later)
  ├─ Capture: microphone + system audio as two separate streams
  ├─ Store: local encrypted recording (FLAC/Opus), never uploaded by default
  ├─ Transcribe: whisper.cpp or faster-whisper + Fluister (Afrikaans fine-tune), language="af"
  ├─ Diarize: speaker segmentation on the "others" stream; "me" comes free from the mic stream
  ├─ Review: "who is who" screen → rename/merge speakers → editable transcript → export
  └─ Optional: cloud fallback for slow machines; opt-in data donation for fine-tuning

Mobile app (Phase 2): in-person recorder, on-device on recent phones, cloud fallback otherwise
Web upload (Phase 2): drag-and-drop for voice notes and exported Zoom/Meet/Teams recordings
Cloud worker (Phase 2): same model, used only for fallback, web upload and bots
```

---

## Phase 0 — Prove the model and get legal (weeks 1–4)

### Step 1. Legal basics

1. Register an Information Officer with the Information Regulator (eServices portal). Sole proprietors are not exempt.
2. Write and keep in `legal/`: privacy notice, consent text shown on first run, PAIA manual. Treat voice recordings conservatively as special personal information under POPIA.
3. Local-first processing means no cross-border transfer by default. Write the notice so that cloud fallback and data donation are clearly separate, opt-in choices with their own consent.
4. Recording a meeting you take part in is lawful under RICA (single-party consent). Put a visible "Recording" indicator and a one-click "notify participants" text in the app, because Zoom and Teams show no indicator for local capture.
5. Retention: recordings live on the user's disk under their control. If cloud fallback is used, audio is deleted within 24–48 hours of transcription.

### Step 2. Build a real test set (highest-leverage task)

1. Collect 2–5 hours of consented audio matching the real workload: recorded online meetings (system audio quality), in-person meetings on a laptop or phone mic, and WhatsApp voice notes. Include heavy Afrikaans-English code-switching.
2. Transcribe by hand or correct a model's output. Pick one Afrikaans spelling convention and stick to it. Label speakers and turn boundaries for the meeting files.
3. Store as `data/test/manifest.jsonl`: `{"audio": "...", "text": "...", "speakers": [...], "source": "online|inperson|voicenote", "codeswitch": true|false}`.
4. Hold back 20% as an untouched evaluation set.
5. Download the AfriSwitch and FLEURS af_za sets for public comparison numbers.

### Step 3. Benchmark the candidate models on a rented GPU and on real laptops

1. Rent an RTX 4090 by the hour (Vast.ai or RunPod, roughly $0.13–0.49/hr). Budget 20–40 GPU-hours.
2. Install `faster-whisper`, `jiwer`, `ctranslate2`, `ffmpeg`.
3. Normalise clips: `ffmpeg -i in -vn -ac 1 -ar 16000 -c:a pcm_s16le out.wav`.
4. Run each candidate with `language="af"` forced (auto-detect flips to English or Dutch):
   - `digiphyte/fluister-turbo` (MIT, large-v3-turbo, trained for code-switching; ships CTranslate2, MLX and Core ML builds) — expected default.
   - `digiphyte/fluister-medium` (smaller, for weak laptops; no published WER, so measure it).
   - `BuzzASR/afrikaans` (MIT, large-v3).
   - `Sunbird/faster-whisper-51-african-languages` (Apache-2.0, gated).
   - Stock `large-v3-turbo` as the baseline.
5. Score WER and CER with `jiwer` after a shared normaliser. Record in `data/benchmarks.md`.
6. Also run diarization on the meeting files with `pyannote/speaker-diarization-3.1` and record diarization error rate; this sets expectations for the "who is who" screen.
7. **Laptop test.** Convert the winner to GGML for whisper.cpp (`convert-h5-to-ggml.py` from the whisper.cpp repo) and to CTranslate2 int8. Time a 30-minute meeting on three real machines: a recent MacBook (Apple Silicon), a mid-range Windows laptop with no discrete GPU, and the cheapest laptop you expect users to own. Record real-time factor and peak RAM. This decides which model size ships by default and whether a cloud fallback is mandatory.

### Step 4. Clear data licences

1. Email the `andreoosthuizen/afrikaans-30s` author to confirm commercial use (its card contradicts itself).
2. Record NCHLT (CC BY 3.0) and FLEURS attribution text for the notice.
3. Any model fine-tuned on WhatsApp-sourced audio stays for your exclusive use (Meta Business Platform terms).

---

## Phase 1 — Desktop app MVP (months 2–4)

### Step 5. Choose the stack

- **Shell:** Tauri 2 (Rust core, small installer, web UI). Electron is acceptable if the team is JavaScript-only, at the cost of a larger download.
- **Inference:** whisper.cpp through the `whisper-rs` bindings, in-process, with Metal on Mac, CUDA or Vulkan where available, CPU otherwise. Alternative: a bundled Python sidecar running faster-whisper, which is simpler to prototype but heavier to ship.
- **Diarization:** either `sherpa-onnx` speaker diarization (ONNX, runs in Rust or C++ without Python) for a pure-native build, or a Python sidecar with pyannote 3.1 if you accept the sidecar. The pyannote route is the one benchmarked in the research; sherpa-onnx was not benchmarked and must be validated in Step 3's spirit before shipping.
- **Models bundled:** Fluister-turbo GGML int8 (about 1.5 GB) as default on capable machines, Fluister-medium as the low-end option, downloaded on first run rather than packed in the installer.
- **Storage:** SQLite for transcripts and metadata; recordings as FLAC in the app's data folder; optional OS-level encryption at rest.

### Step 6. Audio capture (the platform-specific core)

1. **Microphone** on all platforms via `cpal`.
2. **System audio** (what the other participants say):
   - macOS: ScreenCaptureKit audio capture (macOS 13+) or Core Audio process taps (14.2+). Requires the Screen Recording or audio capture permission; handle the permission prompt and explain why.
   - Windows: WASAPI loopback capture of the default render device.
   - Linux (later): PipeWire or PulseAudio monitor source.
3. Keep mic and system audio as **two separate 16 kHz mono streams** with a shared clock. The mic stream is "me"; the system stream is "everyone else". This halves the diarization problem for online meetings.
4. For in-person meetings there is only the mic stream, and all speakers go through diarization.
5. Write both streams to disk continuously so a crash never loses a meeting. Test a 3-hour recording for drift and memory.

### Step 7. Transcription pipeline

1. On "stop", or in rolling 30-second windows during the meeting for live preview, run whisper.cpp on each stream with `language = "af"`, VAD enabled, beam size 5.
2. Chunk long recordings at silence boundaries (roughly 10 minutes) and process sequentially; show progress.
3. Run diarization on the system stream (online) or the mic stream (in-person). Assign each transcript segment the speaker with the largest time overlap.
4. Merge both streams into one timeline ordered by start time, with "Me" pre-labelled from the mic stream.
5. Measure the end-to-end time on the Step 3 laptops. If a machine is slower than about 2x real time, offer the medium model or cloud fallback.

### Step 8. The "who is who" review screen

1. After processing, show each detected speaker with three short audio snippets and the first few lines they said.
2. Let the user type a name, merge two speakers that are the same person, and split a speaker if diarization fused two people.
3. Remember names per meeting title or calendar event so recurring meetings pre-fill.
4. Then show the full editable transcript with timestamps, click-to-play, find-and-replace, and a glossary for place names, surnames and numbers (Fluister's known weak spots).
5. Export to `.txt`, `.docx`, `.srt`, and clipboard. Optional summary generation is a later feature and would need either a local LLM or a cloud call with its own consent.

### Step 9. First-run, consent and settings

1. First run: language choice (Afrikaans UI first), privacy notice, consent, model download with size and disk space shown.
2. Settings: default model size, where recordings are stored, auto-delete recordings after N days, cloud fallback on/off (off by default), data donation on/off (off by default).
3. Data donation: when on, the user chooses per meeting whether to upload the audio and corrected transcript to you. This is the only way a local-first app feeds your fine-tuning.

### Step 10. Packaging, signing and updates

1. macOS: Apple Developer Program (about $99/year), notarise the build, hardened runtime with the microphone and screen-capture entitlements.
2. Windows: code-signing certificate (OV certificate roughly $200–400/year, or Azure Trusted Signing at about $10/month) to avoid SmartScreen warnings.
3. Auto-update through Tauri's updater with signed manifests.
4. Crash reporting without audio or transcript content.

### Step 11. Soft launch

1. Beta with two or three groups that hold regular Afrikaans meetings: a church council, a school governing body, a small law or accounting practice.
2. Collect the correction rate from the editor and the speaker-merge rate from the review screen; these are your quality signals.
3. Track model download completion, processing time per meeting-hour, and crash rate per platform.

---

## Phase 2 — Mobile, web upload, cloud fallback, fine-tune (months 5–8)

### Step 12. Cloud worker (only for fallback, web upload and bots)

1. Docker image with ffmpeg, faster-whisper and the Fluister CTranslate2 int8 model baked in; deploy on RunPod Serverless or Modal, which bill per second and idle at zero.
2. Same pipeline contract as the desktop app so transcripts look identical.
3. Audio in Cloudflare R2 with a 2-day lifecycle rule plus an hourly deletion job; no audio in logs.
4. Desktop "cloud fallback" uploads the FLAC, waits for segments, then runs the same review screen locally.

### Step 13. Web upload page

1. Small Next.js PWA on Vercel or Cloudflare Pages with Supabase auth: drag-and-drop any audio file (`.opus .ogg .m4a .mp3 .mp4 .wav .webm`), resumable upload to R2, job status, the same review and editor UI.
2. Register as an Android share target so a WhatsApp voice note goes Share → your app in two taps. iOS users save to Files and upload.
3. Instructions for exporting Zoom, Google Meet and Teams cloud recordings for users who did not run the desktop app during the call.
4. Per-user monthly cap on free cloud minutes (for example 60–120).

### Step 14. Mobile app for in-person meetings

1. iOS: native app using WhisperKit with the Fluister Core ML build; audio background mode so recording continues when the screen locks; on-device by default, cloud fallback on older devices.
2. Android: whisper.cpp through JNI, foreground service for recording; same review screen.
3. Share sheet / share target so WhatsApp voice notes can be sent straight to the app.
4. Sync transcripts (not audio) between phone and desktop through Supabase if the user signs in.

### Step 15. Second-stage fine-tune on donated data

1. Assemble donated and corrected meetings and voice notes (aim for 2–5 hours of in-domain audio) plus NCHLT, afrikaans-30s (once licensed) and FLEURS. Keep the Step 2 evaluation set untouched.
2. Rent a 24 GB GPU for a day or two (about $20–45). LoRA with `transformers` + `peft` on the Fluister weights, forced language `af`, task `transcribe`; gradient checkpointing and 8-bit optimisers if memory is tight.
3. Ship only if WER improves on the meeting and code-switched subsets.
4. Convert the merged model to GGML (desktop), Core ML (iOS) and CTranslate2 int8 (cloud); push through the in-app model updater as a new version.
5. Keep the fine-tuned model private if any WhatsApp-sourced audio was used.

### Step 16. Freemium and payments

1. Free forever: local transcription on the desktop app with a reasonable cap (for example 10 meeting-hours per month) or fully unlimited if you want the free tier to be the growth engine.
2. Paid (about R90–R180/month, billed through Paystack or Yoco): unlimited, cloud fallback minutes, mobile sync, glossary, team features.
3. Business: per-seat licences with a data-processing agreement and in-country or local-only processing guarantees.

---

## Phase 3 — WhatsApp bot, B2B and scale (months 9–12)

### Step 17. WhatsApp Cloud API bot (optional, direct to Meta, no BSP)

1. Only if users keep asking for it. Start on Meta's test number, handle the `audio` webhook, fetch the media URL within 5 minutes, push through the cloud worker, reply within the 24-hour window.
2. Production needs a Business Portfolio, your own number, display-name review and a payment method. Replies beyond 1,000 per number per month cost about $0.0095 each in South Africa plus VAT, so cap bot usage per user and steer heavy users to the apps.
3. Keep the bot narrow (transcription only) to stay clear of Meta's AI Providers policy.

### Step 18. Dedicated GPU and in-country hosting

1. Move cloud fallback to one always-on GPU when sustained volume passes roughly 5,000 audio hours per month ($250–650/month for a rented RTX 4090, or Hetzner GEX45 at about €250/month).
2. Price South African GPU hosting; local processing is already the default, but an in-country cloud fallback is a selling point for legal, medical and public-sector buyers.

### Step 19. B2B features

Team workspaces, shared glossaries, admin-controlled "local only" policy, audit log of deletions, bulk upload, and a signed data-processing agreement. Target churches, legal and accounting practices, call centres, municipalities and schools.

### Step 20. Later options

- Live captions during the meeting (rolling 30-second windows are already in Step 7; expose them in a small overlay).
- Local summaries with a small on-device LLM, or cloud summaries with explicit consent.
- Self-hosted Vexa meeting bot only if customers want a bot to join meetings they are not attending from a desktop.
- Expansion to isiZulu and isiXhosa, where open models are weaker and your data moat would be larger.

---

## Accounts, credentials and recurring costs

| Item | When | Cost |
|---|---|---|
| Information Regulator IO registration | Step 1 | Free |
| Hugging Face account, accepted gated models (Sunbird, pyannote) | Step 3 | Free |
| Vast.ai / RunPod credit for benchmarking and fine-tuning | Steps 3, 15 | ~$10–45 per burst |
| Apple Developer Program | Step 10 | ~$99/year |
| Windows code-signing (OV cert or Azure Trusted Signing) | Step 10 | ~$120–400/year |
| Domain, update server (static hosting) | Step 10 | ~R150–300/year + free tier |
| Supabase, Cloudflare R2, Vercel/Pages | Steps 12–13 | Free tiers, then ~$25/month |
| Serverless GPU for fallback and web upload | Step 12 | ~$1–50/month depending on volume |
| Paystack or Yoco merchant account | Step 16 | Transaction fees only |
| Meta developer account, number, payment method | Step 17 | Free + ~$0.0095 per reply after 1,000/month |

## What to measure from day one

- WER on the evaluation set per model version, split by online, in-person and code-switched.
- Diarization error rate and the user's speaker merge/split rate on the review screen.
- Processing time per meeting-hour per platform and model size.
- Share of users on cloud fallback (tells you whether local-only is realistic for your audience).
- Data donation opt-in rate and hours donated, the fuel for the next fine-tune.
- Crash rate and recording loss per platform.
