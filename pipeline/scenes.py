# -*- coding: utf-8 -*-
"""As 24 cartelas."""
from PIL import Image, ImageDraw
from art import (W, H, BREU, BREU_J, MATA, AREIA, URUCUM, JADE, DIM, DIM_U, CINZA,
                 font, Pad, aranha, text_img, paste, ease)
import math

CAP_Y = 1500          # linha de base da legenda (acima da zona bloqueada)
ART_CY = 830          # centro óptico do assunto

BRASIL = [(0.1025,0.2359),(0.0025,0.3205),(0.085,0.3718),(0.2,0.3795),(0.35,0.4744),(0.41,0.5897),(0.4025,0.6949),(0.485,0.7846),(0.51,0.8205),(0.41,0.9026),(0.515,0.9923),(0.5475,0.9487),(0.6375,0.859),(0.725,0.7385),(0.875,0.5769),(0.8875,0.4615),(0.97,0.2769),(0.8875,0.2231),(0.7425,0.1923),(0.6375,0.1462),(0.6,0.0769),(0.56,0.0231),(0.35,-0.0051),(0.265,0.0282),(0.1525,0.0821),(0.105,0.1),(0.115,0.1564)]
AUSTRALIA = [(0.0279,0.5333),(0.0465,0.3933),(0.2326,0.2667),(0.3488,0.1267),(0.4372,0.08),(0.4791,0.0367),(0.5744,0.0733),(0.5465,0.1667),(0.6721,0.25),(0.7093,0.0233),(0.786,0.23),(0.8651,0.37),(0.9651,0.6067),(0.9023,0.8367),(0.814,0.96),(0.6721,0.9367),(0.5814,0.8333),(0.5116,0.75),(0.3953,0.72),(0.2558,0.7967),(0.1163,0.8367),(0.0698,0.7867),(0.0349,0.5333)]


def poly(size, pts, color, lw, fechar=True):
    pad = Pad(size, size)
    p = [(x * size, y * size) for x, y in pts]
    if fechar:
        p = p + [p[0]]
    pad.line(p, color, lw)
    return pad.out()


def _costa(size, color, lw):
    pad = Pad(size, size)
    leste = [(0.97,0.2769),(0.8875,0.4615),(0.875,0.5769),(0.725,0.7385),(0.6375,0.859),(0.5475,0.9487)]
    pad.line([(x * size, y * size) for x, y in leste], color, lw)
    return pad.out()


def frasco(size, color, lw, tampa=None):
    pad = Pad(size, size)
    s = size / 200.0
    def P(x, y): return (x * s, y * s)
    corpo = [P(82,48),P(82,68),P(58,92),P(58,168),P(66,178),P(134,178),P(142,168),
             P(142,92),P(118,68),P(118,48)]
    pad.line(corpo, color, lw)
    pad.line([P(76,28),P(124,28),P(124,48),P(76,48),P(76,28)], tampa or color, lw)
    pad.line([P(58,138),P(142,138)], color, lw * 0.75)
    return pad.out()


def molecula(size, color, lw):
    pad = Pad(size, size)
    c = size / 2
    r = size * 0.24
    nos = [(c, c)]
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        nos.append((c + r * math.cos(a), c + r * math.sin(a)))
    for n in nos[1:]:
        pad.line([nos[0], n], color, lw * 0.8)
    for i, n in enumerate(nos):
        rr = size * (0.055 if i == 0 else 0.038)
        pad.ellipse(n[0], n[1], rr, rr, color, lw)
    for i in range(1, 6):
        j = i + 1 if i < 5 else 1
        pad.line([nos[i], nos[j]], color, lw * 0.55)
    return pad.out()


def cubo_sal(size, color, lw):
    pad = Pad(size, size)
    s = size / 100.0
    a, b = 22 * s, 78 * s
    o = 14 * s
    pad.line([(a,b),(a,a+o),(b-o,a+o),(b-o,b),(a,b)], color, lw)
    pad.line([(a,a+o),(a+o,a),(b,a),(b-o,a+o)], color, lw)
    pad.line([(b,a),(b,b-o),(b-o,b)], color, lw)
    return pad.out()


