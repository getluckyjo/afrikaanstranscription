#!/usr/bin/env python3
"""Watsejy drag-and-drop page (Gradio), running locally on your Mac.

    python app/ui.py            # opens http://127.0.0.1:7860
    python app/ui.py --share    # also prints a temporary public link (for Pietie)

Drop a voice note or meeting recording, get an editable transcript with speaker
labels, rename the speakers, download it, and save your corrected version to
~/Watsejy as a test-set row.
"""
import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402

import gradio as gr  # noqa: E402

SOURCES = ["voicenote", "inperson", "online", "read"]


def _downloads(t: engine.Transcript, txt_override: str | None = None) -> list[str]:
    stem = Path(t.source).stem
    d = Path(tempfile.mkdtemp(prefix="watsejy-dl-"))
    files = []
    txt = txt_override if txt_override is not None else t.to_txt()
    for ext, content in (("txt", txt), ("md", t.to_md()), ("srt", t.to_srt())):
        p = d / f"{stem}.{ext}"
        p.write_text(content, encoding="utf-8")
        files.append(str(p))
    return files


def run(file, speakers, num_speakers, progress=gr.Progress()):
    if not file:
        return "", "Drop a file first.", None, None
    msgs = []

    def say(m):
        msgs.append(m)
        progress(0, desc=m)

    try:
        n = int(num_speakers) if num_speakers and int(num_speakers) > 0 else None
        t = engine.transcribe(file, speakers=bool(speakers), num_speakers=n, progress=say)
    except Exception as e:
        return "", f"**Fout:** {e}", None, None
    speed = t.duration_s / t.elapsed_s if t.elapsed_s else 0
    status = (f"Klaar. {engine._hms(t.duration_s)} oudio in {t.elapsed_s:.0f}s ({speed:.1f}x intyds) · "
              f"{t.engine} · {t.model}" + (f" · {len(t.speakers)} sprekers" if t.speakers else ""))
    return t.to_txt(), status, _downloads(t), t


def rename(txt, spec, t):
    mapping = engine.parse_rename(spec)
    if not mapping:
        return txt, "Gee name soos `1=Johannes, 2=Pietie`.", gr.update()
    new_txt = engine.rename_speakers_in_text(txt, mapping)
    for s in (t.segments if t else []):
        if s.speaker in mapping:
            s.speaker = mapping[s.speaker]
    return new_txt, f"Sprekers hernoem: {', '.join(f'{k} → {v}' for k, v in mapping.items())}", (_downloads(t, new_txt) if t else gr.update())


def save(txt, source, codeswitch, t):
    if not t:
        return "Transkribeer eers 'n lêer."
    if not txt.strip():
        return "Die transkripsie is leeg."
    try:
        row = engine.save_correction(t.source, txt, source=source, codeswitch=bool(codeswitch), transcript=t)
    except Exception as e:
        return f"**Kon nie stoor nie:** {e}"
    return (f"Gestoor in `{engine.DATA_DIR}`: oudio gekopieer, transkripsie geskryf, ry bygevoeg by "
            f"`corrections.jsonl` ({row['duration_s']}s, bron: {row['source']}).")


def build() -> gr.Blocks:
    with gr.Blocks(title="Watsejy") as demo:
        gr.Markdown("# Watsejy\n**Wat sê jy?** Afrikaanse oudio na teks, op jou eie Mac. Niks verlaat die rekenaar nie.")
        state = gr.State(None)

        with gr.Row():
            with gr.Column(scale=1):
                file = gr.File(label="Stemboodskap of opname (opus, m4a, mp3, wav, mp4 …)", file_types=["audio", "video"], type="filepath")
                speakers = gr.Checkbox(label="Benoem sprekers (vergaderings; benodig HF_TOKEN)", value=False)
                num_speakers = gr.Number(label="Aantal sprekers (0 = outomaties)", value=0, precision=0)
                go = gr.Button("Transkribeer", variant="primary")
                status = gr.Markdown("")
            with gr.Column(scale=2):
                txt = gr.Textbox(label="Transkripsie (redigeer gerus)", lines=22)
                downloads = gr.File(label="Aflaai", file_count="multiple", interactive=False)

        with gr.Accordion("Hernoem sprekers", open=False):
            with gr.Row():
                spec = gr.Textbox(label="Name", placeholder="1=Johannes, 2=Pietie", scale=3)
                ren = gr.Button("Pas toe", scale=1)
            ren_status = gr.Markdown("")

        with gr.Accordion("Stoor gekorrigeerde transkripsie (bou die toetsstel)", open=False):
            gr.Markdown("Korrigeer die teks hierbo teen die oudio, kies die bron, en stoor. Dit kopieer die oudio en skryf 'n ry na `~/Watsejy/corrections.jsonl`.")
            with gr.Row():
                source = gr.Dropdown(SOURCES, value="voicenote", label="Bron")
                codeswitch = gr.Checkbox(label="Bevat heelwat Engels (code-switching)", value=False)
                sv = gr.Button("Stoor")
            sv_status = gr.Markdown("")

        go.click(run, [file, speakers, num_speakers], [txt, status, downloads, state])
        ren.click(rename, [txt, spec, state], [txt, ren_status, downloads])
        sv.click(save, [txt, source, codeswitch, state], [sv_status])
    return demo


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--share", action="store_true", help="also create a temporary public link")
    ap.add_argument("--port", type=int, default=7860)
    args = ap.parse_args()
    build().launch(server_name="127.0.0.1", server_port=args.port, share=args.share, inbrowser=True)


if __name__ == "__main__":
    main()
