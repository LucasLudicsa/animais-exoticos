# -*- coding: utf-8 -*-
"""As 125 cartelas do vídeo longo."""
import math
from art2 import (BRANCO, PRETO, VERMELHO, AZUL, AMARELO, VERDE, ROSA, MARROM,
                  CINZA, LARANJA, PELE, texto, cola, font, pop, aranha, menino,
                  suor, balao_susto)
import obj16 as O

W, H = 1920, 1080
CY = 470


def T(p, txt, x, y, tam=150, cor=PRETO, esc=1.0, fonte="marker", contorno=None, esp=8):
    if esc < 0.02:
        return
    if contorno is None:
        contorno = BRANCO if cor != BRANCO else PRETO
    cola(p.im, texto(txt, font(fonte, max(8, int(tam * esc))), cor, contorno, esp), x, y)


def lista(p, itens, x, y, t, t0=0.0, passo=0.34, tam=56, sinal=None, seed=0):
    """Itens aparecendo um a um, com ✓ ou ✗ na frente."""
    for k, it in enumerate(itens):
        tt = t0 + k * passo
        if t < tt:
            break
        e = pop(t, tt, 0.18)
        yy = y + k * 92
        if sinal == "certo":
            O.certo(p, x - 60, yy, 92 * e, seed + k)
        elif sinal == "errado":
            O.errado(p, x - 60, yy, 92 * e, seed + k)
        else:
            p.bola(x - 60, yy, 16 * e, PRETO, PRETO, 6, seed + k)
        cola(p.im, texto(it, font("hand", tam), PRETO), x + 30 + texto(it, font("hand", tam), PRETO).width / 2, yy)


