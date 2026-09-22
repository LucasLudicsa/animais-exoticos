# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK, OUT
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from art import (W, H, BREU, BREU_J, MATA, AREIA, URUCUM, JADE, DIM, CINZA,
                 font, make_grain, text_img, paste, ease, Pad)
import scenes


OUT = f"{WORK}/frames"
FPS = 30
WIPE = 0.20          # varredura entre atos
CAP_MAXW = 860

tl = json.load(open(f"{PIPE}/timeline_real.json"))
LINHAS = tl["linhas"]
TOTAL = tl["total"]
NF = int(round(TOTAL * FPS))

# ---- limites de cada cartela: vale até o início da próxima
for n, m in enumerate(LINHAS):
    m["start"] = 0.0 if n == 0 else LINHAS[n]["in"]
for n, m in enumerate(LINHAS):
    m["end"] = LINHAS[n + 1]["start"] if n + 1 < len(LINHAS) else TOTAL
LINHAS[0]["start"] = 0.0

VIRADA_I = next(m["i"] for m in LINHAS if m["ato"].startswith("7"))

def accent_de(i):
    return JADE if i >= VIRADA_I else URUCUM

def bg_de(i):
    return BREU_J if i >= VIRADA_I else BREU

GRAIN = make_grain()

# ---- assets por cartela
CARDS = []
for m in LINHAS:
    a, f = scenes.build(m["i"], accent_de(m["i"]), bg_de(m["i"]))
    cap = text_img(m["legenda"], font("sans", 52, 600), AREIA,
                   spacing=12, align="center", max_w=CAP_MAXW)
    rotulo = " ".join(m["ato"].split()[1].upper())
    lab = text_img(rotulo, font("mono", 24, 500), accent_de(m["i"]))
    CARDS.append({"m": m, "A": a, "f": f, "cap": cap, "lab": lab})

ATO_DE = {c["m"]["i"]: c["m"]["ato"] for c in CARDS}
INICIO_ATO = set()
prev = None
for c in CARDS:
    if c["m"]["ato"] != prev:
        INICIO_ATO.add(c["m"]["i"])
        prev = c["m"]["ato"]


def desenha(idx, t_local):
    c = CARDS[idx]
    m = c["m"]
    b = Image.new("RGBA", (W, H), bg_de(m["i"]) + (255,))

    # a arte vai numa camada própria para poder derivar devagar (deriva de espécime)
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dur_card = m["end"] - m["start"]
    c["f"](camada, t_local, dur_card)
    fase = t_local / max(0.001, dur_card)
    dx = int(round(7 * math.sin(fase * 1.7)))
    dy = int(round(-16 * fase + 8))
    b.alpha_composite(camada, (dx, dy))

    # linha de scanner: percorre a faixa do assunto sem parar
    ys = 520 + ((t_local * 132.0) % 760)
    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sc)
    ac0 = accent_de(m["i"])
    for j, al in enumerate([14, 30, 54, 30, 14]):
        yy = int(ys + (j - 2) * 3)
        if 0 <= yy < H:
            ds.line([(0, yy), (W, yy)], fill=ac0 + (al,), width=3)
    b.alpha_composite(sc)

    b.alpha_composite(GRAIN)

    # rótulo do ato
    paste(b, c["lab"], 80, 214, anchor="tl", alpha=0.85)
    pad = Pad(60, 6)
    pad.line([(3, 3), (57, 3)], accent_de(m["i"]), 5)
    paste(b, pad.out(), 80, 196, anchor="tl", alpha=0.9)

    # estalo de corte: 2 quadros de clarão — dá percussão à montagem
    if t_local < 2.0 / FPS:
        forca = 1.0 if t_local < 1.0 / FPS else 0.45
        ac = accent_de(m["i"])
        fl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        df = ImageDraw.Draw(fl)
        df.rectangle([0, 0, W, H], fill=(255, 255, 255, int(16 * forca)))
        df.rectangle([0, 700, W, 960], fill=ac + (int(30 * forca),))
        for yy, al in [(700, 200), (960, 200)]:
            df.line([(0, yy), (W, yy)], fill=ac + (int(al * forca),), width=4)
        b.alpha_composite(fl)

    # legenda queimada
    cap = c["cap"]
    bx0 = (W - cap.width) // 2 - 28
    bx1 = bx0 + cap.width + 56
    by0 = 1500 - cap.height // 2 - 22
    by1 = by0 + cap.height + 44
    box = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle([bx0, by0, bx1, by1], radius=10,
                                          fill=(8, 13, 11, 224))
    b.alpha_composite(box)
    paste(b, cap, W / 2, 1500)
    return b


def frame_em(t):
    idx = 0
    for n, c in enumerate(CARDS):
        if c["m"]["start"] <= t < c["m"]["end"]:
            idx = n
            break
    else:
        idx = len(CARDS) - 1
    m = CARDS[idx]["m"]
    im = desenha(idx, t - m["start"])

    # varredura de scanner na virada de ato
    if m["i"] in INICIO_ATO and idx > 0:
        dt = t - m["start"]
        if 0 <= dt < WIPE:
            k = dt / WIPE
            ant = CARDS[idx - 1]
            im_ant = desenha(idx - 1, ant["m"]["end"] - ant["m"]["start"] - 0.001)
            y = int(H * ease(k))
            im.paste(im_ant.crop((0, y, W, H)), (0, y))
            gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dg = ImageDraw.Draw(gl)
            ac = accent_de(m["i"])
            for j, al in enumerate([40, 90, 190, 255, 190, 90, 40]):
                yy = y + (j - 3) * 3
                if 0 <= yy < H:
                    dg.line([(0, yy), (W, yy)], fill=ac + (al,), width=3)
            im.alpha_composite(gl)
    return im


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    z = int(sys.argv[2]) if len(sys.argv) > 2 else NF
    modo = sys.argv[3] if len(sys.argv) > 3 else "seq"
    os.makedirs(OUT, exist_ok=True)
    if modo == "probe":
        for n in range(a, z):
            t = n / FPS
            frame_em(t).convert("RGB").save(f"{WORK}/probe_{n:05d}.jpg", quality=92)
        print("probe ok")
    else:
        for n in range(a, z):
            frame_em(n / FPS).convert("RGB").save(f"{OUT}/f_{n:05d}.jpg", quality=94)
            if n % 200 == 0:
                print(f"  {n}/{NF}", flush=True)
        print(f"ok {a}-{z}")
