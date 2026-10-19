# Build steps: free Afrikaans transcription tool

Step-by-step plan to go from nothing to a running, legally compliant, self-hosted Afrikaans transcription service for WhatsApp voice notes and meetings. Based on the research in `Afrikaans transcription tool feasibility.md`; see that report for sources and numbers behind every choice here.

Target architecture (what you are building toward):

```
User phone ──share/upload──► PWA (Next.js)  ──► R2 bucket (audio, 24–48 h TTL)
User phone ──Telegram bot──►  API            ──► Supabase (users, jobs, transcripts)
User phone ──WhatsApp bot──►  (Phase 2)      ──► GPU worker (serverless → dedicated)
                                                   ├─ ffmpeg → 16 kHz mono
                                                   ├─ faster-whisper + Fluister int8, language="af"
                                                   └─ pyannote 3.1 diarization (meetings only)
```

---

## Phase 0 — Prove the model and get legal (weeks 1–4)

### Step 1. Set up the legal basics before any real audio is processed

1. Register an Information Officer with the Information Regulator on its eServices portal. Sole proprietors and small businesses are not exempt.
2. Write three documents and keep them in the repo under `legal/`:
   - Privacy notice (what is collected, where it is processed, retention period, how to delete, cross-border transfer statement).
   - Consent text shown before first upload. Treat voice recordings conservatively as special personal information under POPIA and get explicit consent.
   - PAIA manual (required alongside the Information Officer registration).
3. Decide the retention policy now: audio deleted 24–48 hours after transcription, transcripts kept until the user deletes them. Write it into the notice.
4. Decide the section 72 cross-border ground. If your GPU is in the EU or US, you rely on user consent plus a data-processing agreement with the host and short retention. If you later move to in-country hosting, this requirement disappears.
5. For meetings, state in the UI that the uploader must be a participant (RICA single-party consent) and is responsible for informing others.

### Step 2. Build a real test set (the single highest-leverage task)

1. Collect 2–5 hours of consented audio that looks like your actual workload: WhatsApp voice notes (OGG/Opus, phone quality), a few phone-recorded meetings, and some code-switched Afrikaans-English speech. Friends, family, a church or community group are good sources. Get written consent and record it.
2. Transcribe it manually, or run the best model and correct by hand. Afrikaans spelling conventions matter; pick one and stick to it.
3. Store it as `data/test/manifest.jsonl` with one line per clip: `{"audio": "path.wav", "text": "...", "source": "voicenote|meeting", "codeswitch": true|false}`.
4. Hold back 20% as an untouched evaluation set. Never fine-tune on it.
5. Also download the AfriSwitch test set (code-switched Afrikaans) and FLEURS af_za for public comparison numbers.

### Step 3. Rent a GPU and benchmark the candidate models

1. Rent a 24 GB consumer GPU by the hour (Vast.ai RTX 4090 at roughly $0.13–0.49/hr, or RunPod). Budget 20–40 GPU-hours for this step.
2. Install the stack:

   ```bash
   pip install faster-whisper jiwer ctranslate2 huggingface_hub
   apt-get install -y ffmpeg
   ```

3. Normalise every test clip to 16 kHz mono PCM:

   ```bash
   ffmpeg -i in.opus -vn -ac 1 -ar 16000 -c:a pcm_s16le out.wav
   ```

4. Run each candidate with the language forced to Afrikaans (auto-detect flips segments to English or Dutch):

   ```python
   from faster_whisper import WhisperModel
   model = WhisperModel("digiphyte/fluister-turbo-ct2", device="cuda", compute_type="int8_float16")
   segments, info = model.transcribe("out.wav", language="af", beam_size=5, vad_filter=True)
   text = " ".join(s.text for s in segments)
   ```

   Candidates to run on the same test set:
   - `digiphyte/fluister-turbo` (MIT, large-v3-turbo, trained for code-switching) — expected default.
   - `BuzzASR/afrikaans` (MIT, large-v3).
   - `Sunbird/faster-whisper-51-african-languages` (Apache-2.0, gated; accept terms on Hugging Face first).
   - Stock `large-v3-turbo` as the baseline you expect to beat.
   - Optional paid comparison inside free tiers: ElevenLabs Scribe v2 (4.5 free hours/month). Do not send sensitive audio to Gemini's free tier; it trains on data.

5. Score with `jiwer` (WER and CER) after a shared normaliser (lowercase, strip punctuation). Record results in `data/benchmarks.md`.
6. Pick the model with the best WER on your voice-note and code-switched subsets, not on read speech. Expect 15–25% on clean notes and 25–36% on heavy code-switching at this stage.

### Step 4. Clear the data licences for later fine-tuning

1. Email the author of the `andreoosthuizen/afrikaans-30s` dataset to confirm commercial use is allowed; its card contradicts itself.
2. Confirm NCHLT Afrikaans (CC BY 3.0) and FLEURS attribution text for your notice.
3. Note in `legal/` that any model fine-tuned on WhatsApp-sourced audio must remain for your exclusive use (Meta Business Platform terms).

### Step 5. Optional public demo

Push a Gradio Space on Hugging Face ZeroGPU with the chosen model so early users can test quality for free while you build the product.

