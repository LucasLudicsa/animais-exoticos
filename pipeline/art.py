# -*- coding: utf-8 -*-
import os
from paths import PIPE
"""Sistema de arte — Armadeira. Traço de prancha científica sobre fundo escuro."""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1080, 1920
SS = 2  # supersampling do desenho vetorial

BREU   = (12, 18, 16)
BREU_J = (15, 29, 24)
MATA   = (22, 33, 28)
AREIA  = (244, 239, 230)
URUCUM = (228, 87, 46)
JADE   = (88, 184, 148)
DIM    = (62, 91, 78)
DIM_U  = (116, 56, 33)
CINZA  = (154, 168, 161)

FDIR = os.path.join(PIPE, 'fonts')

_fc = {}
def font(kind, size, weight=None):
    key = (kind, size, weight)
    if key in _fc:
        return _fc[key]
    if kind == "display":
        f = ImageFont.truetype(f"{FDIR}/Bricolage.ttf", size)
        try:
            f.set_variation_by_axes([min(96, max(12, size // 8)), weight or 800, 100])
        except Exception:
            pass
    elif kind == "mono":
        f = ImageFont.truetype(f"{FDIR}/SplineSansMono.ttf", size)
        try:
            f.set_variation_by_axes([weight or 500])
        except Exception:
            pass
    else:
        f = ImageFont.truetype(f"{FDIR}/SplineSans.ttf", size)
        try:
            f.set_variation_by_axes([weight or 600])
        except Exception:
            pass
    _fc[key] = f
    return f


# ---------------------------------------------------------------- grão
def make_grain(seed=7):
    random.seed(seed)
    g = Image.new("L", (W // 3, H // 3))
    px = g.load()
    for y in range(g.height):
        for x in range(g.width):
            px[x, y] = random.randint(0, 255)
    g = g.resize((W, H), Image.BILINEAR)
    layer = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    layer.putalpha(g.point(lambda v: int(v * 0.055)))
    return layer

# ------------------------------------------------- desenho supersampled
class Pad:
    """Camada RGBA desenhada em SS x e reduzida — dá antialias ao traço."""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def line(self, pts, color, width):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=color,
                    width=int(width * SS), joint="curve")

    def ellipse(self, cx, cy, rx, ry, color, width):
        self.d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS],
                       outline=color, width=int(width * SS))

    def disc(self, cx, cy, r, color):
        self.d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=color)

    def rect(self, x0, y0, x1, y1, color, width):
        self.d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], outline=color, width=int(width * SS))

    def out(self):
        return self.im.resize((self.w, self.h), Image.LANCZOS)


# ------------------------------------------------------------- a aranha
# geometria em coordenadas do SVG (-200..200), origem no corpo
_PERNAS_BAIXO = [
    [(30, 4), (102, 26), (156, -6)],
    [(28, 22), (98, 64), (148, 96)],
]
_PERNAS_CIMA = [
    [(26, -20), (88, -58), (114, -146)],
    [(22, -34), (70, -84), (86, -172)],
]

def aranha(size, cor_corpo, cor_armada, traco=5.0, armada=True, abertura=1.0):
    """Desenha a armadeira. `abertura` 0..1 ergue o par dianteiro."""
    pad = Pad(size, size)
    k = size / 420.0
    cx, cy = size / 2, size / 2 + 10 * k

    def T(p):
        return (cx + p[0] * k, cy + p[1] * k)

    lw = traco * k

    for base in _PERNAS_BAIXO:
        for sgn in (1, -1):
            pts = [T((p[0] * sgn, p[1])) for p in base]
            pad.line(pts, cor_corpo, lw)

    for base in _PERNAS_CIMA:
        for sgn in (1, -1):
            pts = []
            for p in base:
                y = p[1] * abertura + (abs(p[1]) * 0.55) * (1 - abertura)
                pts.append(T((p[0] * sgn, y)))
            pad.line(pts, cor_armada if armada else cor_corpo, lw * 1.2)

    pad.ellipse(cx, cy + 62 * k, 38 * k, 54 * k, cor_corpo, lw)
    pad.ellipse(cx, cy - 12 * k, 34 * k, 42 * k, cor_corpo, lw)

    for sgn in (1, -1):
        pad.line([T((14 * sgn, -44)), T((32 * sgn, -66)), T((30 * sgn, -88))], cor_corpo, lw * 0.8)

    for ox, oy, r in [(-11, -44, 3.4), (0, -47, 3.4), (11, -44, 3.4), (-6, -36, 2.6), (6, -36, 2.6)]:
        p = T((ox, oy))
        pad.disc(p[0], p[1], r * k * 1.15, AREIA)

    return pad.out()


# ------------------------------------------------------------ utilidades
def text_img(txt, f, color, spacing=10, align="left", max_w=None):
    linhas = txt.split("\n")
    if max_w:
        novo = []
        for ln in linhas:
            cur = ""
            for p in ln.split():
                t = (cur + " " + p).strip()
                if f.getbbox(t)[2] - f.getbbox(t)[0] > max_w and cur:
                    novo.append(cur); cur = p
                else:
                    cur = t
            novo.append(cur)
        linhas = novo
    tmp = Image.new("RGBA", (10, 10))
    d0 = ImageDraw.Draw(tmp)
    ws, hs = [], []
    for ln in linhas:
        b = d0.textbbox((0, 0), ln, font=f)
        ws.append(b[2] - b[0]); hs.append(b[3] - b[1])
    asc, desc = f.getmetrics()
    lh = asc + desc
    tw = max(ws) if ws else 1
    th = lh * len(linhas) + spacing * (len(linhas) - 1)
    im = Image.new("RGBA", (max(tw, 1) + 8, max(th, 1) + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 0
    for i, ln in enumerate(linhas):
        x = 0
        if align == "center":
            x = (tw - ws[i]) // 2
        elif align == "right":
            x = tw - ws[i]
        d.text((x, y), ln, font=f, fill=color)
        y += lh + spacing
    return im


def paste(base, im, cx, cy, scale=1.0, alpha=1.0, anchor="c"):
    if im is None:
        return
    if scale != 1.0:
        nw = max(1, int(im.width * scale)); nh = max(1, int(im.height * scale))
        im = im.resize((nw, nh), Image.LANCZOS)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * max(0.0, min(1.0, alpha))))
        im = im.copy(); im.putalpha(a)
    if anchor == "c":
        x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    elif anchor == "l":
        x, y = int(cx), int(cy - im.height / 2)
    elif anchor == "tl":
        x, y = int(cx), int(cy)
    else:
        x, y = int(cx - im.width / 2), int(cy)
    base.alpha_composite(im, (x, y))


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - pow(1 - t, 3)
