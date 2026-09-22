# animais-exoticos

Faceless short-form channel about Brazilian wildlife. Crude paint-style animation,
PT-BR narration, one real twist per episode. Everything is rendered from code in
`pipeline/` — there is no video editor in the loop.

Episode 1 (`armadeira`, the Brazilian wandering spider) is finished: an 8min03s
16:9 long-form and a 75s 9:16 short, both cut from the same material.

## Layout

| Path | What |
|---|---|
| `pipeline/` | The renderer. Drawing primitives, scene definitions, TTS, audio mix, encode. |
| `pipeline/fonts/` | Permanent Marker (Apache 2.0), Patrick Hand (OFL), Spline Sans, Bricolage. |
| `pipeline/fotos/` | Source photos from Wikimedia Commons. See `roteiros/armadeira.CREDITOS.txt`. |
| `roteiros/` | Scripts and image credits, per episode. |
| `work/` | Build artifacts — frames, TTS clips, mixed tracks. Gitignored, ~3.5 GB per episode. |
| `out/` | Finished renders. Gitignored. |

## The renderer

Modules build on each other; the `16` suffix is 16:9 long-form, `3` is the 9:16 short.

- `art.py` / `art2.py` — paint-style primitives: wobbly strokes, fills, hand lettering.
- `obj16.py` — drawable objects (the spider, the horse, the boy, arrows, labels).
- `scenes.py` / `scenes3.py` / `cenas16.py` — the scene cards. `cenas16.py` holds all 125 of episode 1.
- `sfx.py` — 11 sound effects synthesized from scratch (no sample library on the machine).
- `render*.py` — rasterize frames, parallel across 16 workers.
- `mixa*.py` — lay narration + effects onto a single track.
- `gen_tts*.py` — narration, per-chapter rate and pitch.
- `busca_fotos.py` — Wikimedia Commons search, filtered to reusable licenses.
- `qc.py`, `analyze.py` — contact sheets and motion measurement against reference videos.

Paths come from `paths.py`. Nothing is hardcoded; set `DARK_WORK=/some/fast/disk`
to move the build directory.

## Running it

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

cd pipeline
python3 gen_tts_longo.py     # narration -> work/tts_longo
python3 render16.py          # frames    -> work/frames16
python3 mixa16.py            # audio     -> work/trilha16.wav
```

Encoding is a plain ffmpeg call over `work/frames16` — `imageio-ffmpeg` ships the binary.

## Editorial rules

1. Crude MS-Paint look on purpose. Polished art was tried and rejected.
2. No monetization-risky subject matter, even where it costs a joke.
3. Images must track the narration. Loosely-chosen images made an early cut feel senseless.
4. No section labels on screen.
5. Keep things moving — episode 1 measures 0% static frames against 58–70% for the references.

## Before publishing episode 1

Two things are open, both recorded in `roteiros/armadeira.CREDITOS.txt`:

- **The long-form script is unverified.** Accident numbers, seasonality, severity
  classification and Butantan history need a primary source. The first-aid section
  needs review by a health professional.
- **The narration is synthetic** (`pt-BR-AntonioNeural`).

Image attribution is done: two photos are CC BY 2.0 and credited, the rest CC0 or
public domain.
