# -*- coding: utf-8 -*-
"""Renderiza os quadros de qualquer episodio, em 16:9 ou 9:16.

render16.py so sabia desenhar a armadeira: importava cenas16 e abria um
timeline com caminho fixo. Aqui tudo vem de fora, e as cartelas saem do
gerador -- entao um episodio novo nao pede codigo novo.

A paleta e a cor de destaque vem do estilo do episodio (variacao.py), que e o
que faz dois videos seguidos nao se parecerem.

    EP=jararaca TL=work/jararaca/timeline.json OUT=work/jararaca/f16 \
    W=1920 H=1080 python3 pipeline/render_auto.py 0 500
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

import art2
from art2 import BRANCO, PRETO, Paint, cola, font, texto
import cenas_auto
import variacao

EP = os.environ.get("EP", "jararaca")
TL_PATH = os.environ["TL"]
OUTDIR = os.environ["OUT"]
W = int(os.environ.get("W", 1920))
H = int(os.environ.get("H", 1080))
FPS = int(os.environ.get("FPS", 30))
BOIL = 10.0

art2.W, art2.H = W, H
vert = H > W
CY = int(H * (0.40 if not vert else 0.42))
CAP_Y = int(H * (0.87 if not vert else 0.80))
CAP_W = int(W * 0.80)
CAP_TAM = int(min(W, H) * (0.054 if not vert else 0.046))

EST = variacao.estilo(EP)
PAL = EST["paleta"]


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


FUNDO = _rgb(PAL["fundo"])
TRACO = _rgb(PAL["traco"])
AC = _rgb(PAL["destaque"])

tl = json.load(open(TL_PATH, encoding="utf-8"))
LIN = tl["linhas"]
TOTAL = tl["total"]
NF = int(round(TOTAL * FPS))

for n, m in enumerate(LIN):
    m["start"] = 0.0 if n == 0 else m["in"]
for n, m in enumerate(LIN):
    m["end"] = LIN[n + 1]["start"] if n + 1 < len(LIN) else TOTAL

cenas_auto.configura(LIN, EP)

CAPS = [texto(m["legenda"], font("hand", CAP_TAM), TRACO, align="center",
              max_w=CAP_W, spacing=4) for m in LIN]
TITULOS = {m["i"]: texto(re.sub(r"^\d+\s+", "", m["ato"]),
                         font("marker", int(min(W, H) * 0.10)), AC, PRETO, 8)
           for m in LIN if m.get("cap_inicio")}


def quadro(t):
    idx = len(LIN) - 1
    for n, m in enumerate(LIN):
        if m["start"] <= t < m["end"]:
            idx = n
            break
    m = LIN[idx]
    tl_ = t - m["start"]
    d = max(m["end"] - m["start"], 0.01)
    seed = int(t * BOIL) * 37 + idx * 101

    p = Paint(W, H, FUNDO)
    ctx = {"p": p, "t": tl_, "d": d, "s": seed, "ac": AC, "CY": CY, "W": W, "H": H,
           "foto": lambda nome, **kw: None, "idx": idx}
    cenas_auto.desenha(m["i"], ctx)

    # cartela de capitulo por cima, no primeiro segundo
    if m["i"] in TITULOS and tl_ < 1.25:
        k = min(1.0, tl_ / 0.22)
        fade = 1.0 if tl_ < 0.95 else max(0.0, 1 - (tl_ - 0.95) / 0.3)
        im = TITULOS[m["i"]]
        p.im.alpha_composite(Image.new("RGBA", (W, H), FUNDO + (int(228 * fade),)))
        cola(p.im, im, W / 2, CY - H * 0.04 + H * 0.024 * (1 - k))
        p.traco([(W / 2 - im.width / 2, CY + H * 0.065),
                 (W / 2 - im.width / 2 + im.width * k, CY + H * 0.065)],
                AC, max(8, int(H * 0.013)), seed + 5, 4.0)

    # estalo do corte: dois quadros de moldura quando a fala troca
    if tl_ < 2.0 / FPS:
        esp = int(H * 0.028) if tl_ < 1.0 / FPS else int(H * 0.015)
        p.forma([(esp, esp), (W - esp, esp), (W - esp, H - esp), (esp, H - esp)],
                None, AC, esp, seed + 77, amp=7.0)

    cap = CAPS[idx]
    bx0 = (W - cap.width) // 2 - 26
    by0 = CAP_Y - cap.height // 2 - 14
    p.forma([(bx0, by0), (bx0 + cap.width + 52, by0),
             (bx0 + cap.width + 52, by0 + cap.height + 28), (bx0, by0 + cap.height + 28)],
            BRANCO if not PAL["escuro"] else (20, 20, 20), TRACO, 9, seed + 11, amp=4.0)
    cola(p.im, cap, W / 2, CAP_Y)
    return p.im


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    z = int(sys.argv[2]) if len(sys.argv) > 2 else NF
    os.makedirs(OUTDIR, exist_ok=True)
    if os.environ.get("PROBE"):
        for n in range(a, z):
            quadro(n / FPS).convert("RGB").save(f"{OUTDIR}/p_{n:06d}.jpg", quality=92)
    else:
        for n in range(a, z):
            quadro(n / FPS).convert("RGB").save(f"{OUTDIR}/f_{n:06d}.jpg", quality=93)
        print(f"ok {a}-{z}", flush=True)
