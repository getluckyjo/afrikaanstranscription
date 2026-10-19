# Watsejy data lead brief

_For Pietie Beyers. A working brief for the person who collects and transcribes the Afrikaans speech that Watsejy is measured and trained on. Johannes owns the project; this document says what the data job is, why it matters more than anything else in Phase 0, and how to do it so the recordings are legally usable._

## Why this job decides the product

Watsejy turns Afrikaans meetings and WhatsApp voice notes into text on the user's own device. The speech models we start from are public and anyone can use them. What nobody has is a few hours of real, consented, carefully transcribed Afrikaans as people actually speak it in meetings and voice notes: fast, mixed with English, over a phone mic, with background noise. Research we rely on found that five minutes of audio that matches the real use case taught a model as much as fifty hours that did not. The person who builds that dataset builds the only thing about Watsejy that cannot be copied.

## Why an actor, and the one trap

An actor brings an ear for register and accent, comfort with microphones, a network of Afrikaans speakers across ages and regions, and the judgement to hear when a transcript is wrong. All of that is exactly what the job needs.

The trap is performance. The model must learn ordinary speech, not delivered speech. A scene, a monologue or a read script is clean and expressive, and the models already handle that kind of audio well. What they fail on is the hesitant, overlapping, half-English talk of a real committee meeting. So the rule is: **collect conversations, never performances.** Pietie's craft is used to recruit, to set people at ease, and to hear errors, not to produce the audio himself.

## What to collect

### Phase 0 target: 2 to 5 hours by week 4

| Source | Hours | What it looks like |
|---|---|---|
| Online meetings | 1 to 2 | Zoom, Meet or Teams calls, recorded from the computer, three to six people |
| In-person meetings | 1 to 2 | A laptop or phone on the table in a real room: church council, school committee, production meeting, family planning a function |
| WhatsApp voice notes | 0.5 to 1 | Real voice notes people agree to share, from many different senders |
| Read speech | up to 0.5, optional | Someone reading a formal text with place names, surnames and numbers; a small set only |

### Phase 2 target: 20 to 50 hours over the following months

Same mix, more speakers, plus recordings donated through the app once it exists.

### Speaker variety matters more than hours

Aim for spread across all of these, and keep a tally:

- Age: under 25, 25 to 50, over 50.
- Gender.
- Region and variety: Western Cape, Northern Cape, Gauteng and Pretoria, Free State, Namibia; Kaaps and other Cape varieties as well as standard Afrikaans.
- Code-switching: at least a third of the material should mix English in freely.
- Microphone: phone, laptop, earbuds, a bad connection on a call.

Ten speakers for one hour each beats one speaker for ten hours.

## How to record

- **In person:** a phone in Voice Memos or any recorder app, placed on the table. Do not use noise suppression. Keep the original file.
- **Online meetings:** record the meeting from the host's side (cloud recording) or with a desktop recorder that captures system audio. Export as the original file; do not convert.
- **Voice notes:** ask the sender to forward the note or share the file. On Android the file is under `WhatsApp/Media/WhatsApp Voice Notes/`; on iPhone, long-press, Forward, share icon, Save to Files.
- **Formats:** anything is fine (m4a, mp3, opus, wav, mp4). Never re-encode.
- **Naming:** `YYYY-MM-DD_source_shortdescription.ext`, for example `2026-11-03_inperson_kerkraad.m4a`.
- **Storage:** one shared, access-controlled folder agreed with Johannes. Never email recordings around and never post them in a group chat.

## Consent is the job, not an afterthought

Every voice in every recording belongs to someone, and under POPIA a voice recording is treated as sensitive personal information. Nothing can be used without a signed form.

1. Before recording, each participant signs `legal/CONSENT_RECORDING.md`. For a meeting, every person signs their own form.
2. For existing recordings someone already owns (a podcast, a YouTube channel), the owner signs `legal/LICENCE_LETTER_CONTENT.md`.
3. Both forms state what the audio is for and what it is not for. In particular, **the recordings will never be used to synthesise, clone or imitate anyone's voice.** They train a model that listens; they will never train one that speaks. This matters to actors and should be said out loud when asking.
4. Give each signed form a number (`C-0001`, `C-0002` …), store the forms in a folder separate from the audio, and write the number on every recording that it covers.
5. Anyone can withdraw later. Keep contact details so the recording can be found and deleted.

## Transcription conventions

A transcript is only useful if everyone writes the same way. The rules:

- **Spelling:** standard Afrikaans per the Afrikaanse Woordelys en Spelreëls. English words and phrases are written in English spelling, exactly as said (`ons het 'n meeting gehad`, not `vergadering`).
- **Numbers:** as words, unless the speaker clearly reads digits (a phone number, an amount read off a page).
- **Fillers:** leave out `uh`, `um`, `ja-nee` as pure filler; keep words that carry meaning.
- **Repetitions and false starts:** write what was said, including restarts, but do not mark them specially.
- **Unclear speech:** write `[onduidelik]` for a stretch nobody can make out; do not guess.
- **Speakers:** label turns in meetings as `SPREKER 1`, `SPREKER 2` …, consistent within one recording. Note the real names only on the consent register, never in the transcript.
- **Punctuation:** normal sentence punctuation. Capital letters for names and sentence starts.
- **No cleaning up:** do not fix grammar, do not translate, do not tidy sentences.

## The fastest way to transcribe

Typing verbatim from scratch takes six to ten hours per hour of audio. Correcting a good machine transcript takes two to three. The workflow:

1. Johannes runs each recording through the current best model and sends back a draft with timestamps.
2. Pietie listens and corrects the draft against the audio, applying the conventions above.
3. Mark speaker turns for meeting recordings.
4. Return the corrected text; it goes into the manifest with the recording's consent number.

Any free editor works for Phase 0 (a text file beside the audio). If volume grows, a dedicated tool with click-to-play per line will be set up.

## What "done" looks like each week

- A tally sheet: hours collected by source, speakers by age, gender, region and variety, hours transcribed.
- Signed forms filed and numbered.
- Corrected transcripts returned with the recording name and consent number.

## Credit and compensation

[To agree between Johannes and Pietie: hourly or per-audio-hour rate, or a share in the project, plus a named credit in the app's About screen and the attribution file.]

## Contacts

- Project owner: Johannes, [email]
- Information Officer (for any privacy question or withdrawal request): [name, email]

---

### Kort opsomming in Afrikaans

Watsejy maak Afrikaanse vergaderings en WhatsApp-stemboodskappe teks, op die gebruiker se eie toestel. Die taak: versamel 2 tot 5 uur egte, natuurlike Afrikaanse gesprekke (vergaderings aanlyn en in persoon, stemboodskappe) van soveel verskillende sprekers as moontlik, met toestemmingsvorms vir elke stem, en korrigeer die masjientranskripsies volgens die spelreëls hierbo. Geen voorlesings of toneelspel nie; gewone praat is wat tel. Die opnames word nooit gebruik om iemand se stem na te boots nie.
