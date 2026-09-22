# -*- coding: utf-8 -*-
"""Where things live. Import this instead of hardcoding paths.

PIPE  source that belongs in the repo: fonts, licensed photos, scripts, timelines
WORK  regenerable build artifacts: frames, TTS, mixed audio tracks (gitignored)
OUT   finished renders (gitignored; too big for git)

Override the build dir with DARK_WORK=/path if you want it on a faster disk.
"""
import os

PIPE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(PIPE)
WORK = os.environ.get("DARK_WORK", os.path.join(ROOT, "work"))
OUT = os.path.join(ROOT, "out")
ROTEIROS = os.path.join(ROOT, "roteiros")

for _d in (WORK, OUT):
    os.makedirs(_d, exist_ok=True)