def sapato(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(36*s,124*s),(36*s,148*s),(44*s,158*s),(150*s,158*s),(164*s,148*s),
              (158*s,128*s),(112*s,112*s),(86*s,86*s),(56*s,86*s),(36*s,124*s)], color, lw)
    pad.line([(36*s,140*s),(164*s,150*s)], color, lw*0.7)
    return pad.out()


def cortina(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(30*s,44*s),(170*s,44*s)], color, lw)
    for i in range(5):
        x = (44 + i * 28) * s
        pad.line([(x,50*s),(x-6*s,96*s),(x+6*s,140*s),(x-4*s,168*s)], color, lw*0.85)
    return pad.out()


def banana(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    for i, (dx, dy, rot) in enumerate([(0,0,0),(-22,14,0),(22,16,0)]):
        pad.line([(78*s+dx*s,52*s+dy*s),(58*s+dx*s,90*s+dy*s),(70*s+dx*s,134*s+dy*s),
                  (104*s+dx*s,152*s+dy*s),(126*s+dx*s,136*s+dy*s)], color, lw*0.9)
    pad.line([(96*s,40*s),(96*s,54*s)], color, lw)
    return pad.out()


def caixa(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(40*s,80*s),(160*s,80*s),(160*s,156*s),(40*s,156*s),(40*s,80*s)], color, lw)
    for i in range(5):
        x = (54 + i * 23) * s
        pad.line([(x,80*s),(x,156*s)], color, lw*0.6)
    pad.line([(40*s,80*s),(62*s,58*s),(182*s,58*s),(160*s,80*s)], color, lw)
    return pad.out()


def navio(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(26*s,132*s),(174*s,132*s),(158*s,160*s),(42*s,160*s),(26*s,132*s)], color, lw)
    for i in range(3):
        x = (58 + i * 32) * s
        pad.line([(x,132*s),(x,104*s),(x+24*s,104*s),(x+24*s,132*s)], color, lw*0.8)
    pad.line([(14*s,176*s),(186*s,176*s)], color, lw*0.6)
    return pad.out()


def nervo(size, color, lw, bloqueio=0.0):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(16*s,100*s),(184*s,100*s)], color, lw)
    for i in range(4):
        x = (44 + i * 38) * s
        pad.ellipse(x, 100*s, 9*s, 9*s, color, lw*0.9)
    if bloqueio > 0:
        cx = 120 * s
        r = 26 * s * bloqueio
        pad.line([(cx-r,100*s-r),(cx+r,100*s+r)], URUCUM, lw*1.3)
        pad.line([(cx-r,100*s+r),(cx+r,100*s-r)], URUCUM, lw*1.3)
    return pad.out()


def casa(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(30*s,96*s),(100*s,44*s),(170*s,96*s)], color, lw)
    pad.line([(44*s,96*s),(44*s,166*s),(156*s,166*s),(156*s,96*s)], color, lw)
    pad.line([(86*s,166*s),(86*s,120*s),(114*s,120*s),(114*s,166*s)], color, lw*0.8)
    return pad.out()


def balao(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(74*s,60*s),(74*s,52*s),(126*s,52*s),(126*s,60*s)], color, lw)
    pad.line([(64*s,60*s),(136*s,60*s),(146*s,150*s),(54*s,150*s),(64*s,60*s)], color, lw)
    pad.line([(58*s,112*s),(142*s,112*s)], color, lw*0.7)
    return pad.out()


def mata(size, color, lw):
    pad = Pad(size, size); s = size / 200.0
    pad.line([(10*s,168*s),(190*s,168*s)], color, lw)
    for i, x in enumerate([32, 66, 104, 146, 176]):
        h = [96, 58, 78, 44, 88][i]
        pad.line([(x*s,168*s),(x*s,h*s)], color, lw*0.85)
        pad.line([(x*s,(h+16)*s),(x*s-16*s,(h+2)*s)], color, lw*0.6)
        pad.line([(x*s,(h+26)*s),(x*s+16*s,(h+12)*s)], color, lw*0.6)
    return pad.out()


