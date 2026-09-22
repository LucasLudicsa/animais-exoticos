# -*- coding: utf-8 -*-
import os
from paths import PIPE
"""Desenho de Paint: traço grosso tremido, cor chapada, zero antialias."""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1080, 1920

# paleta clássica do Paint
BRANCO   = (255, 255, 255)
PRETO    = (0, 0, 0)
VERMELHO = (237, 28, 36)
AZUL     = (63, 72, 204)
AMARELO  = (255, 242, 0)
VERDE    = (34, 177, 76)
ROSA     = (255, 174, 201)
MARROM   = (185, 122, 87)
CINZA    = (127, 127, 127)
LARANJA  = (255, 127, 39)

FDIR = os.path.join(PIPE, 'fonts')
_fc = {}


def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        nome = "Marker.ttf" if kind == "marker" else "Hand.ttf"
        _fc[k] = ImageFont.truetype(f"{FDIR}/{nome}", size)
    return _fc[k]


# ------------------------------------------------------------ tremidinha
def densify(pts, passo=26):
    """Subdivide os segmentos para o tremor virar onda, não bico."""
    out = []
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(d / passo))
        for j in range(n):
            f = j / n
            out.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f))
    out.append(pts[-1])
    return out


def wob(pts, amp, seed):
    """Empurra cada ponto um pouquinho: mão trêmula."""
    r = random.Random(seed)
    return [(x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)) for x, y in pts]


