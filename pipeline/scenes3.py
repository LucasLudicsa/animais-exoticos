# -*- coding: utf-8 -*-
"""24 cartelas de Paint: risco grosso, cor chapada, e foto de verdade nas pancadas."""
import math
from art2 import (W, H, BRANCO, PRETO, VERMELHO, AZUL, AMARELO, VERDE, ROSA,
                  MARROM, CINZA, LARANJA, PELE, Paint, aranha, texto, cola, font, pop,
                  menino, suor, balao_susto)

CY = 780          # centro do desenho
FOTOS = {0: "aranha_0", 3: "n_chao", 9: "aranha_0", 14: "n_cacho", 17: "n_porto", 21: "n_butantan"}

# contornos simplificados na marra — poucos pontos, bem tortos, mas reconhecíveis
def _mapa(norm, cx, cy, larg, alt):
    return [(cx - larg / 2 + x * larg, cy - alt / 2 + y * alt) for x, y in norm]

_BR = [(0.10,0.24),(0.00,0.32),(0.20,0.38),(0.35,0.47),(0.41,0.59),(0.40,0.69),(0.51,0.82),
       (0.41,0.90),(0.52,0.99),(0.64,0.86),(0.73,0.74),(0.88,0.46),(0.97,0.28),(0.74,0.19),
       (0.60,0.08),(0.35,0.00),(0.15,0.08),(0.12,0.16)]
_AU = [(0.03,0.53),(0.05,0.39),(0.23,0.27),(0.44,0.08),(0.57,0.07),(0.55,0.17),(0.67,0.25),
       (0.71,0.02),(0.87,0.37),(0.97,0.61),(0.90,0.84),(0.81,0.96),(0.58,0.83),(0.40,0.72),
       (0.26,0.80),(0.12,0.84),(0.03,0.79)]

BRASIL = _mapa(_BR, 540, 790, 650, 820)
AUSTRA = _mapa(_AU, 540, 790, 780, 660)



# ---- seta + rótulo: (texto, alvo_x, alvo_y, rotulo_x, rotulo_y, t0, cor, tamanho)
SETAS = {
 1:  [("NÃO É AQUI", 540, 900, 700, 1180, 1.35, VERMELHO, 48)],
 2:  [("A ARANHA",   700, 1000, 840, 1240, 1.20, PRETO, 52)],
 3:  [("O CHÃO",     600, 980, 300, 1200, 0.75, BRANCO, 74)],
 4:  [("NERVO",      300, 820, 240, 560, 0.35, PRETO, 46),
      ("TRAVOU",     640, 820, 830, 1090, 1.30, VERMELHO, 48)],
 5:  [("CAMUNDONGO", 560, 1020, 810, 1210, 1.35, PRETO, 40)],
 6:  [("1 GRÃO",     620, 700, 850, 520, 0.85, PRETO, 46)],
 7:  [("A DOSE",     790, 760, 880, 520, 1.00, VERMELHO, 46)],
 8:  [("SEM SAÍDA",  230, 1020, 740, 560, 0.55, VERMELHO, 48)],
 9:  [("PRESAS",     560, 720, 300, 450, 0.45, BRANCO, 76)],
 10: [("PERNAS PRA CIMA", 660, 420, 800, 250, 0.30, VERMELHO, 40),
      ("PRESAS",     540, 900, 250, 1120, 0.85, PRETO, 44)],
 11: [("VEM PRA CIMA", 470, 760, 300, 400, 0.30, VERMELHO, 44)],
 12: [("SÓ ELA",     540, 560, 800, 420, 0.55, PRETO, 46)],
 13: [("DENTRO DE CASA", 540, 800, 810, 500, 0.65, PRETO, 40)],
 16: [("ESCONDIDA",  540, 840, 840, 540, 0.95, VERMELHO, 44)],
 17: [("EUROPA",     700, 820, 320, 1190, 0.45, BRANCO, 76)],
 18: [("ANTÍDOTO",   430, 790, 240, 500, 1.20, VERDE, 46)],
 20: [("HORAS",      400, 880, 230, 1160, 1.10, PRETO, 50)],
 21: [("BUTANTAN",   620, 820, 340, 1190, 0.45, BRANCO, 70)],
 22: [("VIRA REMÉDIO", 540, 780, 800, 480, 1.25, VERDE, 42)],
}

