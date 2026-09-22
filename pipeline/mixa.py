# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK
"""Monta a trilha: narração nos tempos exatos + sub nos cortes do ato 5 + sino na virada."""
import json, wave, math, sys
import numpy as np


SR = 48000

tl = json.load(open(f"{PIPE}/timeline_real.json"))
LIN = tl["linhas"]
TOT = tl["total"]
N = int(TOT * SR) + SR // 2
mix = np.zeros(N, dtype=np.float64)


def ler(p):
    w = wave.open(p, "rb")
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    w.close()
    return d


# ---------------------------------------------------------- narração
for m in LIN:
    d = ler(f"{WORK}/tts/{m['i']:02d}.wav")
    i0 = int(m["in"] * SR)
    # micro-fade nas pontas evita clique
    fl = min(240, len(d) // 8)
    if fl > 4:
        d[:fl] *= np.linspace(0, 1, fl)
        d[-fl:] *= np.linspace(1, 0, fl)
    mix[i0:i0 + len(d)] += d * 0.92

# ------------------------------------------------- sub grave nos cortes
VIRADA_I = next(m["i"] for m in LIN if m["ato"].startswith("7"))

def sub(t0, f0=44.0, dur=0.55, amp=0.22):
    n = int(dur * SR)
    t = np.arange(n) / SR
    env = np.exp(-t * 7.0)
    f = f0 * np.exp(-t * 1.4)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env * amp
    i0 = int(t0 * SR)
    mix[i0:i0 + n] += s[:max(0, min(n, N - i0))]

for m in LIN:
    if m["ato"].startswith("5"):            # ato do pavor
        sub(max(0.0, m["in"] - 0.06))
    if m["ato"].startswith("1"):            # abertura
        sub(0.0, f0=52.0, dur=1.2, amp=0.26)

# ------------------------------------------------------ sino da virada
def sino(t0, f0=523.25, dur=3.2, amp=0.13):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for h, a, dec in [(1.0, 1.0, 1.4), (2.01, 0.5, 2.2), (2.99, 0.28, 3.0), (4.2, 0.14, 4.0)]:
        s += a * np.sin(2 * np.pi * f0 * h * t) * np.exp(-t * dec)
    s *= amp / max(1e-9, np.max(np.abs(s)))
    atk = int(0.004 * SR)
    s[:atk] *= np.linspace(0, 1, atk)
    i0 = int(t0 * SR)
    k = max(0, min(n, N - i0))
    mix[i0:i0 + k] += s[:k]

t_virada = next(m["in"] for m in LIN if m["i"] == VIRADA_I)
sino(t_virada - 0.28)

# ---------------------------------------------------------------- saída
pico = np.max(np.abs(mix))
mix = mix / pico * 0.89 if pico > 0 else mix
out = (mix * 32767).astype(np.int16)
w = wave.open(f"{WORK}/trilha.wav", "wb")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(out.tobytes()); w.close()
print(f"trilha.wav  {len(out)/SR:.2f}s  pico {pico:.3f}  virada em {t_virada:.2f}s")
