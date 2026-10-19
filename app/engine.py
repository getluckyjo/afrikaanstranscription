"""Watsejy personal engine: one audio file in, Afrikaans transcript with speakers out.

Runs entirely on the Mac. Apple Silicon uses mlx-whisper with the Fluister
turbo model; anything else falls back to faster-whisper on CPU. Speaker
labelling uses pyannote and needs a Hugging Face token (HF_TOKEN).

Used by watsejy.py (command line) and ui.py (drag-and-drop page).
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
import time
import wave
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Optional

DEFAULT_MLX_MODEL = os.environ.get("WATSEJY_MLX_MODEL", "digiphyte/fluister-turbo-mlx")
DEFAULT_CT2_MODEL = os.environ.get("WATSEJY_CT2_MODEL", "digiphyte/fluister-turbo")
DEFAULT_DIAR_MODEL = os.environ.get("WATSEJY_DIARIZATION_MODEL", "pyannote/speaker-diarization-3.1")
DATA_DIR = Path(os.environ.get("WATSEJY_HOME", Path.home() / "Watsejy"))
SPEAKER_PREFIX = "SPREKER"

Progress = Optional[Callable[[str], None]]


def _say(progress: Progress, msg: str) -> None:
    if progress:
        progress(msg)


# ---------------------------------------------------------------- data types

@dataclass
class Segment:
    start: float
    end: float
    text: str
    speaker: Optional[str] = None


@dataclass
class Transcript:
    source: str
    duration_s: float
    engine: str
    model: str
    language: str
    segments: list[Segment] = field(default_factory=list)
    elapsed_s: float = 0.0
    diarization_model: Optional[str] = None

    @property
    def speakers(self) -> list[str]:
        seen: list[str] = []
        for s in self.segments:
            if s.speaker and s.speaker not in seen:
                seen.append(s.speaker)
        return seen

    def plain_text(self) -> str:
        return " ".join(s.text.strip() for s in self.segments if s.text.strip())

    def to_txt(self) -> str:
        lines = []
        for s in self.segments:
            who = f"{s.speaker}: " if s.speaker else ""
            lines.append(f"[{_hms(s.start)}] {who}{s.text.strip()}")
        return "\n".join(lines) + "\n"

    def to_md(self) -> str:
        head = [
            f"# {Path(self.source).name}",
            "",
            f"_Duur {_hms(self.duration_s)} · {self.engine} · {self.model} · verwerk in {self.elapsed_s:.0f}s_",
            "",
        ]
        body = []
        cur_speaker, cur_start, buf = None, None, []
        for s in self.segments:
            if s.speaker != cur_speaker and buf:
                body.append(_md_para(cur_speaker, cur_start, buf))
                buf = []
            if not buf:
                cur_speaker, cur_start = s.speaker, s.start
            buf.append(s.text.strip())
        if buf:
            body.append(_md_para(cur_speaker, cur_start, buf))
        return "\n".join(head + body) + "\n"

    def to_srt(self) -> str:
        out = []
        for i, s in enumerate(self.segments, 1):
            who = f"{s.speaker}: " if s.speaker else ""
            out.append(f"{i}\n{_srt_ts(s.start)} --> {_srt_ts(s.end)}\n{who}{s.text.strip()}\n")
        return "\n".join(out)

    def to_json(self) -> str:
        d = asdict(self)
        d["speakers"] = self.speakers
        return json.dumps(d, ensure_ascii=False, indent=2)


def _md_para(speaker: Optional[str], start: Optional[float], parts: list[str]) -> str:
    who = f"**{speaker}**  " if speaker else ""
    return f"{who}`{_hms(start or 0)}`  \n{' '.join(parts)}\n"


def _hms(sec: float) -> str:
    sec = max(0, int(round(sec)))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def _srt_ts(sec: float) -> str:
    ms = int(round(max(0.0, sec) * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ---------------------------------------------------------------- audio prep

def ffmpeg_path() -> str:
    p = shutil.which("ffmpeg")
    if not p:
        raise RuntimeError("ffmpeg not found. Install it with:  brew install ffmpeg")
    return p


def to_wav16k(src: Path, dst_dir: Path) -> Path:
    """Convert any audio/video file to 16 kHz mono 16-bit PCM WAV."""
    dst = dst_dir / (src.stem + ".16k.wav")
    subprocess.run(
        [ffmpeg_path(), "-y", "-loglevel", "error", "-i", str(src),
         "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dst)],
        check=True,
    )
    return dst


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def load_wav16k(path: Path):
    """Read a 16 kHz mono 16-bit WAV into a float32 numpy array in [-1, 1].

    Feeding samples directly means neither engine has to decode audio itself,
    which sidesteps PyAV/ffmpeg version mismatches."""
    import numpy as np

    with wave.open(str(path), "rb") as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == 16000, "expected 16 kHz mono PCM16"
        data = w.readframes(w.getnframes())
    return np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0


# ---------------------------------------------------------------- engines

def pick_engine() -> str:
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            import mlx_whisper  # noqa: F401
            return "mlx"
        except ImportError:
            pass
    return "ct2"


def _transcribe_mlx(wav: Path, model: str, language: str) -> list[Segment]:
    import mlx_whisper

    result = mlx_whisper.transcribe(
        load_wav16k(wav),
        path_or_hf_repo=model,
        language=language,
        task="transcribe",
        condition_on_previous_text=False,
        word_timestamps=True,
    )
    words = [(float(w["start"]), float(w["end"]), str(w["word"]))
             for s in result.get("segments", []) for w in (s.get("words") or [])]
    if words:
        return rechunk(words)
    return [Segment(float(s["start"]), float(s["end"]), s["text"]) for s in result.get("segments", [])]


_CT2_CACHE: dict[str, object] = {}


def _transcribe_ct2(wav: Path, model: str, language: str) -> list[Segment]:
    from faster_whisper import WhisperModel

    m = _CT2_CACHE.get(model)
    if m is None:
        m = WhisperModel(model, device="cpu", compute_type="int8")
        _CT2_CACHE[model] = m
    segments, _info = m.transcribe(load_wav16k(wav), language=language, beam_size=5, vad_filter=True,
                                   condition_on_previous_text=False, word_timestamps=True)
    segments = list(segments)
    words = [(float(w.start), float(w.end), str(w.word)) for s in segments for w in (s.words or [])]
    if words:
        return rechunk(words)
    return [Segment(float(s.start), float(s.end), s.text) for s in segments]


def rechunk(words, max_dur: float = 9.0, max_chars: int = 140, pause: float = 0.7, min_dur: float = 2.0) -> list[Segment]:
    """Cut a word stream into short editable lines.

    Breaks after sentence punctuation once a line is at least `min_dur` long,
    at silences longer than `pause`, and never lets a line run past `max_dur`
    seconds or `max_chars` characters."""
    out: list[Segment] = []
    cur: list[tuple[float, float, str]] = []

    def flush():
        if cur:
            text = "".join(w for _, _, w in cur).strip()
            if text:
                out.append(Segment(cur[0][0], cur[-1][1], text))
        cur.clear()

    for i, (ws, we, wt) in enumerate(words):
        if not wt.strip():
            continue
        cur.append((ws, we, wt))
        dur = we - cur[0][0]
        chars = sum(len(w) for _, _, w in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt[0] - we) if nxt else 0.0
        ends_sentence = wt.rstrip().endswith((".", "?", "!"))
        if (ends_sentence and dur >= min_dur) or (gap > pause and dur >= min_dur) or dur >= max_dur or chars >= max_chars:
            flush()
    flush()
    return out


# ---------------------------------------------------------------- diarization

def diarize(wav: Path, num_speakers: Optional[int] = None, model: str = DEFAULT_DIAR_MODEL) -> list[tuple[float, float, str]]:
    """Return speaker turns as (start, end, label). Needs HF_TOKEN and accepted model terms."""
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        raise RuntimeError(
            "Speaker labelling needs a Hugging Face token. Accept the terms of "
            f"{model} and pyannote/segmentation-3.0 on huggingface.co, then run:  export HF_TOKEN=hf_..."
        )
    from pyannote.audio import Pipeline

    try:
        pipeline = Pipeline.from_pretrained(model, token=token)
    except TypeError:  # older pyannote.audio
        pipeline = Pipeline.from_pretrained(model, use_auth_token=token)
    if pipeline is None:
        raise RuntimeError(f"Could not load {model}. Have you accepted its terms on Hugging Face?")

    try:
        import torch
        if torch.backends.mps.is_available():
            pipeline.to(torch.device("mps"))
    except Exception:
        pass

    kwargs = {"num_speakers": num_speakers} if num_speakers else {}
    result = pipeline(str(wav), **kwargs)
    annotation = getattr(result, "speaker_diarization", result)  # pyannote 4.x wraps the output
    turns = [(float(seg.start), float(seg.end), str(label))
             for seg, _track, label in annotation.itertracks(yield_label=True)]
    turns.sort()
    return turns


def assign_speakers(segments: list[Segment], turns: list[tuple[float, float, str]]) -> None:
    """Give each segment the speaker with the largest time overlap, renumbered in order of appearance."""
    mapping: dict[str, str] = {}
    for seg in segments:
        best, best_ov = None, 0.0
        for start, end, label in turns:
            ov = min(seg.end, end) - max(seg.start, start)
            if ov > best_ov:
                best, best_ov = label, ov
        if best is None and turns:  # no overlap (e.g. VAD trimmed): nearest turn by midpoint
            mid = (seg.start + seg.end) / 2
            best = min(turns, key=lambda t: min(abs(t[0] - mid), abs(t[1] - mid)))[2]
        if best is not None:
            if best not in mapping:
                mapping[best] = f"{SPEAKER_PREFIX} {len(mapping) + 1}"
            seg.speaker = mapping[best]


# ---------------------------------------------------------------- main entry

def transcribe(
    path: str | Path,
    *,
    engine: Optional[str] = None,
    model: Optional[str] = None,
    language: str = "af",
    speakers: bool = False,
    num_speakers: Optional[int] = None,
    progress: Progress = None,
) -> Transcript:
    src = Path(path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(src)
    engine = engine or pick_engine()
    model = model or (DEFAULT_MLX_MODEL if engine == "mlx" else DEFAULT_CT2_MODEL)

    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix="watsejy-") as tmp:
        _say(progress, "Converting audio…")
        wav = to_wav16k(src, Path(tmp))
        duration = wav_duration(wav)

        _say(progress, f"Transcribing with {model} ({engine})… first run downloads the model")
        segs = _transcribe_mlx(wav, model, language) if engine == "mlx" else _transcribe_ct2(wav, model, language)
        segs = [s for s in segs if s.text.strip()]

        diar_model = None
        if speakers and segs:
            _say(progress, "Labelling speakers…")
            turns = diarize(wav, num_speakers=num_speakers)
            assign_speakers(segs, turns)
            diar_model = DEFAULT_DIAR_MODEL

    return Transcript(
        source=str(src), duration_s=duration, engine=engine, model=model, language=language,
        segments=segs, elapsed_s=time.time() - t0, diarization_model=diar_model,
    )


# ---------------------------------------------------------------- editing helpers

_RENAME_RE = re.compile(r"^\s*(\d+)\s*[=:]\s*(.+?)\s*$")


def parse_rename(spec: str) -> dict[str, str]:
    """'1=Johannes, 2=Pietie' -> {'SPREKER 1': 'Johannes', 'SPREKER 2': 'Pietie'}."""
    out = {}
    for part in re.split(r"[,\n;]", spec or ""):
        m = _RENAME_RE.match(part)
        if m:
            out[f"{SPEAKER_PREFIX} {m.group(1)}"] = m.group(2)
    return out


def rename_speakers_in_text(text: str, mapping: dict[str, str]) -> str:
    for old, new in sorted(mapping.items(), key=lambda kv: -len(kv[0])):
        text = re.sub(rf"(?<![\w]){re.escape(old)}(?=\s*:)", new, text)
        text = re.sub(rf"\*\*{re.escape(old)}\*\*", f"**{new}**", text)
    return text


_LINE_RE = re.compile(r"^\s*\[\d+:\d{2}(?::\d{2})?\]\s*(?:[^:\n]{1,40}:\s*)?")


def strip_labels(txt: str) -> str:
    """Turn the editable [time] SPEAKER: text format back into plain running text."""
    parts = []
    for line in txt.splitlines():
        line = _LINE_RE.sub("", line).strip()
        if line:
            parts.append(line)
    return " ".join(parts)


# ---------------------------------------------------------------- saving corrections

def save_correction(
    audio_path: str | Path,
    corrected_txt: str,
    *,
    source: str = "unknown",
    codeswitch: Optional[bool] = None,
    transcript: Optional[Transcript] = None,
    data_dir: Path = DATA_DIR,
) -> dict:
    """Store the audio and your corrected transcript as a test-set row under ~/Watsejy."""
    audio_path = Path(audio_path).expanduser().resolve()
    audio_dir = data_dir / "audio"
    text_dir = data_dir / "transcripts"
    audio_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    stamp = _dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    stem = f"{stamp}_{re.sub(r'[^A-Za-z0-9_-]+', '-', audio_path.stem)[:40]}"
    audio_copy = audio_dir / f"{stem}{audio_path.suffix.lower()}"
    if not audio_copy.exists():
        shutil.copy2(audio_path, audio_copy)
    (text_dir / f"{stem}.txt").write_text(corrected_txt, encoding="utf-8")

    row = {
        "audio": str(audio_copy),
        "text": strip_labels(corrected_txt),
        "transcript_txt": str(text_dir / f"{stem}.txt"),
        "source": source,
        "codeswitch": codeswitch,
        "consent_id": None,
        "split": "dev",
        "saved_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "engine": transcript.engine if transcript else None,
        "model": transcript.model if transcript else None,
        "duration_s": round(transcript.duration_s, 2) if transcript else None,
    }
    with (data_dir / "corrections.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row
