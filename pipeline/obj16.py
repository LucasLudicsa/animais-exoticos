# -*- coding: utf-8 -*-
"""Objetos desenhados à mão para o vídeo longo, em 1920x1080."""
import math
from art2 import (PRETO, BRANCO, VERMELHO, AZUL, AMARELO, VERDE, ROSA, MARROM,
                  CINZA, LARANJA, PELE)

LW = 13


def cavalo(p, cx, cy, tam, seed, fill=MARROM):
    """Cavalo de desenho de criança: caixa, quatro riscos, pescoço e cabeça."""
    e = max(7, int(tam * 0.045))
    w, h = tam * 0.62, tam * 0.34
    p.forma([(cx - w/2, cy - h/2), (cx + w/2, cy - h/2), (cx + w/2, cy + h/2), (cx - w/2, cy + h/2)],
            fill, PRETO, e, seed)
    for k, dx in enumerate([-0.36, -0.14, 0.16, 0.36]):
        x = cx + w * dx
        p.traco([(x, cy + h/2), (x + tam*0.02, cy + tam*0.42)], PRETO, e, seed + 2 + k, 2.6)
    # pescoço e cabeça
    p.forma([(cx + w/2 - tam*0.06, cy - h/2), (cx + w/2 + tam*0.10, cy - tam*0.40),
             (cx + w/2 + tam*0.24, cy - tam*0.38), (cx + w/2 + tam*0.10, cy - h/2 + tam*0.02)],
            fill, PRETO, e, seed + 8)
    p.oval(cx + w/2 + tam*0.20, cy - tam*0.40, tam*0.13, tam*0.085, fill, PRETO, e, seed + 9)
    p.d.ellipse([cx + w/2 + tam*0.13, cy - tam*0.43, cx + w/2 + tam*0.16, cy - tam*0.40], fill=PRETO)
    # crina e rabo
    for k in range(3):
        p.traco([(cx + w/2 + tam*0.06 - k*tam*0.03, cy - tam*0.34),
                 (cx + w/2 - tam*0.02 - k*tam*0.03, cy - tam*0.46)], PRETO, max(5, e-3), seed+12+k, 2.0)
    p.traco([(cx - w/2, cy - h/2 + tam*0.03), (cx - w/2 - tam*0.14, cy + tam*0.10)], PRETO, e, seed+16, 3.0)


def seringa(p, cx, cy, tam, seed, cor=VERDE):
    e = max(6, int(tam * 0.05))
    w, h = tam * 0.62, tam * 0.20
    p.forma([(cx - w/2, cy - h/2), (cx + w/2*0.72, cy - h/2), (cx + w/2*0.72, cy + h/2), (cx - w/2, cy + h/2)],
            BRANCO, PRETO, e, seed)
    p.forma([(cx - w/2, cy - h/2), (cx - w/2 + w*0.42, cy - h/2), (cx - w/2 + w*0.42, cy + h/2), (cx - w/2, cy + h/2)],
            cor, PRETO, e, seed + 1)
    p.traco([(cx + w/2*0.72, cy), (cx + w/2*1.20, cy)], PRETO, max(5, e-3), seed + 2, 2.0)
    p.traco([(cx - w/2, cy - h*0.9), (cx - w/2, cy + h*0.9)], PRETO, e, seed + 3, 2.4)
    p.traco([(cx - w/2, cy), (cx - w/2 - tam*0.14, cy)], PRETO, e, seed + 4, 2.4)


def coracao(p, cx, cy, tam, seed, cor=VERMELHO):
    e = max(7, int(tam * 0.06))
    r = tam * 0.26
    p.bola(cx - r*0.62, cy - r*0.35, r*0.70, cor, PRETO, e, seed)
    p.bola(cx + r*0.62, cy - r*0.35, r*0.70, cor, PRETO, e, seed + 1)
    p.forma([(cx - r*1.28, cy - r*0.18), (cx, cy + r*1.35), (cx + r*1.28, cy - r*0.18)],
            cor, PRETO, e, seed + 2)


def gota(p, cx, cy, tam, seed, cor=(120, 200, 255)):
    e = max(5, int(tam * 0.07))
    p.forma([(cx, cy - tam*0.36), (cx + tam*0.22, cy + tam*0.10), (cx, cy + tam*0.30),
             (cx - tam*0.22, cy + tam*0.10)], cor, PRETO, e, seed)


