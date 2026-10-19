#!/usr/bin/env python3
"""Watsejy editor: drop an audio file, transcribe it, fix the text against the audio.

    python app/web.py                 # opens http://127.0.0.1:7861
    python app/web.py --port 8000

Everything runs on this machine. Uploads and corrected transcripts live under
~/Watsejy (override with WATSEJY_HOME).
"""
import argparse
import json
import shutil
import sys
import threading
import uuid
import webbrowser
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402

from fastapi import FastAPI, File, Form, HTTPException, UploadFile  # noqa: E402
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse  # noqa: E402
import uvicorn  # noqa: E402

STATIC = Path(__file__).resolve().parent / "static"
UPLOADS = engine.DATA_DIR / "uploads"
app = FastAPI(title="Watsejy")

JOBS: dict[str, dict] = {}
_LOCK = threading.Lock()


def _job(job_id: str) -> dict:
    j = JOBS.get(job_id)
    if not j:
        raise HTTPException(404, "unknown job")
    return j


def _run(job_id: str, speakers: bool, num_speakers: Optional[int]) -> None:
    j = JOBS[job_id]

    def say(m: str) -> None:
        j["message"] = m

    try:
        src = Path(j["path"])
        say("Converting audio…")
        wav = engine.to_wav16k(src, src.parent)          # kept for playback (plays in every browser)
        j["wav"] = str(wav)
        t = engine.transcribe(src, speakers=speakers, num_speakers=num_speakers, progress=say)
        j["transcript"] = t
        j["status"] = "done"
        speed = t.duration_s / t.elapsed_s if t.elapsed_s else 0
        say(f"Klaar: {engine._hms(t.duration_s)} oudio in {t.elapsed_s:.0f}s ({speed:.1f}x intyds) · {t.model}")
    except Exception as e:  # surfaced to the page
        j["status"] = "error"
        j["message"] = str(e)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (STATIC / "editor.html").read_text(encoding="utf-8")


@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...), speakers: bool = Form(False), num_speakers: int = Form(0)):
    job_id = uuid.uuid4().hex[:10]
    d = UPLOADS / job_id
    d.mkdir(parents=True, exist_ok=True)
    name = Path(file.filename or "opname").name
    dst = d / name
    with dst.open("wb") as out:
        shutil.copyfileobj(file.file, out)
    with _LOCK:
        JOBS[job_id] = {"id": job_id, "status": "running", "message": "Queued…", "path": str(dst), "name": name}
    threading.Thread(target=_run, args=(job_id, speakers, num_speakers or None), daemon=True).start()
    return {"id": job_id}


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):
    j = _job(job_id)
    out = {"id": job_id, "status": j["status"], "message": j.get("message", ""), "name": j["name"]}
    t = j.get("transcript")
    if t:
        out["transcript"] = {
            "duration_s": t.duration_s, "engine": t.engine, "model": t.model,
            "speakers": t.speakers,
            "segments": [{"start": s.start, "end": s.end, "speaker": s.speaker, "text": s.text.strip()} for s in t.segments],
        }
    return out


@app.get("/api/jobs/{job_id}/audio")
def job_audio(job_id: str):
    j = _job(job_id)
    wav = j.get("wav")
    if not wav or not Path(wav).exists():
        raise HTTPException(404, "audio not ready")
    return FileResponse(wav, media_type="audio/wav")


def _apply_edits(j: dict, segments: list[dict]) -> engine.Transcript:
    t: engine.Transcript = j["transcript"]
    t.segments = [engine.Segment(float(s["start"]), float(s["end"]), str(s.get("text", "")), (s.get("speaker") or None))
                  for s in segments if str(s.get("text", "")).strip()]
    return t


@app.post("/api/jobs/{job_id}/export")
async def export(job_id: str, payload: dict):
    j = _job(job_id)
    if not j.get("transcript"):
        raise HTTPException(409, "not transcribed yet")
    t = _apply_edits(j, payload.get("segments", []))
    fmt = payload.get("fmt", "txt")
    body = {"txt": t.to_txt, "md": t.to_md, "srt": t.to_srt, "json": t.to_json}.get(fmt)
    if not body:
        raise HTTPException(400, "fmt must be txt, md, srt or json")
    stem = Path(j["name"]).stem
    return PlainTextResponse(body(), headers={"Content-Disposition": f'attachment; filename="{stem}.{fmt}"'})


@app.post("/api/jobs/{job_id}/save")
async def save(job_id: str, payload: dict):
    j = _job(job_id)
    if not j.get("transcript"):
        raise HTTPException(409, "not transcribed yet")
    t = _apply_edits(j, payload.get("segments", []))
    row = engine.save_correction(
        j["path"], t.to_txt(), source=payload.get("source", "unknown"),
        codeswitch=payload.get("codeswitch"), transcript=t,
    )
    return JSONResponse({"ok": True, "row": row, "dir": str(engine.DATA_DIR)})


@app.get("/api/info")
def info():
    return {"engine": engine.pick_engine(), "data_dir": str(engine.DATA_DIR),
            "speakers_available": bool(__import__("os").environ.get("HF_TOKEN"))}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=7861)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()
    UPLOADS.mkdir(parents=True, exist_ok=True)
    url = f"http://127.0.0.1:{args.port}"
    if not args.no_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print(f"Watsejy editor at {url}  (Ctrl+C to stop)")
    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
