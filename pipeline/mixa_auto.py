# -*- coding: utf-8 -*-
"""Monta a trilha: narracao + efeitos, para qualquer episodio.

mixa16.py escolhia os efeitos por numero de cartela, numa lista escrita a mao
(FOTOS={7,12,54...}). Isso so vale para o episodio em que foi escrita. Aqui o
efeito sai do que a frase E: numero ganha impacto, proibicao ganha buzina,
virada ganha brilho, o resto ganha um toc discreto.

    python3 pipeline/mixa_auto.py jararaca work/jararaca/timeline.json \
        work/jararaca/tts work/jararaca/trilha.wav
"""
import json
import os
import random
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cenas_auto
import sfx
import variacao

SR = 48000
G = 0.38


def ler(p):
    with wave.open(p, "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0


def monta(episodio, tl_path, dir_tts, saida):
    tl = json.load(open(tl_path, encoding="utf-8"))
    LIN, TOT = tl["linhas"], tl["total"]
    est = variacao.estilo(episodio)
    r = random.Random(est["semente"] + 99)
    cenas_auto.configura(LIN, episodio)

    N = int(TOT * SR) + SR
    mix = np.zeros(N)

    def soma(sig, t0, g=1.0):
        i0 = int(t0 * SR)
        if i0 < 0 or i0 >= N:
            return
        k = min(len(sig), N - i0)
        mix[i0:i0 + k] += sig[:k] * g

    for m in LIN:
        d = ler(os.path.join(dir_tts, f"{m['i']:03d}.wav"))
        fl = min(240, len(d) // 8)
        if fl > 4:
            d[:fl] *= np.linspace(0, 1, fl)
            d[-fl:] *= np.linspace(1, 0, fl)
        soma(d, m["in"], 1.0)

    for m in LIN:
        ini = m["in"]
        txt = m["texto"]
        conc = cenas_auto._conceitos(txt)
        assunto = conc[0] if conc else "cobra"
        rel = cenas_auto._relacao(txt)
        num = cenas_auto._numero(txt)

        if m.get("cap_inicio"):
            soma(sfx.impacto(), max(0.0, ini - 0.55), G * 0.85)
            soma(sfx.brilho(), max(0.0, ini - 0.40), G * 0.50)
            soma(sfx.risco(), max(0.0, ini - 0.25), G * 0.80)

        if num:                       # numero e o que o video quer que voce guarde
            soma(sfx.impacto(), ini, G * 0.90)
            soma(sfx.ding(), ini + 0.45, G * 0.55)
        elif rel == "nega":           # proibicao: buzina, no tempo do X
            soma(sfx.pop(480), ini, G * 0.80)
            soma(sfx.erro(), ini + 0.50, G * 0.85)
        elif rel == "alvo":           # a seta saindo
            soma(sfx.pop(500), ini, G * 0.75)
            soma(sfx.whoosh() if hasattr(sfx, "whoosh") else sfx.boing(), ini + 0.45, G * 0.55)
        elif rel == "queda":
            soma(sfx.pop(470), ini, G * 0.70)
            soma(sfx.tensao(0.8), ini + 0.35, G * 0.70)
        elif assunto in ("comprimido", "frasco"):
            soma(sfx.brilho(), ini + 0.35, G * 0.70)
            soma(sfx.pop(500), ini, G * 0.70)
        elif assunto in ("cobra", "cascavel"):
            soma(sfx.pop(460), ini, G * 0.80)
            if r.random() < 0.35:
                soma(sfx.boing(), ini, G * 0.30)
        else:
            soma(sfx.toc(), ini, G * 0.70)

        if r.random() < 0.10:
            soma(sfx.tensao(0.9), ini, G * 0.65)

    pico = float(np.max(np.abs(mix)))
    if pico > 0:
        mix = mix / pico * 0.89
    out = (mix * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    with wave.open(saida, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(out.tobytes())
    print(f"{os.path.basename(saida)}  {len(out)/SR:.1f}s  pico {pico:.2f}")


if __name__ == "__main__":
    monta(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
