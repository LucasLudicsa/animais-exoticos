# -*- coding: utf-8 -*-
"""Gera a foto de perfil e o banner do canal, no mesmo tracado dos videos.

Conceito: mata densa e o lugar onde alguma coisa esta te olhando e voce nao
ve o que e. Entao a marca e um par de olhos saindo do escuro da folhagem.
Funciona porque sobrevive ao tamanho: no YouTube a foto aparece a 98 px, onde
qualquer desenho detalhado vira borrao. Dois olhos claros sobre fundo escuro
continuam legiveis em qualquer tamanho.

    python3 pipeline/marca.py
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fonts")
SAIDA = os.path.join(os.path.dirname(AQUI), "marca")

FUNDO = (11, 20, 14)
FOLHA = [(18, 38, 24), (24, 50, 30), (14, 30, 19), (30, 60, 36)]
OLHO = (243, 236, 205)
PUPILA = (10, 14, 10)
DESTAQUE = (214, 176, 58)


def fonte(nome, tam):
    return ImageFont.truetype(os.path.join(FONTES, nome), tam)


def tremido(d, pts, cor, larg, r, amp=2.0, fechar=True):
    """Linha com tremor, para nao parecer vetor perfeito."""
    saida = []
    for x, y in pts:
        saida.append((x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)))
    if fechar:
        saida.append(saida[0])
    d.line(saida, fill=cor, width=larg, joint="curve")


def folha(d, cx, cy, comp, ang, cor, r):
    """Folha simples: dois arcos que se encontram nas pontas."""
    pts_a, pts_b = [], []
    for i in range(13):
        t = i / 12
        x = cx + math.cos(ang) * comp * t
        y = cy + math.sin(ang) * comp * t
        larg = math.sin(math.pi * t) * comp * 0.26
        nx, ny = -math.sin(ang), math.cos(ang)
        pts_a.append((x + nx * larg + r.uniform(-2, 2), y + ny * larg + r.uniform(-2, 2)))
        pts_b.append((x - nx * larg + r.uniform(-2, 2), y - ny * larg + r.uniform(-2, 2)))
    d.polygon(pts_a + pts_b[::-1], fill=cor)


def folhagem(d, larg, alt, r, n=42, escala=1.0):
    for _ in range(n):
        x = r.uniform(-larg * 0.05, larg * 1.05)
        y = r.uniform(-alt * 0.05, alt * 1.05)
        folha(d, x, y, r.uniform(alt * 0.18, alt * 0.42) * escala,
              r.uniform(0, math.tau), r.choice(FOLHA), r)


def olhos(d, cx, cy, lar, r, abertura=0.52):
    """Par de olhos. lar = largura de um olho."""
    sep = lar * 1.55
    for lado in (-1, 1):
        ox = cx + lado * sep / 2
        alt = lar * abertura
        # branco do olho, formato amendoado
        cima = [(ox - lar / 2 + i * lar / 12,
                 cy - math.sin(math.pi * i / 12) * alt / 2 + r.uniform(-1.5, 1.5)) for i in range(13)]
        baixo = [(ox - lar / 2 + i * lar / 12,
                  cy + math.sin(math.pi * i / 12) * alt / 2 * 0.78 + r.uniform(-1.5, 1.5)) for i in range(13)]
        d.polygon(cima + baixo[::-1], fill=OLHO)
        # pupila
        pr = alt * 0.34
        d.ellipse([ox - pr, cy - pr, ox + pr, cy + pr], fill=PUPILA)
        br = pr * 0.30
        d.ellipse([ox - pr * 0.42 - br, cy - pr * 0.45 - br,
                   ox - pr * 0.42 + br, cy - pr * 0.45 + br], fill=OLHO)
        tremido(d, cima + baixo[::-1], (8, 12, 9), max(2, int(lar * 0.05)), r, 1.2)


def perfil(tam=800):
    r = random.Random(7)
    im = Image.new("RGB", (tam, tam), FUNDO)
    d = ImageDraw.Draw(im)
    folhagem(d, tam, tam, r, n=46, escala=0.85)
    # escurece as bordas para o centro saltar
    vin = Image.new("L", (tam, tam), 0)
    ImageDraw.Draw(vin).ellipse([-tam * 0.15, -tam * 0.15, tam * 1.15, tam * 1.15], fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(tam * 0.13))
    im = Image.composite(im, Image.new("RGB", (tam, tam), (5, 9, 6)), vin)
    d = ImageDraw.Draw(im)
    olhos(d, tam / 2, tam * 0.52, tam * 0.27, r)
    os.makedirs(SAIDA, exist_ok=True)
    p = os.path.join(SAIDA, "perfil.png")
    im.save(p)
    # prova de legibilidade no tamanho real do YouTube
    im.resize((98, 98), Image.LANCZOS).save(os.path.join(SAIDA, "perfil_98px.png"))
    return p


def banner(larg=2048, alt=1152):
    r = random.Random(11)
    im = Image.new("RGB", (larg, alt), FUNDO)
    d = ImageDraw.Draw(im)
    folhagem(d, larg, alt, r, n=70, escala=0.55)

    # area segura central: 1235 x 338, o unico pedaco visivel no celular
    sx, sy = (larg - 1235) / 2, (alt - 338) / 2
    escuro = Image.new("RGB", (larg, alt), (7, 13, 9))
    mask = Image.new("L", (larg, alt), 0)
    ImageDraw.Draw(mask).rectangle([sx - 120, sy - 70, sx + 1235 + 120, sy + 338 + 70], fill=210)
    im = Image.composite(escuro, im, mask.filter(ImageFilter.GaussianBlur(70)))
    d = ImageDraw.Draw(im)

    # O titulo manda: mede primeiro, depois encaixa os olhos NA SOBRA.
    # Posicao fixa colidia com as letras quando o texto era largo.
    t1, t2 = "MATA DENSA", "a natureza brasileira que te engana"
    tam = 150
    GAP = 54          # respiro minimo entre olho e letra
    OLHO_L = 104      # largura de um olho (o par ocupa ~2.6x isso)
    PAR = OLHO_L * 2.6
    while tam > 70:
        f1 = fonte("Marker.ttf", tam)
        b1 = d.textbbox((0, 0), t1, font=f1)
        tw = b1[2] - b1[0]
        if tw + 2 * (PAR + GAP) <= 1235:
            break
        tam -= 6
    f2 = fonte("Hand.ttf", 50)

    tx = (larg - tw) / 2 - b1[0]
    d.text((tx, sy + 74), t1, font=f1, fill=OLHO)
    b2 = d.textbbox((0, 0), t2, font=f2)
    d.text(((larg - (b2[2] - b2[0])) / 2 - b2[0], sy + 74 + tam + 18), t2, font=f2, fill=DESTAQUE)

    cy_olho = sy + 74 + tam * 0.52
    olhos(d, tx - GAP - PAR / 2, cy_olho, OLHO_L, r, abertura=0.46)
    olhos(d, tx + tw + GAP + PAR / 2, cy_olho, OLHO_L, r, abertura=0.46)

    os.makedirs(SAIDA, exist_ok=True)
    p = os.path.join(SAIDA, "banner.png")
    im.save(p)
    return p


if __name__ == "__main__":
    a, b = perfil(), banner()
    for p in (a, b, os.path.join(SAIDA, "perfil_98px.png")):
        im = Image.open(p)
        print(f"{os.path.basename(p):<18} {im.size[0]}x{im.size[1]}  {os.path.getsize(p)/1024:.0f} KB")
