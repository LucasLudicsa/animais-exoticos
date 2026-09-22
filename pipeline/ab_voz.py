# -*- coding: utf-8 -*-
"""Compara varias referencias de voz e diz qual clona melhor.

Carrega o modelo uma vez so, gera a mesma frase a partir de cada referencia
(duas vezes, para diluir o sorteio) e mede a semelhanca de locutor contra
trechos do original que nao viraram referencia.
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
import torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

S3_SR = 16000
ORIG = "roteiros/voz_ref.wav"
HELDOUT = [(40, 50), (60, 70), (80, 90), (100, 110)]
FRASE = ("Existe uma cobra no Brasil que salvou mais vidas do que tirou. "
         "Do veneno dela saiu um remedio para pressao alta.")
REFS = ["cru_00", "leve_00", "ref_A", "cru_18", "leve_18", "ref_B"]
N = 2


def emb(enc, y):
    t = torch.from_numpy(y).float().unsqueeze(0)
    with torch.no_grad():
        return F.normalize(enc.inference(t), dim=-1)


def emb_file(enc, p, ini=None, dur=None):
    y, _ = librosa.load(p, sr=S3_SR, offset=ini or 0, duration=dur)
    return emb(enc, y)


def main():
    print("carregando modelo...", flush=True)
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    enc = m.s3gen.speaker_encoder

    reais = [emb_file(enc, ORIG, i, j - i) for i, j in HELDOUT]
    pares = [float(F.cosine_similarity(reais[a], reais[b]))
             for a in range(len(reais)) for b in range(a + 1, len(reais))]
    teto = sum(pares) / len(pares)
    print(f"teto (voce vs voce): {teto:.3f}\n", flush=True)

    res = []
    for nome in REFS:
        rp = f"work/refs/{nome}.wav"
        if not os.path.isfile(rp):
            continue
        sims = []
        for k in range(N):
            torch.manual_seed(1234 + k)
            wav = m.generate(FRASE, language_id="pt", audio_prompt_path=rp,
                             exaggeration=0.5, cfg_weight=0.5, temperature=0.8)
            y = wav.squeeze(0).detach().cpu().numpy()
            if m.sr != S3_SR:
                y = librosa.resample(y, orig_sr=m.sr, target_sr=S3_SR)
            e = emb(enc, y)
            sims.append(sum(float(F.cosine_similarity(e, r)) for r in reais) / len(reais))
            torchaudio.save(f"work/refs/out_{nome}_{k}.wav",
                            (wav.detach().cpu() * 32767).clamp(-32768, 32767).to(torch.int16),
                            m.sr, encoding="PCM_S", bits_per_sample=16)
        med = sum(sims) / len(sims)
        res.append((med, nome, sims))
        print(f"  {nome:<9} {med:.3f}  ({', '.join(f'{s:.3f}' for s in sims)})", flush=True)

    res.sort(reverse=True)
    print(f"\n{'referencia':<12}{'semelhanca':>11}{'% do teto':>11}")
    for med, nome, _ in res:
        print(f"{nome:<12}{med:>11.3f}{med/teto*100:>10.0f}%")
    print(f"\nmelhor: {res[0][1]}")


if __name__ == "__main__":
    main()
