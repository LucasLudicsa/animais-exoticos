# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK, OUT
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageEnhance, ImageDraw
from art2 import (W, H, BRANCO, PRETO, VERMELHO, VERDE, AMARELO, CINZA,
                  Paint, texto, cola, font, wob, densify, pop, aponta)
import scenes3


OUT = f"{WORK}/frames3"
FPS = 30
BOIL = 10.0          # o tremor troca 10x por segundo

tl = json.load(open(f"{PIPE}/timeline_real.json"))
LIN = tl["linhas"]
TOTAL = tl["total"]
NF = int(round(TOTAL * FPS))

for n, m in enumerate(LIN):
    m["start"] = 0.0 if n == 0 else m["in"]
for n, m in enumerate(LIN):
    m["end"] = LIN[n + 1]["start"] if n + 1 < len(LIN) else TOTAL

VIRADA = next(m["i"] for m in LIN if m["ato"].startswith("7"))
ac_de = lambda i: VERDE if i >= VIRADA else VERMELHO

# ------------------------------------------------------------------ fotos
_fcache = {}


def foto(nome, alvo=(980, 1020)):
    if nome in _fcache:
        return _fcache[nome]
    im = Image.open(f"{PIPE}/fotos/{nome}.jpg").convert("RGB")
    if nome == "mata_novo":                       # corta o painel do carro
        im = im.crop((0, 0, im.width, int(im.height * 0.72)))
    k = max(alvo[0] / im.width, alvo[1] / im.height) * 1.18
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.35)
    im = ImageEnhance.Contrast(im).enhance(1.18)
    _fcache[nome] = im
    return im


def poe_foto(p, nome, t, d, seed, ac):
    """Foto grande dentro de moldura tremida, com avanço lento."""
    alvo = (980, 1020)
    src = foto(nome, alvo)
    z = 1.0 + 0.055 * min(1.0, t / max(d, 0.01))
    cw, ch = int(alvo[0] / z), int(alvo[1] / z)
    l = max(0, (src.width - cw) // 2)
    tp = max(0, (src.height - ch) // 2)
    rec = src.crop((l, tp, l + cw, tp + ch)).resize(alvo, Image.LANCZOS)

    x0, y0 = (W - alvo[0]) // 2, 300
    # borda tremida: recorta a foto por uma máscara de polígono torto
    msk = Image.new("L", alvo, 0)
    pts = [(0, 0), (alvo[0], 0), (alvo[0], alvo[1]), (0, alvo[1])]
    ImageDraw.Draw(msk).polygon(wob(densify(pts + [pts[0]], 40), 7, seed), fill=255)
    p.im.paste(rec, (x0, y0), msk)
    p.forma([(x0, y0), (x0 + alvo[0], y0), (x0 + alvo[0], y0 + alvo[1]), (x0, y0 + alvo[1])],
            None, PRETO, 17, seed, amp=6.0)


CAPS, ROTS = [], []
for m in LIN:
    CAPS.append(texto(m["legenda"], font("hand", 62), PRETO, align="center", max_w=880, spacing=6))
    ROTS.append(texto(m["ato"].split()[1].upper(), font("marker", 40), ac_de(m["i"])))

INICIO_ATO, prev = set(), None
for m in LIN:
    if m["ato"] != prev:
        INICIO_ATO.add(m["i"]); prev = m["ato"]


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
    ac = ac_de(m["i"])

    p = Paint(fundo=BRANCO)

    nome_foto = scenes3.FOTOS.get(m["i"])
    usa_foto = nome_foto is not None and (
        m["i"] != 0 or tl_ < 2.25) and (
        m["i"] != 14 or tl_ >= 2 * d / 3)
    if usa_foto:
        poe_foto(p, nome_foto, tl_, d, seed, ac)
    scenes3.cena(m["i"], tl_, d, seed, ac, p)

    # seta + rótulo escrito à mão
    for j, (txt, ax, ay, rx, ry, t0, cor, tam) in enumerate(scenes3.SETAS.get(m["i"], [])):
        if tl_ >= t0:
            aponta(p, txt, ax, ay, rx, ry, tl_, t0, cor, seed + 400 + j * 9, tam)

    # estalo de corte: 2 quadros com moldura grossa
    if tl_ < 2.0 / FPS:
        esp = 34 if tl_ < 1.0 / FPS else 18
        p.forma([(esp, esp), (W - esp, esp), (W - esp, H - esp), (esp, H - esp)],
                None, ac, esp, seed + 77, amp=7.0)

    # legenda: fundo branco tremido + texto preto
    cap = CAPS[idx]
    bx0 = (W - cap.width) // 2 - 26
    bx1 = bx0 + cap.width + 52
    by0 = 1500 - cap.height // 2 - 16
    by1 = by0 + cap.height + 32
    p.forma([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], BRANCO, PRETO, 9, seed + 11, amp=4.0)
    cola(p.im, cap, W / 2, 1500)
    return p.im


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    z = int(sys.argv[2]) if len(sys.argv) > 2 else NF
    modo = sys.argv[3] if len(sys.argv) > 3 else "seq"
    os.makedirs(OUT, exist_ok=True)
    if modo == "probe":
        for n in range(a, z):
            quadro(n / FPS).convert("RGB").save(f"{WORK}/p3_{n:05d}.jpg", quality=92)
    else:
        for n in range(a, z):
            quadro(n / FPS).convert("RGB").save(f"{OUT}/f_{n:05d}.jpg", quality=94)
        print(f"ok {a}-{z}")
