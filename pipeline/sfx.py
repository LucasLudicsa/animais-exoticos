# -*- coding: utf-8 -*-
"""Efeitos sonoros sintetizados — sem biblioteca de samples."""
import numpy as np

SR = 48000
_rng = np.random.default_rng(11)


def _env(n, atk=0.004, dec=3.0):
    t = np.arange(n) / SR
    e = np.exp(-t * dec)
    a = max(1, int(atk * SR))
    e[:a] *= np.linspace(0, 1, a)
    return e


def toc(dur=0.07):
    """Tique seco do corte."""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 900 * t) * np.exp(-t * 90)
    s += _rng.normal(0, 0.35, n) * np.exp(-t * 150)
    return s * 0.5


def pop(f0=420, dur=0.14):
    """Elemento entrando: varredura de tom pra cima."""
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 2.6 * t / dur)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.003, 26)
    return s * 0.55


def boing(dur=0.34):
    """Mola de desenho animado."""
    n = int(dur * SR); t = np.arange(n) / SR
    f = 300 + 190 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 5)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.003, 8)
    return s * 0.45


def whoosh(dur=0.30, subida=True):
    """Passagem de ar."""
    n = int(dur * SR); t = np.arange(n) / SR
    ru = _rng.normal(0, 1, n)
    k = np.linspace(0.02, 0.45, n) if subida else np.linspace(0.45, 0.02, n)
    out = np.zeros(n); z = 0.0
    for i in range(n):                       # passa-baixa de 1 polo varrendo
        z += k[i] * (ru[i] - z); out[i] = z
    janela = np.sin(np.pi * np.arange(n) / n) ** 1.6
    return out * janela * 0.5


def impacto(dur=0.55):
    """Pancada: entra foto / corte forte."""
    n = int(dur * SR); t = np.arange(n) / SR
    f = 150 * np.exp(-t * 11) + 42
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += _rng.normal(0, 0.5, n) * np.exp(-t * 46)
    return s * 0.6


def erro(dur=0.30):
    """Buzina de errado — o X vermelho."""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * 148 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 111 * t)) * 0.5
    return s * _env(n, 0.004, 7) * 0.32


def ding(f0=1180, dur=0.9):
    """Reveleção positiva."""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for h, a, dc in [(1, 1, 3.2), (2.7, .4, 4.5), (5.1, .18, 6.0)]:
        s += a * np.sin(2 * np.pi * f0 * h * t) * np.exp(-t * dc)
    return s / max(np.abs(s).max(), 1e-9) * 0.34


def tique(dur=0.05):
    """Tique-taque do relógio."""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 200)
    s += _rng.normal(0, 0.25, n) * np.exp(-t * 320)
    return s * 0.30


def tensao(dur=1.2):
    """Tom subindo: a ameaça chegando."""
    n = int(dur * SR); t = np.arange(n) / SR
    f = 110 * (1 + 2.2 * (t / dur) ** 1.7)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    s += 0.35 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    janela = np.clip(np.sin(np.pi * np.arange(n) / n) * 1.5, 0, 1)
    return s * janela * 0.30


def brilho(dur=1.1):
    """Brilhinho da virada — veneno vira remédio."""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for j, f in enumerate([1570, 2090, 2640, 3130]):
        atraso = int(j * 0.055 * SR)
        if atraso >= n: break
        tt = t[: n - atraso]
        s[atraso:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7.5) * (0.85 ** j)
    return s / max(np.abs(s).max(), 1e-9) * 0.28


def risco(dur=0.22):
    """Rabisco de caneta — a seta sendo desenhada."""
    n = int(dur * SR)
    ru = _rng.normal(0, 1, n)
    mod = (0.5 + 0.5 * np.sin(2 * np.pi * 38 * np.arange(n) / SR))
    janela = np.sin(np.pi * np.arange(n) / n)
    out = np.zeros(n); z = 0.0
    for i in range(n):
        z += 0.30 * (ru[i] - z); out[i] = z
    return out * mod * janela * 0.34


BANCO = {"toc": toc, "pop": pop, "boing": boing, "whoosh": whoosh, "impacto": impacto,
         "erro": erro, "ding": ding, "tique": tique, "tensao": tensao,
         "brilho": brilho, "risco": risco}
