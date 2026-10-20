# Watsejy on your Mac (personal MVP)

Transcribe Afrikaans voice notes and meetings on your own machine. Nothing is uploaded anywhere. This is the Phase 1 stand-in from `reports/Build steps.md`: it proves the model on your real audio before any app or company exists.

## 1. Install (once, about 10 minutes)

```bash
# Homebrew tools
brew install ffmpeg python@3.12

# Python environment inside the repo
cd afrikaanstranscription
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements-mac.txt
```

The first transcription downloads the Fluister turbo model (about 1.6 GB) into `~/.cache/huggingface`. After that it runs offline.

## 2. Transcribe a voice note

```bash
source .venv/bin/activate
python app/watsejy.py ~/Downloads/PTT-20261019-WA0003.opus
```

The transcript prints to the terminal and is written next to the file as `.txt` and `.md`. Add `--formats txt,md,srt,json` for subtitles or raw JSON.

## 3. Meetings with speaker labels (optional setup)

1. On huggingface.co, accept the terms of `pyannote/speaker-diarization-3.1` and `pyannote/segmentation-3.0`.
2. Create a read token under Settings → Access Tokens.
3. Put it in your shell:

```bash
echo 'export HF_TOKEN=hf_your_token_here' >> ~/.zshrc && source ~/.zshrc
```

Then:

```bash
python app/watsejy.py meeting.m4a --speakers              # auto-detect how many people
python app/watsejy.py meeting.m4a --speakers --num-speakers 4
```

Speakers come out as `SPREKER 1`, `SPREKER 2` …; rename them in the page (next step) or with find-and-replace.

## 4. The editor: drop a file, fix the text against the audio

```bash
python app/web.py
```

A browser tab opens at http://127.0.0.1:7861. Drag a voice note or recording onto the page (tick "Benoem sprekers" first for meetings). The transcript is cut into short lines of a few seconds each, using word timestamps, so every line is a quick listen.

The correction loop is: the line plays, you fix the text, you press `Enter`. That marks the line as checked and jumps to the next one, which starts playing. A counter in the player bar shows how many lines are checked.

- Clicking into a line plays it ("Speel by kies"). Click a timestamp to play from there.
- `Esc` plays or pauses. `⌘Enter` replays the line. `⟳ Herhaal` loops it. `⌘←` goes back three seconds. The speed menu slows fast talkers.
- `⌘↓` / `⌘↑` moves between lines. `⌘D` toggles the checked mark. "Volg oudio" scrolls the page along with playback when you are not typing.
- `Shift+Enter` splits a line at the cursor; `⌘⇧M` (or the ⤓ button) merges a line with the next one. Use these when the automatic cut lands in the wrong place.
- Rename speakers once for the whole file with `1=Johannes, 2=Carla`, or type a name on any line.
- Your edits are kept as a draft in the browser as you type, so a refresh or a crash does not lose them. Download `.txt`, `.md` or `.srt`, or copy the plain text.

The older one-box page is still there if you prefer it: `python app/ui.py` (port 7860). Its `--share` flag prints a temporary public link that routes to your Mac, which is the simplest way to let Carla try it for a session. Only share audio that way with people who have consented.

## 4b. Desktop shortcut (no Terminal needed after this)

Once, from the project folder:

```bash
bash app/mac/install_shortcut.sh
```

That builds a small **Watsejy** app on your Desktop with its own icon. Double-click it to start: a Terminal window opens with the server, the browser opens on the editor, and closing that window stops it. If Watsejy is already running, the shortcut just opens the browser again. Re-run the command after updates; it rebuilds the app in place. If the icon looks generic after the first build, run `killall Finder` once.

## 5. Build the test set while you work

When a transcript is corrected, pick the source at the bottom of the editor (stemboodskap, vergadering in persoon, aanlyn vergadering, voorgelees), tick the code-switching box if there is a lot of English, and press **Stoor na ~/Watsejy**. This copies the audio to `~/Watsejy/audio/`, writes the corrected text to `~/Watsejy/transcripts/`, and appends a row to `~/Watsejy/corrections.jsonl` in the same shape as `data/test/manifest.jsonl`. Uploads sit in `~/Watsejy/uploads/` and can be deleted at any time. When you have a few hours of corrections, that file is the benchmark test set, and later the fine-tuning data.

Add `consent_id` to rows for recordings of other people once their forms are signed.

## 6. Recording meetings on a Mac

- **In person:** Voice Memos on your phone or the Mac, placed on the table. Share the file to the Mac.
- **Zoom / Meet / Teams you host:** use the platform's recording and download the file afterwards.
- **Online meetings you do not host:** QuickTime records the microphone only. To capture the other side's audio, install the free BlackHole virtual audio driver and set up a multi-output device, or record with OBS. The desktop app in Phase 1 does this natively; for now a cloud recording is simpler.

## Models and engines

| Situation | Engine | Model |
|---|---|---|
| Apple Silicon (M1 or later) | mlx-whisper | `digiphyte/fluister-turbo-mlx` |
| Intel Mac | faster-whisper on CPU | `digiphyte/fluister-turbo` |
| Low-end machine | faster-whisper | `--model digiphyte/fluister-medium` |

Override with `--engine`, `--model`, or the `WATSEJY_MLX_MODEL` / `WATSEJY_CT2_MODEL` environment variables. The language is forced to Afrikaans (`af`); English words still come through, but auto-detect would flip whole segments to English or Dutch.

## Troubleshooting

- `ffmpeg not found`: `brew install ffmpeg`.
- Speaker labelling fails with a 401 or "could not load": accept both pyannote model terms on Hugging Face and check `echo $HF_TOKEN`.
- First run is slow: it is downloading the model. Later runs on an M-series Mac are several times faster than real time.
- Transcript comes out in Dutch spelling or English: you are not running the Fluister model. Check the model name printed in the status line.