def _mov(pts, dx, dy, k=1.0):
    return [(x * k + dx, y * k + dy) for x, y in pts]


def cena(i, t, d, s, ac, p):
    """Desenha a cartela i no Paint p. s = semente do tremor (muda 10x por segundo)."""

    # ---------------------------------------------------------------- 1 GANCHO
    if i == 0:
        if t > 2.3:
            e = pop(t, 2.3)
            aranha(p, W / 2, CY + 40, 470 * e, s, armada=False, fill=MARROM)
        return

    if i == 1:
        e = pop(t, 0.0)
        p.forma(_mov(AUSTRA, 0, 0, e), AMARELO, PRETO, 15, s)
        if t > 0.45:
            cola(p.im, texto("AUSTRÁLIA", font("marker", 64), PRETO), W / 2, CY + 300)
        if t > 0.9:
            p.xis(W / 2, CY, 330 * pop(t, 0.9, 0.18), VERMELHO, 40, s)
        return

    if i == 2:
        e = pop(t, 0.0)
        p.forma(_mov(BRASIL, 0, 0, e), VERDE, PRETO, 15, s)
        if t > 0.55:
            cola(p.im, texto("BRASIL", font("marker", 86), BRANCO, PRETO, 7), 470, CY - 90)
        if t > 1.0:
            k = pop(t, 1.0, 0.2)
            aranha(p, 700, CY + 250, 210 * k, s, armada=False, fill=MARROM)
        return

    if i == 3:      # foto da mata + aranha andando por cima
        x = 230 + (t / d) * 580
        aranha(p, x, 1190, 230, s, armada=False, fill=MARROM)
        return

    if i == 4:
        y = CY + 40
        p.traco([(120, y), (960, y)], PRETO, 15, s)
        for k in range(4):
            p.bola(230 + k * 200, y, 46, AMARELO, PRETO, 13, s + k)
        if t > 1.0:
            p.xis(630, y, 110 * pop(t, 1.0, 0.18), VERMELHO, 26, s)
        return

    if i == 5:
        e = pop(t, 0.0)
        cola(p.im, texto("6 µg", font("marker", int(250 * max(e, .01))), VERMELHO, PRETO, 9), W / 2, CY - 40)
        if t > 0.9:
            k = pop(t, 0.9, 0.2)
            cx, cy = W / 2, CY + 250
            p.oval(cx, cy, 110 * k, 70 * k, CINZA, PRETO, 12, s)
            p.bola(cx - 95 * k, cy - 40 * k, 38 * k, CINZA, PRETO, 11, s + 1)
            p.bola(cx + 95 * k, cy - 40 * k, 38 * k, CINZA, PRETO, 11, s + 2)
            p.traco([(cx + 105 * k, cy + 15 * k), (cx + 190 * k, cy + 55 * k)], PRETO, 10, s + 3)
        return

    if i == 6:
        e = pop(t, 0.0)
        p.caixa(W / 2 - 150 * e, CY - 150 * e, W / 2 + 150 * e, CY + 150 * e, BRANCO, PRETO, 15, s)
        if t > 0.7:
            cola(p.im, texto("60 µg", font("marker", 96), PRETO), W / 2, CY + 300)
        return

    if i == 7:
        p.caixa(300 - 150, CY - 150, 300 + 150, CY + 150, BRANCO, PRETO, 15, s)
        cola(p.im, texto("60 µg", font("marker", 70), PRETO), 300, CY + 250)
        if t > 0.6:
            k = pop(t, 0.6, 0.2)
            p.bola(790, CY, 22 * k, VERMELHO, PRETO, 9, s + 5)
            cola(p.im, texto("6 µg", font("marker", 70), VERMELHO, PRETO, 5), 790, CY + 250)
        return

    if i == 8:
        p.traco([(180, CY - 320), (180, CY + 300), (900, CY + 300)], PRETO, 16, s)
        aranha(p, 380, CY + 110, 330, s, armada=False, fill=MARROM)
        return

    if i == 9:      # FOTO: a aranha de verdade
        return

    if i == 10:
        aranha(p, W / 2, CY + 20, 500, s, armada=True, fill=MARROM)
        return

    if i == 11:
        f = min(1.0, t / max(d, .01))
        menino(p, 830, CY + 210, 300, s, cara="medo",
               bob=math.sin(t * 11) * 9, bracos=0.45 + 0.25 * math.sin(t * 7))
        suor(p, 830, CY + 60, 300, s, k=abs(math.sin(t * 6)))
        k = 0.80 + 0.80 * f
        aranha(p, 400 + 60 * f, CY + 150, 400 * k, s, armada=True, fill=MARROM)
        if t > 0.5:
            balao_susto(p, 830, CY - 190, 300, s, "!")
        return

    if i == 12:
        aranha(p, W / 2, CY - 150, 330, s, armada=True, fill=MARROM)
        for j in range(3):
            if t > 0.25 + j * 0.2:
                x = 280 + j * 260
                aranha(p, x, CY + 370, 170, s + j * 3, armada=False, fill=CINZA)
                p.xis(x, CY + 370, 105, VERMELHO, 20, s + j)
        return

    if i == 13:
        e = pop(t, 0.0)
        p.forma(_mov([(300, 640), (540, 460), (780, 640)], 0, 0, 1), VERMELHO, PRETO, 15, s)
        p.caixa(340, 640, 740, 1010, AMARELO, PRETO, 15, s + 1)
        p.caixa(490, 830, 590, 1010, MARROM, PRETO, 12, s + 2)
        menino(p, 430, 905, 230, s, cara="ok", bob=math.sin(t * 5) * 5)
        if t > 1.1:
            aranha(p, 690, 940, 135 * pop(t, 1.1, .2), s, armada=False, fill=MARROM)
        return

    if i == 14:     # sapato / cortina / FOTO banana
        seg = d / 3.0
        j = min(2, int(t / seg))
        tl = t - j * seg
        e = pop(tl, 0.0, 0.18)
        if j == 0:
            p.forma([(250, CY + 40), (290, CY - 130), (440, CY - 140), (520, CY - 10),
                     (700, CY + 40), (780, CY + 90), (785, CY + 150), (255, CY + 150)],
                    AZUL, PRETO, 16, s)
            p.traco([(250, CY + 110), (785, CY + 110)], PRETO, 11, s + 1)
            p.traco([(330, CY - 96), (470, CY - 36)], PRETO, 10, s + 2)
            p.traco([(315, CY - 44), (455, CY + 16)], PRETO, 10, s + 3)
            menino(p, 830, CY - 120, 280, s, cara="medo", bob=math.sin(t * 9) * 7, bracos=0.5)
        elif j == 1:
            p.traco([(140, 400), (940, 400)], PRETO, 20, s)
            for c in range(3):
                x0 = 180 + c * 250
                p.forma([(x0, 410), (x0 + 200, 410), (x0 + 230, 1180), (x0 - 30, 1180)],
                        VERMELHO, PRETO, 14, s + c, amp=6.0)
        if tl > 0.85 and j < 2:
            aranha(p, 640, CY + 300, 150, s, armada=False, fill=MARROM)
        return

    if i == 15:
        e = pop(t, 0.0)
        cola(p.im, texto("4 000", font("marker", int(200 * max(e, .01))), VERMELHO, PRETO, 9), W / 2, CY - 60)
        if t > 0.8:
            cola(p.im, texto("por ano", font("hand", 78), PRETO), W / 2, CY + 180)
        return

    if i == 16:
        e = pop(t, 0.0)
        p.caixa(250, CY - 130, 830, CY + 250, AMARELO, PRETO, 15, s)
        for c in range(4):
            x = 250 + (c + 1) * 116
            p.traco([(x, CY - 130), (x, CY + 250)], PRETO, 9, s + c)
        if t > 0.8:
            aranha(p, 540, CY + 60, 190 * pop(t, 0.8, .2), s, armada=False, fill=MARROM)
        return

    if i == 17:     # FOTO porto
        return

    if i == 18:
        e = pop(t, 0.0)
        p.caixa(W / 2 - 110 * e, CY - 190 * e, W / 2 + 110 * e, CY - 130 * e, CINZA, PRETO, 12, s)
        p.caixa(W / 2 - 150 * e, CY - 130 * e, W / 2 + 150 * e, CY + 240 * e, VERDE, PRETO, 15, s + 1)
        if t > 1.0:
            cola(p.im, texto("SORO", font("marker", 74), BRANCO, PRETO, 6), W / 2, CY + 60)
        menino(p, 790, CY + 150, 300, s, cara="dor", bob=math.sin(t * 8) * 8)
        suor(p, 790, CY, 300, s, k=abs(math.sin(t * 5)), n=2)
        return

    if i == 19:
        e = pop(t, 0.0)
        cola(p.im, texto("?", font("marker", int(340 * max(e, .01))), VERDE, PRETO, 10), W / 2, CY)
        if t > 1.2:
            k = pop(t, 1.2, .5)
            for j in range(8):
                a = j * math.pi / 4
                r0, r1 = 230, 230 + 130 * k
                p.traco([(W / 2 + r0 * math.cos(a), CY + r0 * math.sin(a)),
                         (W / 2 + r1 * math.cos(a), CY + r1 * math.sin(a))], VERDE, 14, s + j)
        return

    if i == 20:
        e = pop(t, 0.0)
        ccx, ccy = 330, CY - 40
        p.bola(ccx, ccy, 175 * e, BRANCO, PRETO, 15, s)
        for h in range(12):
            a = h * math.pi / 6
            p.traco([(ccx + 142 * math.cos(a), ccy + 142 * math.sin(a)),
                     (ccx + 168 * math.cos(a), ccy + 168 * math.sin(a))], PRETO, 8, s + h)
        gir = t * 3.4
        ang = -math.pi / 2 + gir * 2 * math.pi
        p.traco([(ccx, ccy), (ccx + 122 * math.cos(ang), ccy + 122 * math.sin(ang))], VERMELHO, 13, s + 20)
        p.traco([(ccx, ccy), (ccx + 78 * math.cos(ang / 6), ccy + 78 * math.sin(ang / 6))], PRETO, 15, s + 21)
        # o menino, sem entender nada
        cara = "choque" if (t % 1.0) < 0.55 else "confuso"
        menino(p, 780, CY + 60, 330, s, cara=cara,
               bob=math.sin(t * 10) * 11, bracos=0.55 + 0.35 * math.sin(t * 8))
        suor(p, 780, CY - 110, 330, s, k=abs(math.sin(t * 6)))
        if t > 0.4:
            balao_susto(p, 790, CY - 250, 330, s, "?!")
        return

    if i == 21:     # FOTO laboratório
        return

    if i == 22:
        e = pop(t, 0.0)
        p.oval(W / 2, CY, 230 * e, 130 * e, BRANCO, PRETO, 16, s)
        p.traco([(W / 2 - 230 * e, CY), (W / 2 + 230 * e, CY)], PRETO, 14, s + 1)
        p.d.pieslice([W / 2 - 228 * e, CY - 128 * e, W / 2 + 228 * e, CY + 128 * e], 0, 180, fill=VERDE)
        p.oval(W / 2, CY, 230 * e, 130 * e, None, PRETO, 16, s)
        p.traco([(W / 2 - 230 * e, CY), (W / 2 + 230 * e, CY)], PRETO, 14, s + 1)
        if t > 1.0:
            p.traco([(W / 2 - 90, CY + 300), (W / 2 - 20, CY + 370), (W / 2 + 110, CY + 220)],
                    VERDE, 26, s + 9)
        return

    if i == 23:
        aranha(p, 380, CY - 110, 340, s, armada=False, cor_perna=VERDE, fill=VERDE)
        menino(p, 810, CY + 120, 320, s, cara="feliz",
               bob=math.sin(t * 5) * 7, bracos=0.30 + 0.30 * math.sin(t * 4))
        if t > 1.0:
            k = pop(t, 1.0, .25)
            p.caixa(380 - 52 * k, CY + 190, 380 + 52 * k, CY + 236, CINZA, PRETO, 11, s + 3)
            p.caixa(380 - 90 * k, CY + 236, 380 + 90 * k, CY + 410, VERDE, PRETO, 14, s + 4)
            cola(p.im, texto("REMÉDIO", font("marker", 40), BRANCO, PRETO, 5), 380, CY + 325)
        return