def calendario(p, cx, cy, tam, seed, marca=None):
    e = max(7, int(tam * 0.045))
    w, h = tam * 0.72, tam * 0.62
    p.forma([(cx - w/2, cy - h/2), (cx + w/2, cy - h/2), (cx + w/2, cy + h/2), (cx - w/2, cy + h/2)],
            BRANCO, PRETO, e, seed)
    p.forma([(cx - w/2, cy - h/2), (cx + w/2, cy - h/2), (cx + w/2, cy - h/2 + h*0.22), (cx - w/2, cy - h/2 + h*0.22)],
            VERMELHO, PRETO, e, seed + 1)
    for c in range(1, 4):
        p.traco([(cx - w/2 + c*w/4, cy - h/2 + h*0.22), (cx - w/2 + c*w/4, cy + h/2)], PRETO, max(4, e-5), seed+2+c, 1.6)
    for r in range(1, 3):
        p.traco([(cx - w/2, cy - h/2 + h*0.22 + r*h*0.26), (cx + w/2, cy - h/2 + h*0.22 + r*h*0.26)],
                PRETO, max(4, e-5), seed+8+r, 1.6)
    if marca is not None:
        col, row = marca
        mx = cx - w/2 + (col + 0.5) * w/4
        my = cy - h/2 + h*0.22 + (row + 0.5) * h*0.26
        p.xis(mx, my, w*0.09, VERMELHO, max(6, e-2), seed + 20)


def cama(p, cx, cy, tam, seed):
    e = max(7, int(tam * 0.045))
    w, h = tam * 0.80, tam * 0.30
    p.forma([(cx - w/2, cy - h/2), (cx + w/2, cy - h/2), (cx + w/2, cy + h/2), (cx - w/2, cy + h/2)],
            BRANCO, PRETO, e, seed)
    p.forma([(cx - w/2, cy - h/2), (cx + w*0.10, cy - h/2), (cx + w*0.10, cy + h/2), (cx - w/2, cy + h/2)],
            AZUL, PRETO, e, seed + 1)
    p.traco([(cx - w/2, cy - h/2), (cx - w/2, cy - h*1.35)], PRETO, e, seed + 2, 2.4)
    p.traco([(cx + w/2, cy - h/2), (cx + w/2, cy - h*1.05)], PRETO, e, seed + 3, 2.4)
    for dx in (-w/2, w/2):
        p.traco([(cx + dx, cy + h/2), (cx + dx, cy + h*1.15)], PRETO, e, seed + 4, 2.4)


def lupa(p, cx, cy, tam, seed):
    e = max(7, int(tam * 0.055))
    r = tam * 0.28
    p.bola(cx, cy, r, BRANCO, PRETO, e, seed)
    p.traco([(cx + r*0.72, cy + r*0.72), (cx + r*1.55, cy + r*1.55)], PRETO, int(e*1.6), seed + 1, 2.6)


def frascoL(p, cx, cy, tam, seed, cor=VERDE, tampa=CINZA):
    e = max(7, int(tam * 0.05))
    w = tam * 0.30
    p.forma([(cx - w*0.62, cy - tam*0.40), (cx + w*0.62, cy - tam*0.40),
             (cx + w*0.62, cy - tam*0.30), (cx - w*0.62, cy - tam*0.30)], tampa, PRETO, e, seed)
    p.forma([(cx - w, cy - tam*0.30), (cx + w, cy - tam*0.30),
             (cx + w, cy + tam*0.36), (cx - w, cy + tam*0.36)], cor, PRETO, e, seed + 1)


def predio(p, cx, cy, tam, seed, cor=(210, 210, 210)):
    """Prédio de instituto — caixa com janelas e uma bandeirinha."""
    e = max(7, int(tam * 0.04))
    w, h = tam * 0.78, tam * 0.52
    p.forma([(cx - w/2, cy - h/2), (cx + w/2, cy - h/2), (cx + w/2, cy + h/2), (cx - w/2, cy + h/2)],
            cor, PRETO, e, seed)
    for r in range(2):
        for c in range(4):
            x = cx - w/2 + (c + 0.6) * w/5
            y = cy - h/2 + (r + 0.55) * h/3
            p.forma([(x - w*0.06, y - h*0.10), (x + w*0.06, y - h*0.10),
                     (x + w*0.06, y + h*0.10), (x - w*0.06, y + h*0.10)], AZUL, PRETO, max(4, e-5), seed+2+r*4+c)
    p.forma([(cx - w*0.07, cy + h/2), (cx + w*0.07, cy + h/2),
             (cx + w*0.07, cy + h*0.22), (cx - w*0.07, cy + h*0.22)], MARROM, PRETO, max(5, e-3), seed+14)
    p.traco([(cx, cy - h/2), (cx, cy - h*0.78)], PRETO, max(5, e-4), seed+15, 2.0)
    p.forma([(cx, cy - h*0.78), (cx + w*0.13, cy - h*0.72), (cx, cy - h*0.66)], VERDE, PRETO, max(4, e-5), seed+16)