def desenha(i, c):
    p, t, d, s, ac = c["p"], c["t"], c["d"], c["s"], c["ac"]
    foto = c["foto"]

    # ============================================ 1 ABERTURA
    if i == 0:
        x = 300 + (t / d) * 900
        aranha(p, x, CY + 60, 300, s, fill=MARROM)
        T(p, "FOGE", 420, CY - 240, 110, CINZA, pop(t, 0.5))
        return
    if i == 1:
        aranha(p, 760, CY + 40, 430, s, fill=MARROM)
        T(p, "ESSA NÃO", 1330, CY - 60, 130, VERMELHO, pop(t, 0.15))
        return
    if i == 2:
        f = min(1.0, t / max(d, .01))
        aranha(p, 620 + 90 * f, CY + 60, 380 + 160 * f, s, armada=True, fill=MARROM)
        menino(p, 1480, CY + 190, 330, s, cara="medo", bob=math.sin(t * 11) * 9, bracos=0.5)
        suor(p, 1480, CY + 40, 330, s, k=abs(math.sin(t * 6)))
        return
    if i == 3:
        T(p, "ARMADEIRA", W / 2, CY, 190, VERMELHO, pop(t, 0.0), esp=10)
        aranha(p, W / 2, CY + 260, 220, s, fill=MARROM)
        return
    if i == 4:
        e = pop(t, 0.0)
        p.forma(_br(760, CY, 420 * e, 520 * e), VERDE, PRETO, 15, s)
        T(p, "BRASIL", 700, CY - 60, 90, BRANCO, min(1.0, t / .3), esp=7)
        if t > 0.6:
            aranha(p, 1320, CY + 60, 260 * pop(t, 0.6), s, fill=MARROM)
        return

    # ============================================ 2 QUEM E ELA
    if i == 5:
        T(p, "Phoneutria", W / 2, CY - 120, 140, PRETO, pop(t, 0.0), fonte="marker")
        aranha(p, W / 2, CY + 230, 280, s, fill=MARROM)
        return
    if i == 6:
        T(p, "9", 420, CY, 300, VERMELHO, pop(t, 0.0), esp=10)
        T(p, "espécies", 420, CY + 230, 80, PRETO, pop(t, 0.4), fonte="hand")
        for k in range(9):
            if t > 0.35 + k * 0.09:
                aranha(p, 950 + (k % 3) * 250, CY - 190 + (k // 3) * 230,
                       150 * pop(t, 0.35 + k * 0.09, .15), s + k * 7, fill=MARROM if k else VERMELHO)
        return
    if i == 7:
        foto("aranha_0")
        return
    if i == 8:
        aranha(p, 780, CY - 30, 420, s, fill=MARROM)
        O.regua(p, 780, CY + 300, 620, s + 3)
        T(p, "15 cm", 1420, CY - 40, 140, VERMELHO, pop(t, 0.5))
        return
    if i == 9:
        aranha(p, 700, CY + 20, 480, s, fill=MARROM)
        return
    if i == 10:
        # cabeça grande com os oito olhos
        p.bola(820, CY, 250, MARROM, PRETO, 16, s)
        pos = [(-120, -70), (0, -95), (120, -70), (-70, 10), (70, 10), (-120, 80), (0, 100), (120, 80)]
        for k, (dx, dy) in enumerate(pos):
            if t > 0.15 + k * 0.07:
                e = pop(t, 0.15 + k * 0.07, .12)
                p.bola(820 + dx, CY + dy, 40 * e, BRANCO, PRETO, 8, s + k)
                p.d.ellipse([820 + dx - 15, CY + dy - 15, 820 + dx + 15, CY + dy + 15], fill=PRETO)
        T(p, "8 OLHOS", 1450, CY - 60, 120, VERMELHO, pop(t, 0.7))
        return
    if i == 11:
        O.teia(p, 760, CY, 620, s)
        if t > 0.5:
            p.xis(760, CY, 300 * pop(t, 0.5, .2), VERMELHO, 34, s)
        T(p, "SEM TEIA", 1440, CY, 110, VERMELHO, pop(t, 0.9))
        return
    if i == 12:
        foto("L_ovos")
        return
    if i == 13:
        T(p, "+ DE 1000", W / 2, CY - 110, 190, VERMELHO, pop(t, 0.0), esp=10)
        for k in range(14):
            if t > 0.4 + k * 0.05:
                aranha(p, 380 + (k % 7) * 195, CY + 190 + (k // 7) * 150,
                       90 * pop(t, 0.4 + k * 0.05, .12), s + k * 5, fill=MARROM)
        return
    if i == 14:
        for k in range(10):
            x = 340 + (k % 5) * 300
            y = CY - 90 + (k // 5) * 260
            aranha(p, x, y, 130, s + k * 5, fill=CINZA if k > 1 else MARROM)
            if k > 1 and t > 0.25 + (k - 2) * 0.09:
                p.xis(x, y, 80 * pop(t, 0.25 + (k - 2) * 0.09, .12), VERMELHO, 16, s + k)
        return

    # ============================================ 3 CACADORA
    if i == 15:
        O.teia(p, 640, CY, 560, s)
        aranha(p, 640, CY, 160, s + 2, fill=CINZA)
        T(p, "ESPERA", 1380, CY, 120, CINZA, pop(t, 0.3))
        return
    if i == 16:
        x = 400 + (t / max(d, .01)) * 700
        aranha(p, x, CY + 40, 340, s, fill=MARROM)
        T(p, "VAI ATRÁS", 1460, CY - 220, 110, VERMELHO, pop(t, 0.2))
        return
    if i == 17:
        p.bola(1560, 190, 110, AMARELO, PRETO, 13, s + 40)
        p.traco([(120, CY + 330), (1800, CY + 330)], PRETO, 15, s + 1, 4.0)
        x = 300 + (t / max(d, .01)) * 1000
        aranha(p, x, CY + 230, 280, s, fill=MARROM)
        return
    if i == 18:
        itens = [("grilo", AMARELO), ("barata", MARROM), ("lagartixa", VERDE)]
        for k, (nome, cor) in enumerate(itens):
            if t > 0.2 + k * 0.42:
                e = pop(t, 0.2 + k * 0.42, .2)
                x = 480 + k * 480
                p.oval(x, CY, 110 * e, 62 * e, cor, PRETO, 12, s + k)
                for j in range(3):
                    p.traco([(x - 60 + j * 55, CY + 50), (x - 70 + j * 55, CY + 120)], PRETO, 8, s + k * 4 + j, 2.0)
                T(p, nome, x, CY + 200, 62, PRETO, 1.0, fonte="hand")
        return
    if i == 19:
        O.botaL(p, 700, CY + 40, 520, s)
        if t > 0.7:
            aranha(p, 760, CY + 90, 170 * pop(t, 0.7, .2), s + 3, fill=MARROM)
        return
    if i == 20:
        T(p, "PROBLEMA", W / 2, CY, 210, VERMELHO, pop(t, 0.0), esp=10)
        return
    if i == 21:
        O.botaL(p, 780, CY, 640, s)
        if t > 0.6:
            aranha(p, 850, CY + 50, 190 * pop(t, 0.6, .2), s + 3, fill=MARROM)
        return
    if i == 22:
        O.pilha_roupa(p, 560, CY + 80, 520, s)
        p.traco([(1120, CY - 320), (1800, CY - 320)], PRETO, 16, s + 9, 3.0)
        for k in range(3):
            x0 = 1150 + k * 210
            p.forma([(x0, CY - 310), (x0 + 170, CY - 310), (x0 + 195, CY + 330), (x0 - 25, CY + 330)],
                    VERMELHO, PRETO, 13, s + 12 + k, 6.0)
        return
    if i == 23:
        O.mao(p, 560, CY - 60, 420, s)
        aranha(p, 1120, CY + 90, 330, s + 4, fill=MARROM)
        if t > 0.6:
            balao_susto(p, 1120, CY - 200, 330, s, "!")
        return
    if i == 24:
        aranha(p, W / 2, CY + 40, 400, s, fill=MARROM)
        return
    if i == 25:
        aranha(p, W / 2, CY + 60, 560, s, armada=True, fill=MARROM)
        T(p, "SE ARMA", 1520, CY - 240, 120, VERMELHO, pop(t, 0.3))
        return

    # ============================================ 4 O VENENO
    if i == 26:
        T(p, "NEUROTOXINA", W / 2, CY, 150, VERMELHO, pop(t, 0.0), esp=9)
        return
    if i == 27 or i == 28 or i == 29 or i == 30:
        y = CY + 20
        p.traco([(220, y), (1700, y)], PRETO, 16, s, 3.4)
        for k in range(6):
            cor = AMARELO
            if i == 29 and t > 0.6 and k == 3:
                cor = VERMELHO
            if i == 30:
                cor = VERMELHO if (int(t * 6) + k) % 2 == 0 else AMARELO
            p.bola(340 + k * 250, y, 62, cor, PRETO, 13, s + k)
        if i == 28 and t > 0.3:
            xs = 340 + ((t - 0.3) / max(d - 0.3, .01)) * 1250
            p.bola(xs, y, 92, VERMELHO, PRETO, 13, s + 30)
        if i == 29 and t > 0.8:
            p.xis(1090, y, 130 * pop(t, 0.8, .2), VERMELHO, 28, s + 20)
        if i == 30:
            for k in range(4):
                p.traco([(340 + k * 250, y - 110), (330 + k * 250, y - 200)], VERMELHO, 12, s + 50 + k, 3.0)
        return
    if i == 31:
        menino(p, 700, CY + 140, 420, s, cara="dor", bob=math.sin(t * 10) * 11)
        suor(p, 700, CY - 40, 420, s, k=abs(math.sin(t * 6)))
        T(p, "DOR", 1420, CY - 40, 190, VERMELHO, pop(t, 0.3), esp=10)
        return
    if i == 32:
        if t > 0.10: O.gota(p, 420, CY - 40, 240 * pop(t, 0.10, .2), s)
        if t > 0.45: p.oval(760, CY - 40, 110 * pop(t, 0.45, .2), 80 * pop(t, 0.45, .2), ROSA, PRETO, 12, s + 2)
        if t > 0.80: O.coracao(p, 1120, CY - 40, 300 * pop(t, 0.80, .2), s + 3)
        if t > 1.15:
            e = pop(t, 1.15, .2)
            p.traco([(1420, CY + 80), (1560, CY - 60), (1700, CY - 150)], VERMELHO, int(18 * e), s + 5, 3.0)
            T(p, "PRESSÃO", 1560, CY + 180, 60, PRETO, e, fonte="hand")
        return
    if i == 33:
        p.bola(W / 2, CY, 26, VERMELHO, PRETO, 8, s)
        T(p, "só isso", W / 2, CY + 200, 90, PRETO, pop(t, 0.4), fonte="hand")
        return
    if i == 34:
        T(p, "µg", W / 2, CY, 320, VERMELHO, pop(t, 0.0), esp=12)
        return
    if i == 35:
        e = pop(t, 0.0)
        p.caixa(620 - 180 * e, CY - 180 * e, 620 + 180 * e, CY + 180 * e, BRANCO, PRETO, 16, s)
        T(p, "1 GRÃO DE SAL", 620, CY + 300, 70, PRETO, min(1.0, t / .3))
        T(p, "60 µg", 1400, CY, 180, VERMELHO, pop(t, 0.5), esp=10)
        return
    if i == 36:
        aranha(p, 700, CY + 40, 440, s, armada=True, fill=MARROM)
        T(p, "Nº 1", 1420, CY - 60, 230, VERMELHO, pop(t, 0.3), esp=11)
        T(p, "do mundo", 1420, CY + 180, 80, PRETO, pop(t, 0.8), fonte="hand")
        return

    # ============================================ 5 OS ACIDENTES
    if i == 37:
        T(p, "POTENTE", 540, CY - 60, 120, VERMELHO, pop(t, 0.0))
        T(p, "≠", W / 2, CY - 60, 170, PRETO, pop(t, 0.45))
        T(p, "MORTAL", 1380, CY - 60, 120, PRETO, pop(t, 0.75))
        return
    if i == 38:
        T(p, "4 000", W / 2, CY - 60, 300, VERMELHO, pop(t, 0.0), esp=12)
        T(p, "acidentes por ano", W / 2, CY + 200, 86, PRETO, pop(t, 0.6), fonte="hand")
        return
    if i == 39:
        O.barras(p, W / 2, CY, 760, s, [10, 2, 0.4], [VERDE, AMARELO, VERMELHO])
        T(p, "leve", 720, CY + 330, 64, PRETO, pop(t, 0.3), fonte="hand")
        T(p, "moder.", 960, CY + 330, 64, PRETO, pop(t, 0.5), fonte="hand")
        T(p, "grave", 1200, CY + 330, 64, PRETO, pop(t, 0.7), fonte="hand")
        return
    if i == 40:
        menino(p, W / 2, CY + 150, 430, s, cara="dor", bob=math.sin(t * 9) * 10)
        suor(p, W / 2, CY, 430, s, k=abs(math.sin(t * 5)))
        return
    if i == 41:
        menino(p, 620, CY + 140, 300, s, cara="medo", bob=math.sin(t * 7) * 6)
        menino(p, 1300, CY + 140, 380, s + 9, cara="dor", bob=math.sin(t * 5) * 6)
        T(p, "crianças", 620, CY - 200, 70, VERMELHO, pop(t, 0.4), fonte="hand")
        T(p, "idosos", 1300, CY - 200, 70, VERMELHO, pop(t, 0.7), fonte="hand")
        return
    if i == 42:
        T(p, "RARÍSSIMA", W / 2, CY, 170, VERDE, pop(t, 0.0), esp=9)
        return
    if i == 43:
        O.calendario(p, W / 2, CY, 620, s)
        return
    if i == 44:
        O.calendario(p, 700, CY, 620, s, marca=(1, 1) if t > 0.5 else None)
        T(p, "ABRIL", 1400, CY - 120, 120, VERMELHO, pop(t, 0.5))
        T(p, "MAIO", 1400, CY + 60, 120, VERMELHO, pop(t, 0.9))
        return
    if i == 45:
        x = 380 + (t / max(d, .01)) * 560
        aranha(p, x, CY + 40, 300, s, fill=MARROM)
        aranha(p, 1480, CY + 40, 340, s + 7, fill=(150, 90, 60))
        T(p, "macho", 480, CY - 230, 66, PRETO, pop(t, 0.2), fonte="hand")
        T(p, "fêmea", 1480, CY - 230, 66, PRETO, pop(t, 0.2), fonte="hand")
        return
    if i == 46:
        e = pop(t, 0.0)
        p.forma([(560, CY + 20), (860, CY - 220), (1160, CY + 20)], VERMELHO, PRETO, 16, s)
        p.caixa(620, CY + 20, 1100, CY + 360, AMARELO, PRETO, 16, s + 1)
        p.caixa(800, CY + 180, 920, CY + 360, MARROM, PRETO, 13, s + 2)
        if t > 0.7:
            aranha(p, 1030, CY + 280, 150 * pop(t, 0.7, .2), s + 5, fill=MARROM)
        return

    # ============================================ 6 QUEM MAIS PICA
    if i == 47:
        menino(p, W / 2, CY + 120, 460, s, cara="choque", bob=math.sin(t * 10) * 12, bracos=0.6)
        balao_susto(p, W / 2 + 30, CY - 230, 460, s, "?!")
        return
    if i == 48:
        O.cama(p, 760, CY + 60, 640, s)
        aranha(p, 1440, CY, 260, s + 4, fill=MARROM)
        if t > 0.8:
            p.xis(1440, CY, 150 * pop(t, 0.8, .2), VERMELHO, 24, s + 9)
        return
    if i == 49:
        O.escorpiao(p, 760, CY + 20, 620, s)
        T(p, "Nº 1", 1480, CY - 80, 210, VERMELHO, pop(t, 0.4), esp=11)
        return
    if i == 50:
        O.escorpiao(p, 420, CY, 340, s)
        if t > 0.5:
            e = pop(t, 0.5, .2)
            p.traco([(820, CY + 60), (1000, CY - 40), (1180, CY + 60)], VERDE, int(26 * e), s + 4, 4.0)
            p.bola(1180, CY + 60, 34 * e, VERDE, PRETO, 9, s + 5)
        if t > 0.95:
            aranha(p, 1560, CY, 260 * pop(t, 0.95, .2), s + 8, fill=MARROM)
        return
    if i == 51:
        O.barras(p, W / 2, CY, 820, s, [10, 3, 1.2], [(60, 60, 60), VERDE, VERMELHO])
        T(p, "escorpião", 700, CY + 330, 58, PRETO, pop(t, 0.2), fonte="hand")
        T(p, "cobra", 960, CY + 330, 58, PRETO, pop(t, 0.4), fonte="hand")
        T(p, "aranha", 1220, CY + 330, 58, VERMELHO, pop(t, 0.6), fonte="hand")
        return
    if i == 52:
        T(p, "REPUTAÇÃO", W / 2, CY, 185, VERMELHO, pop(t, 0.0), esp=10)
        return

    # ============================================ 7 NAO CONFUNDA
    if i == 53:
        for k in range(3):
            x = 480 + k * 480
            aranha(p, x, CY, 280, s + k * 11, fill=MARROM)
            if t > 0.3 + k * 0.2:
                T(p, "?", x, CY - 260, 130, VERMELHO, pop(t, 0.3 + k * 0.2, .15))
        return
    if i == 54:
        foto("L_loxosceles")
        return
    if i == 55:
        aranha(p, 620, CY, 200, s, fill=(160, 110, 80))
        aranha(p, 1300, CY, 430, s + 6, fill=MARROM)
        T(p, "pequena", 620, CY + 230, 62, PRETO, pop(t, 0.3), fonte="hand")
        return
    if i == 56:
        p.forma([(640, CY - 150), (1280, CY - 120), (1280, CY + 170), (640, CY + 140)], PELE, PRETO, 15, s)
        if t > 0.5:
            e = pop(t, 0.5, .3)
            p.bola(960, CY + 10, 92 * e, VERMELHO, PRETO, 12, s + 3)
            p.bola(960, CY + 10, 46 * e, (90, 20, 20), PRETO, 9, s + 4)
        return
    if i == 57:
        foto("L_caranguejeira")
        return
    if i == 58:
        O.barras(p, W / 2, CY, 620, s, [1.2, 9], [CINZA, VERMELHO])
        T(p, "caranguej.", 800, CY + 330, 58, PRETO, pop(t, 0.3), fonte="hand")
        T(p, "armadeira", 1100, CY + 330, 58, VERMELHO, pop(t, 0.5), fonte="hand")
        return
    if i == 59:
        T(p, "SUSTO", 560, CY - 40, 180, PRETO, pop(t, 0.0), esp=9)
        T(p, "RISCO", 1380, CY - 40, 80, VERDE, pop(t, 0.5), esp=6)
        return

    # ============================================ 8 COMO RECONHECER
    if i == 60:
        aranha(p, 760, CY + 30, 400, s, fill=MARROM)
        O.lupa(p, 1300, CY - 30, 480, s + 5)
        return
    if i == 61:
        T(p, "3", W / 2, CY, 340, VERMELHO, pop(t, 0.0), esp=12)
        T(p, "coisas", W / 2, CY + 250, 90, PRETO, pop(t, 0.4), fonte="hand")
        return
    if i == 62:
        aranha(p, 760, CY - 30, 460, s, fill=MARROM)
        O.regua(p, 760, CY + 300, 660, s + 3)
        T(p, "10 cm +", 1440, CY - 40, 140, VERMELHO, pop(t, 0.4))
        return
    if i == 63:
        aranha(p, 760, CY + 20, 480, s, fill=MARROM)
        for k in range(5):
            if t > 0.3 + k * 0.1:
                e = pop(t, 0.3 + k * 0.1, .12)
                p.traco([(1140 + k * 120, CY - 80), (1140 + k * 120, CY + 80 * e)],
                        AMARELO if k % 2 else (90, 60, 40), int(34 * e), s + 20 + k, 2.0)
        T(p, "MANCHAS", 1420, CY - 220, 100, VERMELHO, pop(t, 0.8))
        return
    if i == 64:
        T(p, "A POSTURA", W / 2, CY, 195, VERMELHO, pop(t, 0.0), esp=10)
        return
    if i == 65:
        aranha(p, W / 2, CY + 60, 560, s, armada=True, fill=MARROM)
        return
    if i == 66:
        aranha(p, 560, CY - 30, 340, s, armada=True, fill=MARROM)
        for k in range(3):
            x = 1080 + k * 270
            aranha(p, x, CY + 30, 200, s + k * 9, fill=CINZA)
            if t > 0.3 + k * 0.15:
                p.xis(x, CY + 30, 120 * pop(t, 0.3 + k * 0.15, .15), VERMELHO, 20, s + k)
        return
    if i == 67:
        p.bola(860, CY, 300, MARROM, PRETO, 17, s)
        for lado in (-1, 1):
            p.bola(860 + lado * 110, CY - 70, 56, BRANCO, PRETO, 10, s + 2 + lado)
            p.d.ellipse([860 + lado * 110 - 22, CY - 92, 860 + lado * 110 + 22, CY - 48], fill=PRETO)
        if t > 0.4:
            e = pop(t, 0.4, .2)
            for lado in (-1, 1):
                p.traco([(860 + lado * 90, CY + 150), (860 + lado * 140, CY + 150 + 190 * e)],
                        VERMELHO, 30, s + 8 + lado, 3.0)
        T(p, "PRESAS", 1480, CY + 100, 120, VERMELHO, pop(t, 0.8))
        return
    if i == 68:
        O.mao(p, 760, CY, 460, s)
        if t > 0.4:
            p.xis(760, CY, 260 * pop(t, 0.4, .2), VERMELHO, 32, s + 5)
        return
    if i == 69:
        O.celular(p, 700, CY, 620, s)
        aranha(p, 1340, CY + 40, 300, s + 6, fill=MARROM)
        if t > 0.6:
            e = pop(t, 0.6, .2)
            p.traco([(880, CY - 60), (1160, CY - 20)], VERDE, int(16 * e), s + 9, 3.0)
        return

    # ============================================ 9 COMO EVITAR
    if i == 70:
        aranha(p, 700, CY + 20, 400, s, fill=MARROM)
        O.certo(p, 1340, CY, 300 * pop(t, 0.4), s + 5)
        return
    if i == 71:
        ang = math.sin(t * 13) * 0.10
        O.botaL(p, 760 + math.sin(t * 13) * 40, CY, 560, s)
        if t > 0.5:
            aranha(p, 1180, CY + 260 + math.sin(t * 9) * 30, 170, s + 4, fill=MARROM)
        O.certo(p, 1520, CY - 100, 260 * pop(t, 0.9), s + 8)
        return
    if i == 72:
        O.pilha_roupa(p, 760, CY + 40, 560, s)
        if t > 0.5:
            p.xis(760, CY, 250 * pop(t, 0.5, .2), VERMELHO, 30, s + 6)
        return
    if i == 73:
        O.cama(p, 820, CY + 40, 700, s)
        p.traco([(320, CY - 340), (320, CY + 380)], PRETO, 18, s + 9, 3.0)
        if t > 0.6:
            e = pop(t, 0.6, .25)
            p.traco([(470, CY - 60), (620, CY - 60)], VERDE, int(20 * e), s + 11, 3.0)
            p.traco([(620, CY - 60), (570, CY - 110)], VERDE, int(20 * e), s + 12, 2.0)
            p.traco([(620, CY - 60), (570, CY - 10)], VERDE, int(20 * e), s + 13, 2.0)
        return
    if i == 74:
        p.caixa(560, CY - 260, 1180, CY + 220, (225, 235, 245), PRETO, 16, s)
        for k in range(6):
            p.traco([(560 + k * 124, CY - 260), (560 + k * 124, CY + 220)], CINZA, 7, s + 2 + k, 1.6)
        for k in range(4):
            p.traco([(560, CY - 260 + k * 120), (1180, CY - 260 + k * 120)], CINZA, 7, s + 9 + k, 1.6)
        O.certo(p, 1480, CY - 20, 300 * pop(t, 0.5), s + 20)
        return
    if i == 75:
        for k in range(5):
            x = 520 + (k % 3) * 230
            y = CY - 40 + (k // 3) * 190
            p.forma([(x - 90, y + 60), (x + 90, y + 60), (x + 70, y - 50), (x - 70, y - 50)],
                    (170, 120, 90) if k % 2 else CINZA, PRETO, 12, s + k)
        if t > 0.7:
            p.xis(760, CY + 20, 300 * pop(t, 0.7, .2), VERMELHO, 32, s + 15)
        return
    if i == 76:
        p.caixa(1080, CY - 260, 1680, CY + 260, (40, 40, 40), PRETO, 16, s)
        O.mao(p, 900, CY, 420, s + 3)
        if t > 0.5:
            p.xis(1100, CY, 220 * pop(t, 0.5, .2), VERMELHO, 30, s + 8)
        return
    if i == 77:
        O.mao(p, 640, CY - 40, 400, s)
        aranha(p, 1180, CY + 60, 340, s + 6, fill=MARROM)
        if t > 0.5:
            balao_susto(p, 1180, CY - 200, 340, s, "!")
        return

    # ============================================ 10 O QUE FAZER
    if i == 78:
        p.traco([(W / 2, 140), (W / 2, 820)], PRETO, 14, s, 4.0)
        O.certo(p, 560, CY, 340 * pop(t, 0.1), s + 2)
        O.errado(p, 1360, CY, 340 * pop(t, 0.5), s + 3)
        return
    if i == 79:
        lista(p, ["lavar o local", "manter elevado", "ir ao hospital"], 620, CY - 110, t, 0.1, 0.42, 66, "certo", s)
        return
    if i == 80:
        O.gota(p, 700, CY, 300, s, cor=(255, 170, 120))
        O.certo(p, 1240, CY, 320 * pop(t, 0.4), s + 4)
        return
    if i == 81:
        T(p, "TORNIQUETE", W / 2, CY - 60, 165, VERMELHO, pop(t, 0.0), esp=9)
        if t > 0.6:
            O.errado(p, W / 2, CY + 210, 300 * pop(t, 0.6), s + 5)
        return
    if i == 82:
        p.forma([(520, CY - 90), (1400, CY - 60), (1400, CY + 130), (520, CY + 100)], PELE, PRETO, 15, s)
        p.forma([(920, CY - 130), (1010, CY - 125), (1010, CY + 170), (920, CY + 165)], (60, 60, 60), PRETO, 13, s + 2)
        O.errado(p, 965, CY - 250, 260 * pop(t, 0.4), s + 6)
        return
    if i == 83:
        lista(p, ["cortar", "furar", "chupar o local"], 680, CY - 110, t, 0.1, 0.40, 66, "errado", s)
        return
    if i == 84:
        p.forma([(620, CY - 110), (1300, CY - 80), (1300, CY + 160), (620, CY + 130)], PELE, PRETO, 15, s)
        for k in range(5):
            if t > 0.2 + k * 0.12:
                e = pop(t, 0.2 + k * 0.12, .15)
                p.bola(800 + k * 120, CY + 20, 34 * e, VERDE, PRETO, 8, s + 4 + k)
        T(p, "INFECÇÃO", 1560, CY - 160, 100, VERMELHO, pop(t, 0.8))
        return
    if i == 85:
        aranha(p, 700, CY, 360, s, fill=MARROM)
        p.caixa(1180, CY - 180, 1560, CY + 180, BRANCO, PRETO, 15, s + 4)
        if t > 0.5:
            p.xis(1370, CY, 200 * pop(t, 0.5, .2), VERMELHO, 26, s + 9)
        return
    if i == 86:
        O.celular(p, 780, CY, 640, s)
        aranha(p, 1380, CY + 40, 280, s + 6, fill=MARROM)
        O.certo(p, 1380, CY - 250, 220 * pop(t, 0.6), s + 12)
        return

    # ============================================ 11 NO HOSPITAL
    if i == 87:
        T(p, "3", W / 2, CY - 60, 320, ac, pop(t, 0.0), esp=12)
        T(p, "níveis", W / 2, CY + 200, 90, PRETO, pop(t, 0.4), fonte="hand")
        return
    if i == 88:
        p.bola(620, CY, 190, VERDE, PRETO, 16, s)
        T(p, "LEVE", 620, CY, 90, BRANCO, 1.0, esp=6)
        menino(p, 1280, CY + 140, 380, s + 3, cara="dor", bob=math.sin(t * 7) * 7)
        return
    if i == 89:
        lista(p, ["analgésico", "às vezes anestesia", "observação"], 640, CY - 110, t, 0.1, 0.42, 66, "certo", s)
        return
    if i == 90:
        p.bola(620, CY, 190, AMARELO, PRETO, 16, s)
        T(p, "MODER.", 620, CY, 66, PRETO, 1.0, esp=5)
        menino(p, 1280, CY + 140, 380, s + 3, cara="medo", bob=math.sin(t * 9) * 9)
        suor(p, 1280, CY - 10, 380, s, k=abs(math.sin(t * 6)))
        return
    if i == 91:
        lista(p, ["suor no corpo todo", "agitação", "pressão alterada", "vômito"], 620, CY - 190, t, 0.1, 0.34, 62, None, s)
        return
    if i == 92:
        p.bola(620, CY, 190, VERMELHO, PRETO, 16, s)
        T(p, "GRAVE", 620, CY, 76, BRANCO, 1.0, esp=6)
        O.cama(p, 1320, CY + 60, 560, s + 5)
        return
    if i == 93:
        if t > 0.10: O.coracao(p, 520, CY - 40, 260 * pop(t, 0.10, .2), s)
        if t > 0.45: O.pulmao(p, 900, CY - 40, 340 * pop(t, 0.45, .2), s + 2)
        if t > 0.80: O.gota(p, 1260, CY - 40, 220 * pop(t, 0.80, .2), s + 4)
        if t > 1.15: T(p, "GRAVE", 1620, CY - 40, 110, VERMELHO, pop(t, 1.15, .2))
        return
    if i == 94:
        O.frascoL(p, 760, CY, 520, s, cor=ac)
        if t > 0.7:
            p.xis(760, CY, 250 * pop(t, 0.7, .2), VERMELHO, 30, s + 8)
        T(p, "NEM SEMPRE", 1400, CY - 60, 110, VERMELHO, pop(t, 1.0))
        return
    if i == 95:
        p.bola(560, CY, 150, VERDE, PRETO, 14, s)
        p.bola(900, CY, 150, AMARELO, PRETO, 14, s + 1)
        p.bola(1240, CY, 150, VERMELHO, PRETO, 14, s + 2)
        if t > 0.5:
            e = pop(t, 0.5, .25)
            O.frascoL(p, 1600, CY, 340 * e, s + 6, cor=ac)
            p.traco([(1060, CY - 230), (1420, CY - 230)], ac, int(16 * e), s + 9, 3.0)
        return
    if i == 96:
        menino(p, 780, CY + 120, 420, s, cara="ok", bob=math.sin(t * 5) * 5)
        p.forma([(700, CY - 150), (860, CY - 150), (860, CY - 60), (700, CY - 60)], BRANCO, PRETO, 12, s + 20)
        menino(p, 1360, CY + 140, 380, s + 7, cara="dor", bob=math.sin(t * 8) * 8)
        T(p, "médico", 780, CY - 300, 70, ac, pop(t, 0.3), fonte="hand")
        return

    # ============================================ 12 O SORO
    if i == 97:
        O.frascoL(p, W / 2, CY, 560, s, cor=ac)
        return
    if i == 98:
        T(p, "SORO", W / 2, CY - 60, 250, ac, pop(t, 0.0), esp=11)
        T(p, "antiaracnídico", W / 2, CY + 190, 80, PRETO, pop(t, 0.5), fonte="hand")
        return
    if i == 99:
        aranha(p, 460, CY, 280, s, fill=MARROM)
        O.cavalo(p, 1180, CY, 480, s + 5)
        if t > 0.5:
            e = pop(t, 0.5, .25)
            p.traco([(660, CY - 40), (880, CY - 40)], PRETO, int(16 * e), s + 9, 3.0)
            T(p, "?!", 770, CY - 190, 120, VERMELHO, e)
        return
    if i == 100:
        aranha(p, 680, CY + 20, 440, s, armada=True, fill=MARROM)
        if t > 0.4:
            e = pop(t, 0.4, .25)
            O.gota(p, 1120, CY + 60, 200 * e, s + 6, cor=AMARELO)
            O.frascoL(p, 1480, CY, 300 * e, s + 8, cor=AMARELO)
        return
    if i == 101:
        O.cavalo(p, 1120, CY + 20, 620, s)
        if t > 0.35:
            e = pop(t, 0.35, .25)
            O.seringa(p, 620, CY - 60, 420 * e, s + 9, cor=AMARELO)
        return
    if i == 102:
        O.cavalo(p, 700, CY + 20, 560, s)
        for k in range(4):
            if t > 0.4 + k * 0.16:
                O.anticorpo(p, 1300 + (k % 2) * 220, CY - 100 + (k // 2) * 220,
                            180 * pop(t, 0.4 + k * 0.16, .18), s + 12 + k, cor=ac)
        return
    if i == 103:
        O.cavalo(p, 640, CY + 20, 520, s)
        if t > 0.4:
            e = pop(t, 0.4, .25)
            p.traco([(980, CY - 20), (1240, CY - 20)], VERMELHO, int(18 * e), s + 9, 3.0)
            O.frascoL(p, 1460, CY, 340 * e, s + 11, cor=VERMELHO)
        return
    if i == 104:
        O.frascoL(p, W / 2, CY, 560, s, cor=ac)
        T(p, "SORO", W / 2, CY + 30, 90, BRANCO, pop(t, 0.3), esp=6)
        return
    if i == 105:
        foto("n_butantan")
        return
    if i == 106:
        T(p, "1901", W / 2, CY - 40, 300, ac, pop(t, 0.0), esp=12)
        return
    if i == 107:
        p.forma([(420, CY + 120), (1180, CY + 120), (1080, CY + 260), (520, CY + 260)], (60, 60, 120), PRETO, 16, s)
        for k in range(3):
            p.caixa(560 + k * 180, CY - 20, 700 + k * 180, CY + 120,
                    [VERMELHO, AMARELO, VERDE][k], PRETO, 13, s + 2 + k)
        if t > 0.6:
            e = pop(t, 0.6, .25)
            p.oval(1440, CY + 60, 130 * e, 70 * e, (90, 70, 60), PRETO, 12, s + 9)
            p.traco([(1560, CY + 60), (1680, CY + 100)], PRETO, 10, s + 10, 2.4)
            T(p, "PESTE", 1440, CY - 160, 100, VERMELHO, pop(t, 0.9))
        return
    if i == 108:
        O.predio(p, 760, CY, 620, s)
        if t > 0.5:
            e = pop(t, 0.5, .25)
            p.bola(1480, CY, 210 * e, (120, 190, 240), PRETO, 14, s + 8)
            p.traco([(1330, CY), (1630, CY)], PRETO, 8, s + 9, 2.0)
            p.traco([(1480, CY - 200), (1480, CY + 200)], PRETO, 8, s + 10, 2.0)
        return
    if i == 109:
        T(p, "DE GRAÇA", W / 2, CY - 40, 220, VERDE, pop(t, 0.0), esp=11)
        T(p, "pelo SUS", W / 2, CY + 190, 90, PRETO, pop(t, 0.5), fonte="hand")
        return

    # ============================================ 13 VIRA REMEDIO
    if i == 110:
        menino(p, W / 2, CY + 120, 440, s, cara="confuso", bob=math.sin(t * 6) * 8, bracos=0.35)
        return
    if i == 111:
        T(p, "?", W / 2, CY, 340, ac, pop(t, 0.0), esp=12)
        return
    if i == 112:
        ab = min(1.0, t / max(d * 0.7, .01))
        O.vaso(p, W / 2, CY, 900, s, aberto=ab)
        T(p, "ABRE", 1560, CY - 220, 120, ac, pop(t, 0.6))
        return
    if i == 113:
        for k in range(3):
            if t > 0.15 + k * 0.30:
                e = pop(t, 0.15 + k * 0.30, .2)
                x = 620 + k * 340
                p.bola(x, CY, 90 * e, ac, PRETO, 13, s + k)
                if k < 2:
                    p.traco([(x + 90, CY), (x + 250, CY)], PRETO, 9, s + 10 + k, 2.0)
        T(p, "óxido nítrico", W / 2, CY + 250, 84, PRETO, pop(t, 1.05), fonte="hand")
        return
    if i == 114:
        T(p, "PnTx2-6", W / 2, CY, 210, ac, pop(t, 0.0), esp=10)
        return
    if i == 115:
        e = pop(t, 0.0)
        p.forma(_br(780, CY, 380 * e, 470 * e), VERDE, PRETO, 15, s)
        if t > 0.5:
            p.bola(880, CY + 40, 44 * pop(t, 0.5, .2), VERMELHO, PRETO, 10, s + 4)
        O.lupa(p, 1380, CY - 20, 440, s + 8)
        T(p, "MINAS", 880, CY + 190, 70, PRETO, pop(t, 0.8))
        return
    if i == 116:
        O.frascoL(p, 560, CY, 400, s, cor=AMARELO)
        if t > 0.4:
            e = pop(t, 0.4, .25)
            p.traco([(820, CY - 20), (1120, CY - 20)], ac, int(20 * e), s + 6, 3.0)
            p.traco([(1120, CY - 20), (1050, CY - 90)], ac, int(20 * e), s + 7, 2.0)
            p.traco([(1120, CY - 20), (1050, CY + 50)], ac, int(20 * e), s + 8, 2.0)
        if t > 0.8:
            O.frascoL(p, 1440, CY, 440 * pop(t, 0.8, .25), s + 10, cor=ac)
        return
    if i == 117:
        O.frascoL(p, 760, CY, 480, s, cor=ac)
        O.lupa(p, 1320, CY - 20, 420, s + 6)
        T(p, "ainda em pesquisa", W / 2, CY + 330, 76, PRETO, pop(t, 0.5), fonte="hand")
        return
    if i == 118:
        aranha(p, 520, CY, 340, s, armada=True, fill=MARROM)
        if t > 0.4:
            e = pop(t, 0.4, .25)
            p.traco([(780, CY - 20), (1120, CY - 20)], ac, int(22 * e), s + 6, 3.0)
            p.traco([(1120, CY - 20), (1040, CY - 100)], ac, int(22 * e), s + 7, 2.0)
            p.traco([(1120, CY - 20), (1040, CY + 60)], ac, int(22 * e), s + 8, 2.0)
        if t > 0.8:
            O.frascoL(p, 1440, CY, 460 * pop(t, 0.8, .25), s + 11, cor=ac)
        return
    if i == 119:
        for k in range(4):
            if t > 0.1 + k * 0.22:
                O.arvore(p, 480 + k * 340, CY + 40, 420 * pop(t, 0.1 + k * 0.22, .2), s + k * 7)
        return
    if i == 120:
        O.arvore(p, 520, CY + 40, 400, s)
        if t > 0.4:
            p.xis(520, CY + 40, 220 * pop(t, 0.4, .2), VERMELHO, 28, s + 5)
        if t > 0.8:
            e = pop(t, 0.8, .25)
            O.frascoL(p, 1200, CY, 380 * e, s + 9, cor=CINZA)
            p.xis(1200, CY, 200 * e, VERMELHO, 26, s + 12)
        return

    # ============================================ 14 FECHO
    if i == 121:
        aranha(p, W / 2, CY + 40, 460, s, fill=MARROM)
        return
    if i == 122:
        O.botaL(p, 1280, CY + 40, 560, s)
        aranha(p, 660, CY + 40, 360, s + 5, fill=MARROM)
        p.bola(1620, 200, 90, AMARELO, PRETO, 12, s + 20)
        return
    if i == 123:
        O.arvore(p, 440, CY + 20, 380, s)
        if t > 0.5:
            e = pop(t, 0.5, .25)
            p.oval(960, CY + 20, 150 * e, 90 * e, AMARELO, PRETO, 14, s + 6)
        if t > 1.0:
            O.frascoL(p, 1480, CY, 420 * pop(t, 1.0, .25), s + 10, cor=VERDE)
        return
    if i == 124:
        aranha(p, 640, CY, 400, s, cor_perna=VERDE, fill=VERDE)
        if t > 0.6:
            O.frascoL(p, 1300, CY, 520 * pop(t, 0.6, .3), s + 8, cor=VERDE)
        return


def _br(cx, cy, w, h):
    n = [(0.10, 0.24), (0.00, 0.32), (0.20, 0.38), (0.35, 0.47), (0.41, 0.59), (0.40, 0.69),
         (0.51, 0.82), (0.41, 0.90), (0.52, 0.99), (0.64, 0.86), (0.73, 0.74), (0.88, 0.46),
         (0.97, 0.28), (0.74, 0.19), (0.60, 0.08), (0.35, 0.00), (0.15, 0.08), (0.12, 0.16)]
    return [(cx - w / 2 + x * w, cy - h / 2 + y * h) for x, y in n]


SETAS = {
 7:  [("nigriventer", 960, 500, 500, 230, 0.5, BRANCO, 64)],
 12: [("BOLSA DE OVOS", 980, 520, 560, 760, 0.5, BRANCO, 58)],
 19: [("ESCURO", 760, 520, 1280, 250, 0.7, VERMELHO, 60)],
 21: [("O SAPATO", 860, 500, 1400, 230, 0.6, VERMELHO, 62)],
 27: [("SÓDIO", 840, 490, 640, 200, 0.4, PRETO, 58)],
 29: [("TRAVOU", 1090, 490, 1450, 780, 1.0, VERMELHO, 62)],
 35: [("60 µg", 620, 400, 300, 200, 0.9, PRETO, 58)],
 43: [("OUTONO", 960, 440, 1460, 220, 0.5, VERMELHO, 62)],
 49: [("ESCORPIÃO", 760, 480, 420, 200, 0.6, PRETO, 58)],
 54: [("ARANHA-MARROM", 960, 500, 520, 750, 0.5, BRANCO, 58)],
 57: [("CARANGUEJEIRA", 960, 500, 560, 750, 0.5, BRANCO, 58)],
 65: [("ESSA POSTURA", 960, 330, 1480, 200, 0.5, VERMELHO, 56)],
 71: [("SACUDA", 760, 380, 340, 200, 0.5, VERDE, 60)],
 101:[("VENENO", 620, 420, 380, 210, 0.7, AMARELO, 58)],
 102:[("ANTICORPOS", 1410, 360, 1560, 160, 1.1, VERDE, 52)],
 105:[("BUTANTAN", 960, 480, 520, 750, 0.5, BRANCO, 64)],
 112:[("VASO", 700, 470, 420, 200, 0.7, PRETO, 58)],
}