---

## Phase 1 — Share-sheet MVP (months 2–3)

### Step 6. Create the project skeleton

```
apps/web        Next.js PWA (Vercel Hobby or Cloudflare Pages)
apps/worker     Python GPU worker (Docker: ffmpeg + faster-whisper + model)
apps/bots       Telegram bot (Phase 1), WhatsApp bot (Phase 2)
packages/db     Supabase schema and migrations
legal/          privacy notice, consent, PAIA manual
data/           test manifests, benchmark results (audio never committed)
```

### Step 7. Provision the free-tier infrastructure

1. Supabase (Free): auth, Postgres, row-level security. Tables: `users`, `jobs` (id, user_id, status, source, duration_s, audio_key, created_at, expires_at), `transcripts` (job_id, text, segments jsonb, speakers jsonb).
2. Cloudflare R2 (Free, no egress fees): one bucket for incoming audio. Set a lifecycle rule to delete objects after 2 days as a safety net behind your own cleanup job.
3. Serverless GPU: RunPod Serverless (RTX 4090 class) or Modal (L4). Both bill per second and idle at zero cost.
4. Domain and email (for consent receipts and deletion confirmations).

### Step 8. Build the GPU worker

1. Dockerfile: CUDA base image, `ffmpeg`, `faster-whisper`, the chosen model converted to CTranslate2 int8 and baked into the image so cold starts do not download 1.5 GB.
2. Handler contract: input `{job_id, audio_url, mode: "voicenote"|"meeting"}`; output `{segments: [{start, end, text, speaker?}], language, duration_s}`.
3. Pipeline inside the handler:
   - Download from R2 via a signed URL.
   - `ffmpeg` to 16 kHz mono WAV.
   - For files over 10 minutes, split at silence (`ffmpeg -af silencedetect`) into roughly 10-minute chunks and transcribe sequentially with batched inference.
   - `transcribe(..., language="af", vad_filter=True, beam_size=5)`.
   - Delete local temp files; never log audio.
4. Test cold start and throughput; bake the model into the image if cold start exceeds about 20 seconds.

### Step 9. Build the PWA

1. Upload page accepting `.opus .ogg .m4a .mp3 .mp4 .wav .webm`, with chunked resumable upload (tus or multipart) straight to R2 via presigned URLs.
2. Register as an Android share target in `manifest.json` so a voice note goes WhatsApp → Share → your app in two taps:

   ```json
   "share_target": {
     "action": "/share",
     "method": "POST",
     "enctype": "multipart/form-data",
     "params": { "files": [{ "name": "audio", "accept": ["audio/*", ".opus", ".ogg", ".m4a"] }] }
   }
   ```

   The PWA must be installed for this to work. Add an install prompt on first visit.
3. iOS has no Web Share Target: show a short guide (long-press voice note → Forward → share icon → Save to Files → upload here).
4. Job flow: create `jobs` row → enqueue worker call → poll status → show transcript with copy, download `.txt`/`.docx`, and a "correct this transcript" editor.
5. Afrikaans-first UI with an English toggle.
6. Consent checkbox on first upload, with a link to the privacy notice. Optional "donate this recording to improve the model" checkbox, off by default, stored as a flag on the job.
7. Per-user cap, for example 60 minutes per month, enforced in the API before enqueueing.

### Step 10. Add the Telegram bot (free channel, zero approvals)

1. Create the bot with BotFather, store the token as a secret.
2. Set a webhook to your API. On a `voice` message, call `getFile`, download (20 MB limit), upload to R2, create a job, and reply with the transcript when done.
3. Same pipeline as the web app; Telegram voice notes are also OGG/Opus.

### Step 11. Retention and deletion jobs

1. Scheduled job (Supabase cron or Cloudflare Cron Trigger) every hour: delete R2 objects for jobs past `expires_at`, null out `audio_key`.
2. "Delete my data" button that removes transcripts, jobs and auth record in one transaction, and emails confirmation.
3. Log deletions (job id, time) without content, so you can demonstrate compliance.

### Step 12. Soft launch

1. Invite one or two community groups (a church, a school committee, a small business) as beta users.
2. Add a one-tap "was this transcript good?" rating and capture corrections from the editor (with consent) as future fine-tuning data.
3. Watch cost: at 100 audio hours per month this should run at roughly $10–25 per month in total.

---

## Phase 2 — WhatsApp bot, meetings, in-domain fine-tune (months 4–6)

### Step 13. WhatsApp Cloud API bot (direct to Meta, no BSP)

1. Create a Meta developer account and an app of type Business; add the WhatsApp product. A test number with up to 5 verified recipients is available immediately.
2. Implement the webhook: verify the `hub.challenge` handshake, then handle `messages[].type == "audio"` payloads. Fetch the media URL with `GET /<version>/<media_id>` using the bearer token and download it within 5 minutes (the URL expires).
3. Push the file through the same R2 → job → worker pipeline and reply with the transcript inside the 24-hour service window. Split long transcripts into as few messages as possible, because every reply beyond the free tier is billed.
4. Go to production: Business Portfolio → register your own number → display-name review (a day or two) → add a payment method. Business verification is only needed for business-initiated messaging, which a reply-only bot does not do.
5. Cost control: 1,000 service replies per number per month are free, after that about $0.0095 per reply in South Africa plus VAT. Enforce a per-user monthly cap on the bot and point heavy users to the PWA or Telegram, which cost nothing per message.
6. Read Meta's AI Providers policy and keep the bot narrow (transcription only, no general chat) to stay outside the restricted category.
7. If you register as a non-profit, service messages stay free until the end of 2027.