def teia(p, cx, cy, tam, seed, cor=CINZA):
    """Teia — para dizer que ela NÃO faz."""
    e = max(5, int(tam * 0.03))
    for j in range(8):
        a = j * math.pi / 4
        p.traco([(cx, cy), (cx + tam*0.42*math.cos(a), cy + tam*0.42*math.sin(a))], cor, e, seed+j, 2.0)
    for anel in (0.16, 0.27, 0.39):
        pts = [(cx + tam*anel*math.cos(j*math.pi/4), cy + tam*anel*math.sin(j*math.pi/4)) for j in range(9)]
        p.traco(pts, cor, e, seed + 20 + int(anel*100), 2.4)


def bolsa_ovos(p, cx, cy, tam, seed):
    e = max(6, int(tam * 0.05))
    p.bola(cx, cy, tam*0.28, BRANCO, PRETO, e, seed)
    for j in range(7):
        a = j * 2*math.pi/7
        p.bola(cx + tam*0.14*math.cos(a), cy + tam*0.14*math.sin(a), tam*0.045, AMARELO, PRETO, max(4, e-4), seed+2+j)


def pulmao(p, cx, cy, tam, seed, cor=ROSA):
    e = max(7, int(tam * 0.05))
    for lado in (-1, 1):
        p.forma([(cx + lado*tam*0.07, cy - tam*0.26), (cx + lado*tam*0.30, cy - tam*0.10),
                 (cx + lado*tam*0.30, cy + tam*0.22), (cx + lado*tam*0.10, cy + tam*0.28),
                 (cx + lado*tam*0.05, cy + tam*0.02)], cor, PRETO, e, seed + (lado > 0))
    p.traco([(cx, cy - tam*0.40), (cx, cy - tam*0.20)], PRETO, e, seed + 4, 2.0)


def pilha_roupa(p, cx, cy, tam, seed):
    e = max(6, int(tam * 0.05))
    cores = [AZUL, VERMELHO, AMARELO]
    for k in range(3):
        y = cy + tam*0.16 - k*tam*0.15
        w = tam*(0.42 - k*0.05)
        p.forma([(cx - w, y), (cx + w, y - tam*0.04), (cx + w*0.86, y - tam*0.15), (cx - w*0.90, y - tam*0.12)],
                cores[k], PRETO, e, seed + k)


def botaL(p, cx, cy, tam, seed, cor=AZUL):
    e = max(7, int(tam * 0.05))
    p.forma([(cx - tam*0.20, cy - tam*0.34), (cx + tam*0.06, cy - tam*0.34),
             (cx + tam*0.10, cy + tam*0.10), (cx + tam*0.40, cy + tam*0.16),
             (cx + tam*0.44, cy + tam*0.30), (cx - tam*0.22, cy + tam*0.30)], cor, PRETO, e, seed)
    p.traco([(cx - tam*0.22, cy + tam*0.20), (cx + tam*0.44, cy + tam*0.24)], PRETO, max(5, e-3), seed+1, 2.0)


def escorpiao(p, cx, cy, tam, seed, fill=(60, 60, 60)):
    e = max(7, int(tam * 0.05))
    p.oval(cx, cy, tam*0.26, tam*0.16, fill, PRETO, e, seed)
    for lado in (-1, 1):
        for k in range(3):
            a = math.radians(-20 + k*35)
            x1 = cx + lado*tam*0.20
            p.traco([(x1, cy), (x1 + lado*tam*0.22, cy + math.sin(a)*tam*0.22),
                     (x1 + lado*tam*0.34, cy + math.sin(a)*tam*0.34)], PRETO, max(5, e-3), seed+2+k+lado*4, 2.4)
        p.traco([(cx - tam*0.24, cy - tam*0.06), (cx - tam*0.44, cy - tam*0.20)], PRETO, e, seed+12+lado, 2.4)
        p.bola(cx - tam*0.50, cy - tam*0.24, tam*0.08, fill, PRETO, max(5, e-3), seed+14+lado)
    cauda = [(cx + tam*0.24, cy), (cx + tam*0.46, cy - tam*0.10), (cx + tam*0.54, cy - tam*0.32),
             (cx + tam*0.44, cy - tam*0.50)]
    p.traco(cauda, PRETO, e, seed + 20, 2.6)
    p.forma([(cx + tam*0.44, cy - tam*0.50), (cx + tam*0.54, cy - tam*0.58),
             (cx + tam*0.42, cy - tam*0.64)], VERMELHO, PRETO, max(5, e-3), seed+21)


def celular(p, cx, cy, tam, seed):
    e = max(7, int(tam * 0.05))
    w, h = tam * 0.30, tam * 0.54
    p.forma([(cx-w/2, cy-h/2), (cx+w/2, cy-h/2), (cx+w/2, cy+h/2), (cx-w/2, cy+h/2)],
            (70, 70, 70), PRETO, e, seed)
    p.forma([(cx-w*0.38, cy-h*0.38), (cx+w*0.38, cy-h*0.38), (cx+w*0.38, cy+h*0.32), (cx-w*0.38, cy+h*0.32)],
            BRANCO, PRETO, max(5, e-4), seed+1)