# ------------------------------------------------------------------ cenas
def build(i, accent, bg):
    """Devolve (assets, fn(base, tl, dur)) para a cartela i."""
    A = {}

    if i == 0:
        A["sp"] = aranha(760, DIM, DIM, traco=4.2, abertura=0.25)
        A["tt"] = text_img("ARMADEIRA", font("display", 128), AREIA)
        A["sub"] = text_img("Phoneutria nigriventer", font("mono", 38), accent)
        def f(b, t, d):
            paste(b, A["sp"], W/2, ART_CY, alpha=min(1.0, t/2.2)*0.9)
            if t > 1.9:
                k = ease((t-1.9)/0.7)
                paste(b, A["tt"], W/2, 470, scale=0.96+0.04*k, alpha=k)
            if t > 3.1:
                paste(b, A["sub"], W/2, 600, alpha=ease((t-3.1)/0.6))
        return A, f

    if i == 1:
        A["au"] = poly(620, AUSTRALIA, DIM, 4.5)
        A["x1"] = text_img("NAO", font("display", 96), URUCUM)
        def f(b, t, d):
            paste(b, A["au"], W/2, ART_CY, alpha=min(1.0, t/0.10))
            if t > 1.1:
                k = ease((t-1.1)/0.35)
                pad = Pad(560, 560)
                r = 250*k
                pad.line([(280-r,280-r),(280+r,280+r)], URUCUM, 14)
                pad.line([(280-r,280+r),(280+r,280-r)], URUCUM, 14)
                paste(b, pad.out(), W/2, ART_CY)
        return A, f

    if i == 2:
        A["br"] = poly(640, BRASIL, AREIA, 5.0)
        A["cs"] = _costa(640, URUCUM, 9.0)
        A["aq"] = text_img("AQUI", font("display", 104), URUCUM)
        def f(b, t, d):
            paste(b, A["br"], W/2, ART_CY, alpha=min(1.0, t/0.10))
            if t > 0.9:
                paste(b, A["cs"], W/2, ART_CY, alpha=ease((t-0.9)/0.5))
            if t > 1.8:
                k = ease((t-1.8)/0.4)
                paste(b, A["aq"], W/2, 420, scale=0.9+0.1*k, alpha=k)
        return A, f

    if i == 3:
        A["mt"] = mata(820, DIM, 5.0)
        A["sp"] = aranha(190, AREIA, URUCUM, traco=6.0, abertura=0.2)
        def f(b, t, d):
            paste(b, A["mt"], W/2, ART_CY, alpha=min(1.0, t/0.10))
            x = 250 + (t/d) * 560
            paste(b, A["sp"], x, ART_CY+238, alpha=min(1.0, t/0.10))
        return A, f

    if i == 4:
        def f(b, t, d):
            k = min(1.0, t/0.10)
            paste(b, nervo(820, AREIA, 5.0, bloqueio=max(0.0,(t-1.1)/0.5)), W/2, ART_CY, alpha=min(1.0, t/0.10))
        return A, f

    if i == 5:
        A["n"] = text_img("6", font("display", 300), AREIA)
        A["u"] = text_img("µg", font("display", 110), URUCUM)
        A["l"] = text_img("mata um camundongo", font("mono", 36), CINZA)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["n"], W/2-70, ART_CY-40, scale=0.9+0.1*k, alpha=k)
            if t > 0.5:
                paste(b, A["u"], W/2+150, ART_CY+40, alpha=ease((t-0.5)/0.4))
            if t > 1.3:
                paste(b, A["l"], W/2, ART_CY+240, alpha=ease((t-1.3)/0.5))
        return A, f

    if i == 6:
        A["c"] = cubo_sal(420, AREIA, 5.0)
        A["l"] = text_img("um grão de sal", font("mono", 40), CINZA)
        A["v"] = text_img("60 µg", font("display", 96), AREIA)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["c"], W/2, ART_CY-60, scale=0.85+0.15*k, alpha=k)
            if t > 0.8:
                paste(b, A["l"], W/2, ART_CY+190, alpha=ease((t-0.8)/0.4))
            if t > 1.5:
                paste(b, A["v"], W/2, ART_CY+300, alpha=ease((t-1.5)/0.4))
        return A, f

    if i == 7:
        A["c"] = cubo_sal(360, DIM, 4.5)
        A["l6"] = text_img("60 µg", font("mono", 38), CINZA)
        A["l1"] = text_img("6 µg", font("mono", 38), URUCUM)
        def f(b, t, d):
            paste(b, A["c"], W/2-210, ART_CY, alpha=min(1.0, t/0.10))
            paste(b, A["l6"], W/2-210, ART_CY+230, alpha=min(1.0, t/0.10))
            if t > 0.7:
                k = ease((t-0.7)/0.5)
                pad = Pad(120,120); pad.disc(60,60, 11, URUCUM)
                paste(b, pad.out(), W/2+210, ART_CY, alpha=k, scale=0.5+0.5*k)
                paste(b, A["l1"], W/2+210, ART_CY+230, alpha=k)
        return A, f

    if i == 8:
        A["sp"] = aranha(420, AREIA, URUCUM, traco=5.0, abertura=0.25)
        def f(b, t, d):
            pad = Pad(900, 700)
            pad.line([(120,40),(120,560),(820,560)], DIM, 6)
            paste(b, pad.out(), W/2, ART_CY)
            paste(b, A["sp"], W/2-190, ART_CY+130, alpha=min(1.0, t/0.10))
        return A, f

    if i == 9:
        A["sp"] = {}
        for n in range(9):
            A["sp"][n] = aranha(900, AREIA, URUCUM, traco=5.4, abertura=0.2+0.8*(n/8))
        A["t"] = text_img("ELA SE ARMA", font("display", 92), URUCUM)
        def f(b, t, d):
            n = min(8, int((t/0.9)*8))
            paste(b, A["sp"][n], W/2, ART_CY-30, alpha=min(1.0, t/0.10))
            if t > 1.35:
                k = ease((t-1.35)/0.4)
                paste(b, A["t"], W/2, 1290, scale=0.94+0.06*k, alpha=k)
        return A, f

    if i == 10:
        A["sp"] = aranha(1500, AREIA, URUCUM, traco=5.6, abertura=1.0)
        def f(b, t, d):
            s = 1.0 + 0.09*ease(min(1.0, t/d))
            paste(b, A["sp"], W/2, ART_CY-140, scale=s, alpha=min(1.0, t/0.10))
        return A, f

    if i == 11:
        A["sp"] = aranha(1100, AREIA, URUCUM, traco=5.6, abertura=1.0)
        def f(b, t, d):
            k = ease(min(1.0, t/d))
            paste(b, A["sp"], W/2, ART_CY-40+120*k, scale=0.85+0.65*k, alpha=min(1.0, t/0.10))
        return A, f

    if i == 12:
        A["sp"] = aranha(360, AREIA, URUCUM, traco=6.0, abertura=1.0)
        A["ot"] = aranha(230, DIM, DIM, traco=6.0, abertura=0.0)
        def f(b, t, d):
            paste(b, A["sp"], W/2, ART_CY-120, alpha=min(1.0, t/0.10))
            for j in range(4):
                if t > 0.35 + j*0.16:
                    x = 220 + j*214
                    paste(b, A["ot"], x, ART_CY+190, alpha=ease((t-0.35-j*0.16)/0.3)*0.8)
        return A, f

    if i == 13:
        A["h"] = casa(660, AREIA, 5.0)
        A["sp"] = aranha(150, URUCUM, URUCUM, traco=6.5, abertura=0.4)
        def f(b, t, d):
            paste(b, A["h"], W/2, ART_CY, alpha=min(1.0, t/0.10))
            if t > 1.2:
                paste(b, A["sp"], W/2+120, ART_CY+150, alpha=ease((t-1.2)/0.4))
        return A, f

    if i == 14:
        A["a"] = sapato(560, AREIA, 5.2)
        A["b"] = cortina(560, AREIA, 5.2)
        A["c"] = banana(560, AREIA, 5.2)
        A["sp"] = aranha(120, URUCUM, URUCUM, traco=7.0, abertura=0.5)
        def f(b, t, d):
            seg = d/3.0
            j = min(2, int(t/seg))
            tl = t - j*seg
            im = [A["a"], A["b"], A["c"]][j]
            k = ease(min(1.0, tl/0.25))
            paste(b, im, W/2, ART_CY, scale=0.95+0.05*k, alpha=k)
            if tl > 0.75:
                ox = [(60,90),(0,120),(70,60)][j]
                paste(b, A["sp"], W/2+ox[0], ART_CY+ox[1], alpha=ease((tl-0.75)/0.35))
        return A, f

    if i == 15:
        A["n"] = text_img("4 000", font("display", 190), AREIA)
        A["l"] = text_img("casos por ano no Brasil", font("mono", 40), CINZA)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["n"], W/2, ART_CY-40, scale=0.92+0.08*k, alpha=k)
            if t > 0.8:
                paste(b, A["l"], W/2, ART_CY+140, alpha=ease((t-0.8)/0.4))
            if t > 1.4:
                kk = ease((t-1.4)/0.6)
                pad = Pad(760, 12); pad.line([(6,6),(6+748*kk,6)], URUCUM, 9)
                paste(b, pad.out(), W/2, ART_CY+240)
        return A, f

    if i == 16:
        A["cx"] = caixa(620, AREIA, 5.0)
        A["sp"] = aranha(150, URUCUM, URUCUM, traco=6.5, abertura=0.35)
        def f(b, t, d):
            paste(b, A["cx"], W/2, ART_CY, alpha=min(1.0, t/0.10))
            if t > 0.9:
                paste(b, A["sp"], W/2+20, ART_CY+40, alpha=ease((t-0.9)/0.4))
        return A, f

    if i == 17:
        A["nv"] = navio(700, AREIA, 5.0)
        def f(b, t, d):
            k = ease(min(1.0, t/d))
            paste(b, A["nv"], W/2-110+220*k, ART_CY, alpha=min(1.0, t/0.10))
        return A, f

    if i == 18:
        A["fr"] = frasco(520, JADE, 5.2)
        A["l"] = text_img("soro antiaracnídico", font("mono", 38), JADE)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["fr"], W/2, ART_CY-40, scale=0.9+0.1*k, alpha=k)
            if t > 1.0:
                paste(b, A["l"], W/2, ART_CY+230, alpha=ease((t-1.0)/0.45))
        return A, f

    if i == 19:
        A["q"] = text_img("?", font("display", 320), JADE)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["q"], W/2, ART_CY, scale=0.85+0.15*k, alpha=k)
            if t > 1.2:
                kk = ease((t-1.2)/0.9)
                pad = Pad(760, 760)
                for j in range(8):
                    a = j*math.pi/4
                    r0, r1 = 210*kk, (250+90*kk)*kk
                    pad.line([(380+r0*math.cos(a),380+r0*math.sin(a)),
                              (380+r1*math.cos(a),380+r1*math.sin(a))], JADE, 5)
                paste(b, pad.out(), W/2, ART_CY, alpha=0.8*kk)
        return A, f

    if i == 20:
        A["m"] = molecula(600, JADE, 5.0)
        A["l"] = text_img("PnTx2-6", font("mono", 42), JADE)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["m"], W/2, ART_CY-40, scale=0.88+0.12*k, alpha=k)
            if t > 1.2:
                paste(b, A["l"], W/2, ART_CY+250, alpha=ease((t-1.2)/0.45))
        return A, f

    if i == 21:
        A["b"] = balao(560, JADE, 5.2)
        A["l"] = text_img("pesquisa brasileira", font("mono", 38), CINZA)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["b"], W/2, ART_CY-40, scale=0.9+0.1*k, alpha=k)
            if t > 1.1:
                paste(b, A["l"], W/2, ART_CY+240, alpha=ease((t-1.1)/0.45))
        return A, f

    if i == 22:
        A["fr"] = frasco(460, JADE, 5.2)
        A["l"] = text_img("teste clínico", font("mono", 42), JADE)
        def f(b, t, d):
            k = ease(min(1.0, t/0.10))
            paste(b, A["fr"], W/2, ART_CY-60, scale=0.9+0.1*k, alpha=k)
            if t > 1.0:
                kk = ease((t-1.0)/0.5)
                pad = Pad(620, 12); pad.line([(6,6),(6+608*kk,6)], JADE, 8)
                paste(b, pad.out(), W/2, ART_CY+170)
                paste(b, A["l"], W/2, ART_CY+250, alpha=kk)
        return A, f

    if i == 23:
        A["sp"] = aranha(680, JADE, JADE, traco=5.0, abertura=0.85)
        A["fr"] = frasco(300, JADE, 5.0)
        def f(b, t, d):
            paste(b, A["sp"], W/2, ART_CY-70, alpha=min(1.0, t/0.10))
            if t > 1.1:
                k = ease((t-1.1)/0.6)
                paste(b, A["fr"], W/2, ART_CY+330, scale=0.85+0.15*k, alpha=k)
        return A, f

    def f(b, t, d):
        pass
    return A, f
