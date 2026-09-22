# -*- coding: utf-8 -*-
"""Mede o quanto a voz gerada se parece com a voz real, objetivamente.

Usa o proprio codificador de locutor do Chatterbox (x-vector) e compara por
cosseno. Para nao trapacear, a voz gerada NAO e comparada com a janela que
serviu de referencia: e comparada com trechos do original que ficaram de fora.

O teto e a semelhanca do original com ele mesmo em trechos diferentes -- nenhum
clone deve passar disso. E o piso util e a semelhanca entre pessoas diferentes.
"""
import os
import sys

VENDOR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vendor", "voz")
if os.path.isdir(VENDOR):
    sys.path.insert(0, VENDOR)

import warnings
warnings.filterwarnings("ignore")
import librosa
import torch
import torch.nn.functional as F
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

S3_SR = 16000
ORIG = "roteiros/voz_ref.wav"
# trechos do original que NAO foram usados como referencia (A=0-10s, B=18.8-28.8s)
HELDOUT = [(40, 50), (60, 70), (80, 90), (100, 110)]


def emb(enc, caminho, ini=None, dur=None):
    y, _ = librosa.load(caminho, sr=S3_SR, offset=ini or 0, duration=dur)
    t = torch.from_numpy(y).float().unsqueeze(0)
    with torch.no_grad():
        return F.normalize(enc.inference(t), dim=-1)


def main():
    print("carregando modelo...", flush=True)
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    enc = m.s3gen.speaker_encoder

    reais = [emb(enc, ORIG, i, j - i) for i, j in HELDOUT]

    # teto: original contra original, trechos diferentes
    pares = [float(F.cosine_similarity(reais[a], reais[b]))
             for a in range(len(reais)) for b in range(a + 1, len(reais))]
    teto = sum(pares) / len(pares)

    print(f"\nteto (voce vs voce, trechos diferentes): {teto:.3f}\n")
    print(f"{'amostra':<14}{'semelhanca':>11}{'% do teto':>11}")
    for n in ["A", "B"]:
        p = f"work/refs/voz_{n}.wav"
        if not os.path.isfile(p):
            continue
        e = emb(enc, p)
        s = sum(float(F.cosine_similarity(e, r)) for r in reais) / len(reais)
        print(f"voz_{n:<10}{s:>11.3f}{s/teto*100:>10.0f}%")


if __name__ == "__main__":
    main()