def mao(p, cx, cy, tam, seed, cor=PELE):
    e = max(7, int(tam * 0.05))
    p.forma([(cx-tam*0.16, cy+tam*0.28), (cx-tam*0.20, cy-tam*0.06), (cx-tam*0.10, cy-tam*0.30),
             (cx, cy-tam*0.34), (cx+tam*0.10, cy-tam*0.30), (cx+tam*0.20, cy-tam*0.04),
             (cx+tam*0.18, cy+tam*0.28)], cor, PRETO, e, seed)
    for k in range(3):
        x = cx - tam*0.10 + k*tam*0.10
        p.traco([(x, cy-tam*0.26), (x, cy-tam*0.02)], PRETO, max(4, e-5), seed+2+k, 1.6)


def vaso(p, cx, cy, tam, seed, aberto=0.0):
    """Vaso sanguíneo: quanto maior `aberto`, mais largo o canal."""
    e = max(7, int(tam * 0.045))
    h = tam * (0.10 + 0.16 * aberto)
    p.forma([(cx-tam*0.45, cy-h), (cx+tam*0.45, cy-h), (cx+tam*0.45, cy+h), (cx-tam*0.45, cy+h)],
            VERMELHO if aberto > 0.4 else ROSA, PRETO, e, seed)
    for k in range(4):
        p.bola(cx - tam*0.30 + k*tam*0.20, cy, h*0.45, BRANCO, PRETO, max(4, e-5), seed+2+k)


def barras(p, cx, cy, tam, seed, valores, cores, rotulos=None):
    """Gráfico de barras torto."""
    e = max(6, int(tam * 0.035))
    n = len(valores)
    lw = tam * 0.72 / n
    mx = max(valores) or 1
    base = cy + tam * 0.30
    for k, v in enumerate(valores):
        x = cx - tam*0.36 + k*lw + lw*0.5
        alt = tam * 0.56 * (v / mx)
        p.forma([(x-lw*0.36, base), (x+lw*0.36, base), (x+lw*0.36, base-alt), (x-lw*0.36, base-alt)],
                cores[k], PRETO, e, seed+k)
    p.traco([(cx-tam*0.42, base), (cx+tam*0.42, base)], PRETO, e, seed+40, 2.4)


def certo(p, cx, cy, tam, seed, cor=VERDE):
    p.traco([(cx-tam*0.30, cy), (cx-tam*0.08, cy+tam*0.26), (cx+tam*0.32, cy-tam*0.28)],
            cor, max(8, int(tam*0.13)), seed, 3.0)


def errado(p, cx, cy, tam, seed, cor=VERMELHO):
    p.xis(cx, cy, tam*0.28, cor, max(8, int(tam*0.13)), seed)


def regua(p, cx, cy, tam, seed):
    e = max(6, int(tam*0.035))
    w, h = tam*0.80, tam*0.12
    p.forma([(cx-w/2, cy-h/2), (cx+w/2, cy-h/2), (cx+w/2, cy+h/2), (cx-w/2, cy+h/2)],
            AMARELO, PRETO, e, seed)
    for k in range(1, 8):
        x = cx - w/2 + k*w/8
        p.traco([(x, cy-h/2), (x, cy-h/2 + (h*0.55 if k % 2 else h*0.85))], PRETO, max(4, e-3), seed+k, 1.4)


def arvore(p, cx, cy, tam, seed):
    e = max(7, int(tam*0.045))
    p.forma([(cx-tam*0.07, cy+tam*0.40), (cx+tam*0.07, cy+tam*0.40),
             (cx+tam*0.05, cy-tam*0.05), (cx-tam*0.05, cy-tam*0.05)], MARROM, PRETO, e, seed)
    p.bola(cx, cy-tam*0.22, tam*0.26, VERDE, PRETO, e, seed+1)
    p.bola(cx-tam*0.20, cy-tam*0.08, tam*0.17, VERDE, PRETO, e, seed+2)
    p.bola(cx+tam*0.20, cy-tam*0.08, tam*0.17, VERDE, PRETO, e, seed+3)


def anticorpo(p, cx, cy, tam, seed, cor=VERDE):
    e = max(6, int(tam*0.09))
    p.traco([(cx, cy+tam*0.28), (cx, cy)], cor, e, seed, 2.0)
    p.traco([(cx, cy), (cx-tam*0.24, cy-tam*0.26)], cor, e, seed+1, 2.0)
    p.traco([(cx, cy), (cx+tam*0.24, cy-tam*0.26)], cor, e, seed+2, 2.0)
