# -*- coding: utf-8 -*-
"""Objetos do episodio da jararaca, no mesmo traco tosco dos outros.

A biblioteca (obj16.py) tinha aranha, cavalo, escorpiao e mais vinte coisas,
mas nenhum reptil. Estes ficam aqui e vao crescendo: cada episodio novo
deposita seus objetos, e os proximos reaproveitam.
"""
import math
import random

from art2 import (AMARELO, AZUL, BRANCO, CINZA, LARANJA, MARROM, PRETO, ROSA,
                  VERDE, VERMELHO, font)

BEGE = (214, 190, 150)
MARROM_ESC = (120, 80, 55)
FOLHA_SECA = (190, 150, 95)


def _espinha(cx, cy, comp, ondas=2.2, amp=0.20, n=34, fase=0.0):
    """Curva em S: o esqueleto por onde o corpo engrossa."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = cx - comp / 2 + comp * t
        y = cy + math.sin(t * math.pi * ondas + fase) * comp * amp
        pts.append((x, y))
    return pts


def cobra(p, cx, cy, tam, seed, ondas=2.2, cabeca_erguida=False, boca=0.0,
          fill=BEGE, marcas=True):
    """Jararaca: corpo em S que afina, cabeca chata, e os Vs nas costas.

    boca 0..1 abre as presas. cabeca_erguida levanta a frente em S de ataque.
    """
    e = max(6, int(tam * 0.035))
    comp = tam * 1.5
    esp = _espinha(cx, cy, comp, ondas, 0.16, 36)

    # corpo: poligono construido a partir da espinha, engrossando no meio
    cima, baixo = [], []
    for i, (x, y) in enumerate(esp):
        t = i / (len(esp) - 1)
        larg = tam * 0.115 * (0.35 + 1.3 * math.sin(math.pi * min(t * 1.15, 1.0)) ** 0.65)
        if t > 0.82:                      # cauda afina ate virar risco
            larg *= max(0.06, (1 - t) / 0.18)
        if i == 0:
            dx, dy = esp[1][0] - x, esp[1][1] - y
        else:
            dx, dy = x - esp[i - 1][0], y - esp[i - 1][1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        cima.append((x + nx * larg, y + ny * larg))
        baixo.append((x - nx * larg, y - ny * larg))
    p.forma(cima + baixo[::-1], fill, PRETO, e, seed, 2.6)

    # os Vs: o desenho que identifica a jararaca
    if marcas:
        r = random.Random(seed + 5)
        for k in range(5):
            t = 0.16 + k * 0.145
            i = int(t * (len(esp) - 1))
            x, y = esp[i]
            w = tam * 0.105
            h = tam * 0.075
            p.traco([(x - w, y - h), (x, y + h * 0.45), (x + w, y - h)],
                    MARROM_ESC, max(4, int(e * 0.75)), seed + 30 + k, 2.2)

    # cabeca na ponta esquerda, achatada e mais larga que o pescoco
    hx, hy = esp[0]
    if cabeca_erguida:
        # pescoco em S: sobe do corpo e volta, que e a postura de bote
        base = esp[3]
        hy -= tam * 0.34
        hx += tam * 0.10
        p.traco([base, (base[0] - tam * 0.16, base[1] - tam * 0.16),
                 (hx - tam * 0.16, hy + tam * 0.20), (hx, hy + tam * 0.04)],
                fill, int(tam * 0.155), seed + 2, 2.2)
        p.traco([base, (base[0] - tam * 0.16, base[1] - tam * 0.16),
                 (hx - tam * 0.16, hy + tam * 0.20), (hx, hy + tam * 0.04)],
                PRETO, max(3, int(e * 0.45)), seed + 12, 2.2)
    rh = tam * 0.15
    p.forma([(hx - rh * 1.15, hy), (hx - rh * 0.45, hy - rh * 0.72),
             (hx + rh * 0.75, hy - rh * 0.60), (hx + rh * 0.95, hy),
             (hx + rh * 0.75, hy + rh * 0.60), (hx - rh * 0.45, hy + rh * 0.72)],
            fill, PRETO, e, seed + 3, 2.4)
    # olho
    p.bola(hx - rh * 0.30, hy - rh * 0.20, max(3, tam * 0.028), PRETO, PRETO,
           max(3, int(e * 0.5)), seed + 4)

    # lingua bifurcada ou presas
    if boca > 0.02:
        p.forma([(hx - rh * 1.15, hy + rh * 0.10),
                 (hx - rh * 0.30, hy + rh * 0.35 + tam * 0.16 * boca),
                 (hx + rh * 0.4, hy + rh * 0.55)], ROSA, PRETO, max(4, int(e * 0.7)), seed + 6, 2.0)
        for s in (-1, 1):
            px = hx - rh * 0.75 + s * tam * 0.035
            p.traco([(px, hy + rh * 0.25), (px - s * tam * 0.012, hy + rh * 0.25 + tam * 0.10 * boca)],
                    BRANCO, max(4, int(e * 0.65)), seed + 7 + s, 1.4)
    else:
        lx = hx - rh * 1.15
        ly = hy + rh * 0.12
        p.traco([(lx, ly), (lx - tam * 0.17, ly + tam * 0.03)], VERMELHO, max(3, int(e * 0.5)), seed + 8, 1.8)
        for s in (-1, 1):
            p.traco([(lx - tam * 0.17, ly + tam * 0.03),
                     (lx - tam * 0.25, ly + tam * 0.03 + s * tam * 0.045)],
                    VERMELHO, max(3, int(e * 0.5)), seed + 9 + s, 1.6)


def folha(p, cx, cy, tam, seed, cor=FOLHA_SECA):
    """Folha seca: o chao onde ela some."""
    e = max(4, int(tam * 0.06))
    pts = []
    for i in range(17):
        t = i / 16
        x = cx - tam / 2 + tam * t
        y = cy - math.sin(math.pi * t) * tam * 0.34
        pts.append((x, y))
    for i in range(17):
        t = 1 - i / 16
        x = cx - tam / 2 + tam * t
        y = cy + math.sin(math.pi * t) * tam * 0.30
        pts.append((x, y))
    p.forma(pts, cor, PRETO, e, seed, 2.4)
    p.traco([(cx - tam * 0.48, cy), (cx + tam * 0.48, cy)], PRETO, max(3, int(e * 0.6)), seed + 1, 2.0)
    for k in range(4):
        t = 0.22 + k * 0.19
        x = cx - tam * 0.48 + tam * 0.96 * t
        for s in (-1, 1):
            p.traco([(x, cy), (x + tam * 0.10, cy + s * tam * 0.16)],
                    PRETO, max(2, int(e * 0.45)), seed + 10 + k * 2 + (s > 0), 1.6)


def rato(p, cx, cy, tam, seed, cor=CINZA):
    """Rato: o que ela realmente quer."""
    e = max(5, int(tam * 0.05))
    p.oval(cx, cy, tam * 0.34, tam * 0.24, cor, PRETO, e, seed, 2.6)
    p.bola(cx + tam * 0.34, cy - tam * 0.04, tam * 0.16, cor, PRETO, e, seed + 1)
    p.bola(cx + tam * 0.30, cy - tam * 0.18, tam * 0.085, ROSA, PRETO, max(3, int(e * 0.7)), seed + 2)
    p.bola(cx + tam * 0.43, cy - tam * 0.07, max(2, tam * 0.022), PRETO, PRETO, max(2, int(e * 0.4)), seed + 3)
    p.traco([(cx - tam * 0.33, cy + tam * 0.04), (cx - tam * 0.62, cy - tam * 0.10),
             (cx - tam * 0.70, cy + tam * 0.10)], PRETO, max(3, int(e * 0.55)), seed + 4, 2.2)


def comprimido(p, cx, cy, tam, seed, cor=BRANCO):
    """Comprimido: o fim da historia."""
    e = max(5, int(tam * 0.07))
    p.oval(cx, cy, tam * 0.5, tam * 0.3, cor, PRETO, e, seed, 2.4)
    p.traco([(cx, cy - tam * 0.27), (cx, cy + tam * 0.27)], PRETO, max(3, int(e * 0.6)), seed + 1, 2.0)


def estrada(p, cx, cy, tam, seed, casinha=True, cruz=True):
    """Estrada com a casa de um lado e o hospital longe do outro.

    Substitui o mapa que eu tentei tres vezes e nunca ficou reconhecivel como
    Brasil. E melhor assim: o capitulo da geografia nao fala de formato de
    pais, fala de DISTANCIA ate o soro. Estrada diz isso, mapa nao dizia.
    """
    e = max(5, int(tam * 0.035))
    y = cy + tam * 0.18
    p.traco([(cx - tam * 0.52, y + tam * 0.10), (cx + tam * 0.52, y - tam * 0.04)],
            PRETO, e, seed, 2.6)
    for k in range(7):
        t0 = k / 7 + 0.03
        x0 = cx - tam * 0.48 + tam * 0.96 * t0
        p.traco([(x0, y + tam * 0.055 - tam * 0.10 * t0),
                 (x0 + tam * 0.055, y + tam * 0.05 - tam * 0.10 * t0)],
                CINZA, max(3, int(e * 0.7)), seed + 10 + k, 1.6)
    if casinha:
        hx, hy = cx - tam * 0.36, y - tam * 0.20
        p.caixa(hx - tam * 0.10, hy - tam * 0.10, hx + tam * 0.10, hy + tam * 0.10,
                (236, 224, 200), PRETO, e, seed + 2)
        p.forma([(hx - tam * 0.13, hy - tam * 0.10), (hx, hy - tam * 0.24),
                 (hx + tam * 0.13, hy - tam * 0.10)], MARROM, PRETO, e, seed + 3)
    if cruz:
        bx, by = cx + tam * 0.36, y - tam * 0.30
        p.caixa(bx - tam * 0.12, by - tam * 0.12, bx + tam * 0.12, by + tam * 0.16,
                (240, 240, 240), PRETO, e, seed + 4)
        p.traco([(bx - tam * 0.07, by), (bx + tam * 0.07, by)], VERMELHO, max(4, int(e * 0.9)), seed + 5, 1.6)
        p.traco([(bx, by - tam * 0.07), (bx, by + tam * 0.07)], VERMELHO, max(4, int(e * 0.9)), seed + 6, 1.6)
