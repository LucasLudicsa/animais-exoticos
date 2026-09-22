# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK, OUT
"""Vídeo longo 1920x1080, mesmo traço de Paint."""
import sys, os, json, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageEnhance, ImageDraw
import art2
from art2 import (BRANCO, PRETO, VERMELHO, AZUL, AMARELO, VERDE, ROSA, MARROM,
                  CINZA, LARANJA, PELE, Paint, texto, cola, font, wob, densify,
                  pop, aranha, menino, suor, balao_susto, seta, rotulo, aponta)
import obj16 as OB
import cenas16

W, H = 1920, 1080
art2.W, art2.H = W, H          # o Paint usa esses valores como padrão

OUT = f"{WORK}/frames16"
FPS = 30
BOIL = 10.0
CAP_Y = 940
CY = 470                        # centro do desenho

tl = json.load(open(f"{PIPE}/timeline_longo.json"))
LIN = tl["linhas"]
TOTAL = tl["total"]
NF = int(round(TOTAL * FPS))

for n, m in enumerate(LIN):
    m["start"] = 0.0 if n == 0 else m["in"]
for n, m in enumerate(LIN):
    m["end"] = LIN[n + 1]["start"] if n + 1 < len(LIN) else TOTAL

# a virada de cor acontece no capítulo que fala do soro em diante
VIRADA_CAP = ("12 O SORO", "13 VIRA REMEDIO", "14 FECHO")
def ac_de(m):
    return VERDE if m["ato"] in VIRADA_CAP else VERMELHO

_fc = {}
def foto(nome):
    if nome in _fc:
        return _fc[nome]
    im = Image.open(f"{PIPE}/fotos/{nome}.jpg").convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.30)
    im = ImageEnhance.Contrast(im).enhance(1.15)
    _fc[nome] = im
    return im


def poe_foto(p, nome, t, d, seed, cx=W//2, cy=CY, alvo=(1020, 720)):
    src = foto(nome)
    z = 1.0 + 0.05 * min(1.0, t / max(d, .01))
    k = max(alvo[0] / src.width, alvo[1] / src.height) * 1.12 * z
    im = src.resize((int(src.width * k), int(src.height * k)), Image.LANCZOS)
    l = max(0, (im.width - alvo[0]) // 2); tp = max(0, (im.height - alvo[1]) // 2)
    rec = im.crop((l, tp, l + alvo[0], tp + alvo[1]))
    x0, y0 = int(cx - alvo[0] / 2), int(cy - alvo[1] / 2)
    msk = Image.new("L", alvo, 0)
    pts = [(0, 0), (alvo[0], 0), (alvo[0], alvo[1]), (0, alvo[1])]
    ImageDraw.Draw(msk).polygon(wob(densify(pts + [pts[0]], 40), 7, seed), fill=255)
    p.im.paste(rec, (x0, y0), msk)
    p.forma([(x0, y0), (x0 + alvo[0], y0), (x0 + alvo[0], y0 + alvo[1]), (x0, y0 + alvo[1])],
            None, PRETO, 16, seed, amp=6.0)


CAPS = [texto(m["legenda"], font("hand", 58), PRETO, align="center", max_w=1420, spacing=4)
        for m in LIN]
TITULOS = {}
for m in LIN:
    if m.get("cap_inicio"):
        nome = re.sub(r"^\d+\s+", "", m["ato"])
        TITULOS[m["i"]] = texto(nome, font("marker", 110), ac_de(m), PRETO, 8)


def quadro(t):
    idx = 0
    for n, m in enumerate(LIN):
        if m["start"] <= t < m["end"]:
            idx = n; break
    else:
        idx = len(LIN) - 1
    m = LIN[idx]
    tl_ = t - m["start"]
    d = m["end"] - m["start"]
    seed = int(t * BOIL) * 37 + idx * 101
    ac = ac_de(m)

    p = Paint(W, H, BRANCO)
    ctx = {"p": p, "t": tl_, "d": d, "s": seed, "ac": ac, "CY": CY, "W": W, "H": H,
           "foto": lambda nome, **kw: poe_foto(p, nome, tl_, d, seed, **kw), "idx": idx}
    cenas16.desenha(m["i"], ctx)

    for j, (txt, ax, ay, rx, ry, t0, cor, tam) in enumerate(cenas16.SETAS.get(m["i"], [])):
        if tl_ >= t0:
            aponta(p, txt, ax, ay, rx, ry, tl_, t0, cor, seed + 400 + j * 9, tam)

    # cartela de capítulo: entra por cima nos primeiros 1,2 s
    if m["i"] in TITULOS and tl_ < 1.25:
        k = min(1.0, tl_ / 0.22)
        fade = 1.0 if tl_ < 0.95 else max(0.0, 1 - (tl_ - 0.95) / 0.3)
        im = TITULOS[m["i"]]
        veu = Image.new("RGBA", (W, H), (255, 255, 255, int(220 * fade)))
        p.im.alpha_composite(veu)
        cola(p.im, im, W / 2, CY - 40 + 26 * (1 - k))
        p.traco([(W / 2 - im.width / 2, CY + 70), (W / 2 - im.width / 2 + im.width * k, CY + 70)],
                ac, 14, seed + 5, 4.0)

    # estalo do corte
    if tl_ < 2.0 / FPS:
        esp = 30 if tl_ < 1.0 / FPS else 16
        p.forma([(esp, esp), (W - esp, esp), (W - esp, H - esp), (esp, H - esp)],
                None, ac, esp, seed + 77, amp=7.0)

    cap = CAPS[idx]
    bx0 = (W - cap.width) // 2 - 26
    bx1 = bx0 + cap.width + 52
    by0 = CAP_Y - cap.height // 2 - 14
    by1 = by0 + cap.height + 28
    p.forma([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], BRANCO, PRETO, 9, seed + 11, amp=4.0)
    cola(p.im, cap, W / 2, CAP_Y)
    return p.im


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    z = int(sys.argv[2]) if len(sys.argv) > 2 else NF
    modo = sys.argv[3] if len(sys.argv) > 3 else "seq"
    os.makedirs(OUT, exist_ok=True)
    if modo == "probe":
        for n in range(a, z):
            quadro(n / FPS).convert("RGB").save(f"{WORK}/p16_{n:06d}.jpg", quality=92)
    else:
        for n in range(a, z):
            quadro(n / FPS).convert("RGB").save(f"{OUT}/f_{n:06d}.jpg", quality=93)
        print(f"ok {a}-{z}")
