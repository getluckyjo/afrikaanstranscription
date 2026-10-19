# Test set (Phase 0, Step 2)

Audio and real transcripts are **never committed**; `.gitignore` excludes them. Only this README and the example manifest are tracked.

## Target

2–5 hours of consented audio that matches the real workload. Aim for roughly:

| Source | Hours | Notes |
|---|---|---|
| `online` | 1–2 | Zoom/Meet/Teams meetings captured from system audio, several speakers |
| `inperson` | 1–2 | Meetings recorded on a laptop or phone mic in a real room |
| `voicenote` | 0.5–1 | WhatsApp voice notes, exported as `.opus`, many different speakers |
| `read` | 0.5 (optional) | Scripted/read speech, for the formal register and proper nouns |

Include heavy Afrikaans–English code-switching in each source. Vary accents, microphones and background noise.

## Who does this

The collection and transcription job is described in `docs/DATA_LEAD_BRIEF.md`, written for the data lead.

## Consent

Every recording needs a signed `legal/CONSENT_RECORDING.md` from each participant, or a `legal/LICENCE_LETTER_CONTENT.md` from the copyright owner for existing content (for example a YouTube creator's own videos). Store signed forms outside the repo and reference them by `consent_id` in the manifest.

## Layout

```
data/raw/                 original files as received (git-ignored)
data/test/manifest.jsonl  one JSON object per clip (git-ignored; see example)
data/test/wav/            16 kHz mono WAV produced by benchmark/normalize.py
data/test/rttm/           reference speaker turns for meeting clips (optional, for DER)
```

## Manifest fields

```json
{"audio": "../raw/meeting-2026-10-21.m4a",
 "text": "Goeiemôre almal, kom ons begin met die agenda ...",
 "source": "inperson",
 "codeswitch": true,
 "speakers": 4,
 "consent_id": "C-0007",
 "split": "eval",
 "notes": "church council, phone on the table, aircon noise"}
```

- `audio`: path relative to the manifest file, or absolute.
- `text`: full verbatim transcript. Pick one spelling convention (AWS, the official Afrikaanse Woordelys en Spelreëls) and keep English words in their English spelling. Write numbers as words unless they are read as digits.
- `source`: `online`, `inperson`, `voicenote`, `read`.
- `codeswitch`: `true` if more than a few English words or phrases occur.
- `split`: `eval` for the 20% hold-out that is never used for fine-tuning; `dev` otherwise.

## Transcription tips

- Run the current best model first, then correct by hand; it is faster than typing from scratch.
- Keep hesitations (`uh`, `um`) out of the reference unless you decide to keep them everywhere.
- For meeting clips, also write a reference RTTM (speaker turns) if you want a diarization error rate. Audacity label tracks can be exported and converted.

## Clips 30 minutes or longer

Split long meetings into 5–10 minute segments at natural pauses so a single failed segment does not distort the score. Keep the same `consent_id` on each piece.
