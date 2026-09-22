# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK
"""Trilha completa: narração + efeitos sonoros nas batidas."""
import json, wave, sys
import numpy as np
sys.path.insert(0, PIPE)
import sfx


SR = 48000

tl = json.load(open(f"{PIPE}/timeline_real.json"))
LIN = tl["linhas"]
TOT = tl["total"]
N = int(TOT * SR) + SR
mix = np.zeros(N)

# (offset em s, efeito, ganho) por cartela
EVENTOS = {
 0:  [(0.00,"impacto",.55),(2.30,"pop",.7),(2.30,"boing",.35)],
 1:  [(0.00,"toc",.8),(0.00,"pop",.5),(0.90,"erro",1.0)],
 2:  [(0.00,"toc",.8),(0.00,"pop",.5),(0.55,"risco",.9),(1.00,"pop",.45)],
 3:  [(0.00,"impacto",.7),(0.35,"whoosh",.5)],
 4:  [(0.00,"toc",.8),(0.30,"pop",.4),(1.00,"erro",.9)],
 5:  [(0.00,"pop",.8),(0.90,"pop",.5),(1.30,"risco",.7)],
 6:  [(0.00,"pop",.7),(0.70,"risco",.8),(1.50,"pop",.5)],
 7:  [(0.00,"toc",.8),(0.60,"pop",.6),(0.60,"ding",.25)],
 8:  [(0.00,"toc",.8),(0.20,"whoosh",.4)],
 9:  [(0.00,"impacto",1.0)],                       # a foto real entra
 10: [(0.00,"boing",.9),(0.10,"risco",.6)],
 11: [(0.00,"tensao",1.0),(0.05,"whoosh",.5)],
 12: [(0.00,"toc",.8),(0.25,"pop",.4),(0.41,"pop",.4),(0.57,"pop",.4)],
 13: [(0.00,"toc",.8),(0.00,"pop",.5),(1.10,"pop",.45)],
 14: [(0.00,"pop",.7),(0.33,"risco",.6)],          # os outros dois tempos entram abaixo
 15: [(0.00,"impacto",.55),(0.00,"pop",.7),(0.80,"risco",.8),(1.40,"whoosh",.45)],
 16: [(0.00,"toc",.8),(0.00,"pop",.5),(0.80,"pop",.45)],
 17: [(0.00,"impacto",.7)],
 18: [(0.00,"pop",.7),(1.00,"risco",.8)],
 19: [(0.00,"pop",.8),(1.20,"brilho",1.0)],
 20: [(0.00,"toc",.8),(0.00,"pop",.5)],            # o tique-taque entra abaixo
 21: [(0.00,"impacto",.7)],
 22: [(0.00,"pop",.7),(1.00,"ding",1.0)],
 23: [(0.00,"pop",.7),(1.00,"brilho",.9),(1.30,"ding",.6)],
}


def soma(sinal, t0, g=1.0):
    i0 = int(t0 * SR)
    if i0 < 0 or i0 >= N:
        return
    k = min(len(sinal), N - i0)
    mix[i0:i0 + k] += sinal[:k] * g


def ler(p):
    w = wave.open(p, "rb")
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    w.close()
    return d


# ---------------------------------------------------------------- narração
for m in LIN:
    d = ler(f"{WORK}/tts/{m['i']:02d}.wav")
    fl = min(240, len(d) // 8)
    if fl > 4:
        d[:fl] *= np.linspace(0, 1, fl)
        d[-fl:] *= np.linspace(1, 0, fl)
    soma(d, m["in"], 1.0)

# ----------------------------------------------------------------- efeitos
POS = {m["i"]: m for m in LIN}
for n, m in enumerate(LIN):
    ini = 0.0 if n == 0 else m["in"]
    fim = LIN[n + 1]["in"] if n + 1 < len(LIN) else TOT
    for off, nome, g in EVENTOS.get(m["i"], []):
        soma(sfx.BANCO[nome](), ini + off, g * 0.42)

# cartela 14: três tempos (sapato / cortina / foto do cacho)
m14 = POS[14]
i14 = [n for n, m in enumerate(LIN) if m["i"] == 14][0]
fim14 = LIN[i14 + 1]["in"] if i14 + 1 < len(LIN) else TOT
seg = (fim14 - m14["in"]) / 3.0
soma(sfx.pop(520), m14["in"] + seg, 0.42 * 0.7)
soma(sfx.whoosh(0.26), m14["in"] + seg, 0.42 * 0.5)
soma(sfx.impacto(), m14["in"] + 2 * seg, 0.42 * 0.8)

# cartela 20: tique-taque acelerado enquanto o relógio gira
m20 = POS[20]
i20 = [n for n, m in enumerate(LIN) if m["i"] == 20][0]
fim20 = LIN[i20 + 1]["in"] if i20 + 1 < len(LIN) else TOT
t = m20["in"] + 0.15
while t < fim20 - 0.1:
    soma(sfx.tique(), t, 0.42 * 0.55)
    t += 0.165

# ------------------------------------------------------- mistura e limite
pico = np.max(np.abs(mix))
if pico > 0:
    mix = mix / pico * 0.89
out = (mix * 32767).astype(np.int16)
w = wave.open(f"{WORK}/trilha.wav", "wb")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(out.tobytes()); w.close()
n_ev = sum(len(v) for v in EVENTOS.values()) + 3 + int((fim20 - m20["in"]) / 0.165)
print(f"trilha.wav {len(out)/SR:.2f}s | {n_ev} efeitos | pico {pico:.2f}")