class Paint:
    """Tela onde tudo é desenhado grosso e sem suavização."""

    def __init__(self, w=W, h=H, fundo=None):
        self.im = Image.new("RGBA", (w, h), (fundo + (255,)) if fundo else (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def traco(self, pts, cor=PRETO, esp=13, seed=0, amp=3.4, fechar=False):
        p = list(pts) + ([pts[0]] if fechar else [])
        p = wob(densify(p), amp, seed)
        self.d.line(p, fill=cor, width=esp, joint="curve")
        # bolinha nas pontas para o traço não ficar cortado
        r = esp // 2
        for x, y in (p[0], p[-1]):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=cor)

    def forma(self, pts, fill, cor=PRETO, esp=13, seed=0, amp=3.4):
        p = wob(densify(list(pts) + [pts[0]]), amp, seed)
        if fill:
            self.d.polygon(p, fill=fill)
        self.traco(pts, cor, esp, seed, amp, fechar=True)

    def bola(self, cx, cy, r, fill=None, cor=PRETO, esp=13, seed=0, amp=3.0):
        pts = [(cx + r * math.cos(a * math.pi / 12), cy + r * math.sin(a * math.pi / 12))
               for a in range(24)]
        self.forma(pts, fill, cor, esp, seed, amp)

    def oval(self, cx, cy, rx, ry, fill=None, cor=PRETO, esp=13, seed=0, amp=3.0):
        pts = [(cx + rx * math.cos(a * math.pi / 12), cy + ry * math.sin(a * math.pi / 12))
               for a in range(24)]
        self.forma(pts, fill, cor, esp, seed, amp)

    def caixa(self, x0, y0, x1, y1, fill=None, cor=PRETO, esp=13, seed=0, amp=3.0):
        self.forma([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, cor, esp, seed, amp)

    def xis(self, cx, cy, r, cor=VERMELHO, esp=22, seed=0):
        self.traco([(cx - r, cy - r), (cx + r, cy + r)], cor, esp, seed, 4.0)
        self.traco([(cx - r, cy + r), (cx + r, cy - r)], cor, esp, seed + 1, 4.0)

    def out(self):
        return self.im


# ---------------------------------------------------------------- aranha
def aranha(p, cx, cy, tam, seed, armada=False, cor_perna=PRETO, fill=MARROM):
    """Aranha de criança: duas bolas, oito riscos, dois olhos."""
    e = max(7, int(tam * 0.055))
    rb = tam * 0.30          # bundão
    rc = tam * 0.20          # cabeça

    # pernas de baixo (3 pares), riscos retos com um joelho
    for lado in (-1, 1):
        for k, (ang, comp) in enumerate([(-8, 1.00), (18, 1.05), (44, 0.95)]):
            a = math.radians(ang)
            x1 = cx + lado * tam * 0.22
            y1 = cy - tam * 0.02
            jx = x1 + lado * math.cos(a) * tam * comp * 0.42
            jy = y1 + math.sin(a) * tam * comp * 0.42
            px = jx + lado * math.cos(a - 0.5) * tam * comp * 0.44
            py = jy + math.sin(a - 0.5) * tam * comp * 0.44
            p.traco([(x1, y1), (jx, jy), (px, py)], cor_perna, e, seed + 10 + k + lado * 7, 3.2)

    # par da frente: em pé quando ela se arma
    cor_f = VERMELHO if armada else cor_perna
    for lado in (-1, 1):
        x1 = cx + lado * tam * 0.18
        y1 = cy - tam * 0.16
        if armada:
            jx = x1 + lado * tam * 0.30; jy = y1 - tam * 0.42
            px = jx + lado * tam * 0.12; py = jy - tam * 0.52
        else:
            jx = x1 + lado * tam * 0.44; jy = y1 - tam * 0.10
            px = jx + lado * tam * 0.40; py = jy + tam * 0.06
        p.traco([(x1, y1), (jx, jy), (px, py)], cor_f, int(e * 1.25), seed + 30 + lado * 5, 3.2)

    p.oval(cx, cy + tam * 0.30, rb, rb * 1.05, fill, PRETO, e, seed + 1)
    p.bola(cx, cy - tam * 0.12, rc, fill, PRETO, e, seed + 2)

    # olhos
    for lado in (-1, 1):
        ox = cx + lado * rc * 0.42
        oy = cy - tam * 0.18
        p.bola(ox, oy, rc * 0.30, BRANCO, PRETO, max(5, e // 2), seed + 40 + lado)
        p.d.ellipse([ox - rc * 0.12, oy - rc * 0.12, ox + rc * 0.12, oy + rc * 0.12], fill=PRETO)
    # presas
    for lado in (-1, 1):
        bx = cx + lado * rc * 0.30
        p.traco([(bx, cy + rc * 0.42), (bx + lado * rc * 0.18, cy + rc * 0.80)],
                PRETO, max(5, e // 2), seed + 50 + lado, 2.0)


# --------------------------------------------------------------- texto
def texto(txt, f, cor, contorno=None, esp=0, align="center", max_w=None, spacing=14):
    linhas = txt.split("\n")
    if max_w:
        novo = []
        for ln in linhas:
            cur = ""
            for pal in ln.split():
                t = (cur + " " + pal).strip()
                if f.getbbox(t)[2] - f.getbbox(t)[0] > max_w and cur:
                    novo.append(cur); cur = pal
                else:
                    cur = t
            novo.append(cur)
        linhas = novo
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    ws = [tmp.textbbox((0, 0), l, font=f)[2] - tmp.textbbox((0, 0), l, font=f)[0] for l in linhas]
    asc, desc = f.getmetrics()
    lh = asc + desc
    tw = max(ws) if ws else 1
    th = lh * len(linhas) + spacing * (len(linhas) - 1)
    pad = esp + 8
    im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = pad
    for i, ln in enumerate(linhas):
        x = pad + ((tw - ws[i]) // 2 if align == "center" else 0)
        if contorno and esp:
            for dx in range(-esp, esp + 1, 2):
                for dy in range(-esp, esp + 1, 2):
                    if dx * dx + dy * dy <= esp * esp:
                        d.text((x + dx, y + dy), ln, font=f, fill=contorno)
        d.text((x, y), ln, font=f, fill=cor)
        y += lh + spacing
    return im


def cola(base, im, cx, cy, escala=1.0, anchor="c"):
    if im is None:
        return
    if escala != 1.0:
        im = im.resize((max(1, int(im.width * escala)), max(1, int(im.height * escala))),
                       Image.NEAREST)
    x = int(cx - im.width / 2) if anchor in ("c", "b") else int(cx)
    y = int(cy - im.height / 2) if anchor in ("c", "l") else int(cy)
    base.alpha_composite(im, (x, y))


def pop(t, t0=0.0, dur=0.22):
    """Entrada com estufada: some, estoura, assenta."""
    k = (t - t0) / dur
    if k < 0:
        return 0.0
    if k >= 1:
        return 1.0
    return 1.18 * math.sin(k * math.pi / 2) - 0.18 * math.sin(k * math.pi)


PELE = (255, 219, 172)

def menino(p, cx, cy, tam, seed, cara="ok", bob=0.0, bracos=0.0):
    """Menino de desenho de criança. `bob` sobe/desce, `bracos` levanta os braços."""
    e = max(6, int(tam * 0.055))
    cy = cy + bob
    rc = tam * 0.26                      # cabeça
    hy = cy - tam * 0.42                 # centro da cabeça

    # corpo
    p.forma([(cx - tam*0.24, hy + rc*0.92), (cx + tam*0.24, hy + rc*0.92),
             (cx + tam*0.28, cy + tam*0.34), (cx - tam*0.28, cy + tam*0.34)],
            AZUL, PRETO, e, seed + 1)
    # pernas
    for lado in (-1, 1):
        p.traco([(cx + lado*tam*0.14, cy + tam*0.34), (cx + lado*tam*0.17, cy + tam*0.78)], PRETO, e, seed+2+lado, 2.6)
        p.traco([(cx + lado*tam*0.17, cy + tam*0.78), (cx + lado*tam*0.30, cy + tam*0.80)], PRETO, e, seed+4+lado, 2.2)
    # braços
    for lado in (-1, 1):
        ax = cx + lado*tam*0.25; ay = hy + rc*1.15
        ex = ax + lado*tam*0.30
        ey = ay + tam*0.30 - bracos*tam*0.62
        p.traco([(ax, ay), (ex, ey)], PRETO, e, seed+6+lado, 2.6)
        p.bola(ex, ey, tam*0.055, PELE, PRETO, max(4, e//2), seed+8+lado)
    # cabeça
    p.bola(cx, hy, rc, PELE, PRETO, e, seed + 10)
    for k in range(3):
        x = cx - rc*0.5 + k*rc*0.5
        p.traco([(x, hy - rc*0.92), (x - rc*0.1, hy - rc*1.25)], PRETO, max(5, e-2), seed+12+k, 2.2)

    ox = rc*0.40; oy = hy - rc*0.14
    if cara in ("choque", "medo"):
        for lado in (-1, 1):
            p.bola(cx + lado*ox, oy, rc*0.26, BRANCO, PRETO, max(4, e//2), seed+20+lado)
            p.d.ellipse([cx+lado*ox-rc*0.10, oy-rc*0.10, cx+lado*ox+rc*0.10, oy+rc*0.10], fill=PRETO)
    else:
        for lado in (-1, 1):
            p.d.ellipse([cx+lado*ox-rc*0.11, oy-rc*0.13, cx+lado*ox+rc*0.11, oy+rc*0.13], fill=PRETO)

    my = hy + rc*0.40
    if cara == "choque":
        p.oval(cx, my + rc*0.06, rc*0.22, rc*0.30, PRETO, PRETO, max(4, e//2), seed+30)
    elif cara == "confuso":
        p.traco([(cx-rc*0.30, my), (cx-rc*0.10, my-rc*0.12), (cx+rc*0.10, my+rc*0.10), (cx+rc*0.30, my-rc*0.04)],
                PRETO, max(5, e-3), seed+31, 2.0)
        p.traco([(cx-ox-rc*0.20, oy-rc*0.44), (cx-ox+rc*0.18, oy-rc*0.56)], PRETO, max(5, e-3), seed+32, 2.0)
    elif cara == "dor":
        p.traco([(cx-rc*0.28, my+rc*0.10), (cx+rc*0.28, my+rc*0.10)], PRETO, max(5, e-3), seed+33, 2.0)
        p.traco([(cx-rc*0.28, my+rc*0.10), (cx-rc*0.16, my-rc*0.06)], PRETO, max(5, e-3), seed+34, 2.0)
    elif cara == "feliz":
        p.traco([(cx-rc*0.32, my-rc*0.06), (cx-rc*0.10, my+rc*0.20), (cx+rc*0.10, my+rc*0.20), (cx+rc*0.32, my-rc*0.06)],
                PRETO, max(5, e-3), seed+35, 2.0)
    elif cara == "medo":
        p.traco([(cx-rc*0.28, my+rc*0.16), (cx-rc*0.08, my-rc*0.04), (cx+rc*0.10, my+rc*0.16), (cx+rc*0.30, my-rc*0.02)],
                PRETO, max(5, e-3), seed+36, 2.2)
    else:
        p.traco([(cx-rc*0.24, my+rc*0.04), (cx+rc*0.24, my+rc*0.04)], PRETO, max(5, e-3), seed+37, 2.0)


def suor(p, cx, cy, tam, seed, k=1.0, n=3):
    """Gotinhas de suor voando — reforça susto e dor."""
    for j in range(n):
        lado = -1 if j % 2 == 0 else 1
        dx = lado * tam * (0.34 + 0.11*j) + lado*tam*0.22*k
        dy = -tam*0.30 + j*tam*0.16 - tam*0.20*k
        r = tam*0.048
        p.forma([(cx+dx, cy+dy-r*1.7), (cx+dx+r, cy+dy+r*0.5), (cx+dx-r, cy+dy+r*0.5)],
                (120, 200, 255), PRETO, max(4, int(tam*0.016)), seed+60+j, amp=2.0)


def balao_susto(p, cx, cy, tam, seed, simbolo="!"):
    from art2 import texto as _t, font as _f
    im = _t(simbolo, _f("marker", int(tam*0.62)), VERMELHO, PRETO, 6)
    p.im.alpha_composite(im, (int(cx - im.width/2), int(cy - im.height/2)))


def seta(p, x0, y0, x1, y1, cor=PRETO, seed=0, esp=11, prog=1.0, curva=0.22):
    """Seta desenhada à mão. `prog` 0..1 faz ela se desenhar."""
    prog = max(0.0, min(1.0, prog))
    if prog < 0.02:
        return
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * curva, my + dx * curva          # ponto de controle: barriga
    pts = []
    N = 16
    for i in range(N + 1):
        u = (i / N) * prog
        a = (1 - u) ** 2
        b = 2 * (1 - u) * u
        c = u ** 2
        pts.append((a * x0 + b * cx + c * x1, a * y0 + b * cy + c * y1))
    p.traco(pts, cor, esp, seed, 3.0)
    if prog > 0.82:
        px, py = pts[-1]
        qx, qy = pts[-3]
        ang = math.atan2(py - qy, px - qx)
        L = esp * 3.1
        for da in (2.5, -2.5):
            p.traco([(px, py), (px + L * math.cos(ang + da), py + L * math.sin(ang + da))],
                    cor, esp, seed + 7, 2.0)


def rotulo(p, txt, x, y, cor=PRETO, tam=54, fonte="marker", contorno=None, esp=None, prog=1.0):
    """Palavra escrita à mão ao lado da seta. Contorno se ajusta para dar contraste."""
    if prog < 0.02:
        return
    if contorno is None:
        contorno = PRETO if cor == BRANCO else BRANCO
    if esp is None:
        esp = 9 if cor == BRANCO else 6
    im = texto(txt, font(fonte, tam), cor, contorno, esp)
    if prog < 1.0:
        w = max(1, int(im.width * prog))
        im = im.crop((0, 0, w, im.height))
    p.im.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))


def aponta(p, txt, ax, ay, tx, ty, t, t0=0.0, cor=PRETO, seed=0, tam=52, esp=11):
    """Seta + rótulo juntos, com a seta se desenhando e a palavra aparecendo depois."""
    k = (t - t0) / 0.30
    # sobre foto, a seta branca precisa de um contorno preto por baixo
    if cor == BRANCO:
        seta(p, tx, ty, ax, ay, PRETO, seed, esp + 7, prog=k)
    seta(p, tx, ty, ax, ay, cor, seed, esp, prog=k)
    rotulo(p, txt, tx, ty - 6, cor, tam, prog=(t - t0 - 0.18) / 0.22)