### Step 14. Meeting support

1. Accept long recordings via chunked resumable uploads. Tell iPhone users to record in Voice Memos and share the file; browser recording on iOS stops when the screen locks.
2. Add speaker diarization: accept the gated terms for `pyannote/speaker-diarization-3.1` and `pyannote/segmentation-3.0` on Hugging Face, add the token to the worker, run diarization on the full file, then assign each Whisper segment the speaker with the largest time overlap.
3. Export guidance for Zoom (cloud recording MP4), Google Meet (Drive "Meet Recordings" folder) and Teams (OneDrive/SharePoint). Skip meeting bots for now.
4. Transcript view with speaker labels, timestamps, rename-speaker, and `.docx` export.

### Step 15. Second-stage fine-tune on your own data

1. Assemble the training set: donated and corrected voice notes and meetings from Steps 9 and 12 (aim for 2–5 hours), plus the public corpora (NCHLT Afrikaans, afrikaans-30s once licensed, FLEURS). Keep the Step 2 evaluation set untouched.
2. Rent a 24 GB GPU for a day or two (about $20–45). Use `transformers` + `peft` LoRA on top of the Fluister (or chosen) weights, following the Hugging Face "fine-tune Whisper" recipe with forced language `af` and task `transcribe`. Use gradient checkpointing and 8-bit optimisers if memory is tight.
3. Evaluate against Step 3 numbers. Ship only if WER improves on the voice-note and code-switched subsets.
4. Convert the merged weights to CTranslate2 int8 (`ct2-transformers-converter --quantization int8_float16`), rebuild the worker image, and deploy behind a feature flag for an A/B comparison.
5. Keep the fine-tuned model private if any WhatsApp-sourced audio was used.

### Step 16. Freemium plan

1. Keep a permanent free tier (for example 60–120 minutes per month).
2. Add a paid tier (unlimited or high cap, diarization, priority) billed in rand through Paystack or Yoco. Price around R90–R180 per month.
3. Gate WhatsApp bot volume by plan so Meta reply fees are covered.

---

## Phase 3 — Scale and B2B (months 7–12)

### Step 17. Move to a dedicated GPU when it pays

When sustained volume passes roughly 5,000 audio hours per month, replace serverless with one always-on GPU: RunPod or Vast RTX 4090 ($250–650 per month) or Hetzner GEX45 in the EU (about €250 per month plus setup). Run a small queue (Redis or Postgres `SKIP LOCKED`) in front of it and keep serverless as overflow.

### Step 18. Evaluate in-country hosting

Price South African GPU hosting (Teraco-based providers, local clouds). If workable, moving processing in-country removes the section 72 cross-border requirement entirely and is a selling point for legal, medical and public-sector customers.

### Step 19. B2B offerings

Churches (sermon transcripts), legal practices, call centres, municipalities and schools are the sectors with evidence of Afrikaans transcription demand. Offer bulk upload, team workspaces, glossary (place names, surnames and numbers are Fluister's known weak spot) and data-processing agreements.

### Step 20. Optional advanced features

- Self-hosted Vexa (Apache-2.0) meeting bot for Google Meet if customers ask for live meeting joining; a Zoom bot needs a 4–6 week app review.
- Browser-only mode using transformers.js with WebGPU for privacy-sensitive users: audio never leaves the phone, at the cost of a 1.6 GB model download.
- Ongoing fine-tune cycle each quarter from corrected transcripts.

---

## Checklist of accounts and credentials you will need

| Item | When | Cost |
|---|---|---|
| Information Regulator IO registration | Step 1 | Free |
| Hugging Face account + accepted gated models (Sunbird, pyannote) | Step 3, 14 | Free |
| Vast.ai / RunPod account with credit | Step 3, 8, 15 | ~$10–45 per burst |
| Supabase project | Step 7 | Free tier |
| Cloudflare account (R2, optional Pages/Cron) | Step 7 | Free tier |
| Vercel or Cloudflare Pages | Step 9 | Free tier |
| Domain | Step 7 | ~R150–300/year |
| Telegram BotFather token | Step 10 | Free |
| Meta developer account, Business Portfolio, WhatsApp number, payment method | Step 13 | Free + per-reply fees after 1,000/month |
| Paystack or Yoco merchant account | Step 16 | Transaction fees only |

## Things to measure from day one

- WER on your own evaluation set, per model version.
- Cost per audio hour (GPU seconds × price ÷ hours transcribed).
- Audio deleted on schedule (count of objects older than the retention window should always be zero).
- WhatsApp replies per month against the 1,000 free allowance.
- User correction rate from the transcript editor, as the signal for the next fine-tune.
