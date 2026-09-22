# -*- coding: utf-8 -*-
"""Acha os ajustes que deixam a narracao ANIMADA sem perder a diccao.

"Monotono" nao e opiniao, e medida: numa fala sem energia o tom varia pouco.
Aqui cada combinacao e avaliada em tres eixos ao mesmo tempo --

  animacao  desvio do tom em semitons (maior = mais expressivo)
  clareza   WER do Whisper contra o texto pretendido (menor = melhor)
  voce      semelhanca de locutor contra trechos reais (maior = mais voce)

Nao existe "melhor" num eixo so: exagero demais destroi a diccao. O que
interessa e o ponto que sobe a animacao sem estragar os outros dois.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SO o ambiente do Chatterbox. O Whisper roda em subprocesso (clareza.py),
# porque os dois pinam versoes incompativeis de tokenizers/numpy.
_voz = os.path.join(RAIZ, "vendor", "voz")
if os.path.isdir(_voz):
    sys.path.insert(0, _voz)

import warnings
warnings.filterwarnings("ignore")
import librosa
import numpy as np
import torch
import torch.nn.functional as F
import torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

import subprocess
import json as _json


def wer_lote(texto, arquivos):
    """Chama o Whisper num processo a parte e devolve {arquivo: WER}."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(RAIZ, "vendor", "asr")
    r = subprocess.run([sys.executable, os.path.join(RAIZ, "pipeline", "clareza.py"),
                        texto] + arquivos, capture_output=True, text=True, env=env)
    out = {}
    for ln in r.stdout.split("\n"):
        m = re.match(r"^(\S+\.wav)\s+(\d+\.\d)%", ln.strip())
        if m:
            out[m.group(1)] = float(m.group(2)) / 100
    if not out:
        print("  (aviso: Whisper nao retornou WER)", r.stderr[-300:], flush=True)
    return out

S3_SR = 16000
REF = "work/refs/leve_00.wav"
ORIG = "roteiros/voz_ref.wav"
HELDOUT = [(40, 50), (60, 70), (80, 90), (100, 110)]
TEXTO = ("Existe uma cobra no Brasil que salvou mais vidas do que tirou. "
         "Ela e a jararaca, e do veneno dela saiu um dos remedios "
         "para pressao alta mais usados do mundo inteiro.")

GRADE = [
    (0.50, 0.50, "atual"),
    (0.65, 0.50, "animado"),
    (0.80, 0.50, "muito animado"),
    (0.65, 0.30, "animado + solto"),
    (0.80, 0.30, "maximo"),
    (0.50, 0.30, "solto"),
]


def tom_semitons(y, sr):
    """Desvio do tom em semitons: o quanto a voz sobe e desce."""
    f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=320, sr=sr, frame_length=1024)
    f0 = f0[~np.isnan(f0)]
    if len(f0) < 20:
        return 0.0, 0.0
    semi = 12 * np.log2(f0 / np.median(f0))
    return float(np.std(semi)), float(np.percentile(semi, 95) - np.percentile(semi, 5))


def main():
    print("carregando modelo...", flush=True)
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    enc = m.s3gen.speaker_encoder

    def emb(y):
        with torch.no_grad():
            return F.normalize(enc.inference(torch.from_numpy(y).float().unsqueeze(0)), dim=-1)

    reais = []
    for i, j in HELDOUT:
        y, _ = librosa.load(ORIG, sr=S3_SR, offset=i, duration=j - i)
        reais.append(emb(y))

    print(f"\ngerando {len(GRADE)} versoes...", flush=True)
    dados = []
    for exa, cfg, nome in GRADE:
        torch.manual_seed(1234)
        wav = m.generate(TEXTO, language_id="pt", audio_prompt_path=REF,
                         exaggeration=exa, cfg_weight=cfg, temperature=0.8)
        y24 = wav.squeeze(0).detach().cpu().numpy()
        caminho = f"work/refs/en_{int(exa*100)}_{int(cfg*100)}.wav"
        torchaudio.save(caminho, (wav.detach().cpu() * 32767).clamp(-32768, 32767).to(torch.int16),
                        m.sr, encoding="PCM_S", bits_per_sample=16)
        std, faixa = tom_semitons(y24, m.sr)
        y16 = librosa.resample(y24, orig_sr=m.sr, target_sr=S3_SR)
        sim = sum(float(F.cosine_similarity(emb(y16), r)) for r in reais) / len(reais)
        dur = len(y24) / m.sr
        dados.append({"nome": nome, "exa": exa, "cfg": cfg, "std": std, "faixa": faixa,
                      "sim": sim, "dur": dur, "arq": caminho})
        print(f"  {nome:<18} tom {std:.2f}st  voce {sim:.3f}  {dur:.1f}s", flush=True)

    print("\nmedindo clareza com Whisper...", flush=True)
    wers = wer_lote(TEXTO, [d["arq"] for d in dados])
    for d in dados:
        d["wer"] = wers.get(os.path.basename(d["arq"]))

    print(f"\n{'ajuste':<18}{'exa':>5}{'cfg':>5}{'animacao':>10}{'faixa':>8}{'clareza':>9}{'voce':>7}")
    for d in dados:
        w = f"{d['wer']*100:.1f}%" if d["wer"] is not None else "  -  "
        print(f"{d['nome']:<18}{d['exa']:>5.2f}{d['cfg']:>5.2f}{d['std']:>9.2f}st{d['faixa']:>8.1f}{w:>9}{d['sim']:>7.3f}")

    base = dados[0]
    print("\n--- comparado com o ajuste atual ---")
    for d in dados[1:]:
        d_an = (d["std"] / base["std"] - 1) * 100 if base["std"] else 0
        if d["wer"] is not None and base["wer"] is not None:
            d_cl = (d["wer"] - base["wer"]) * 100
            cl = f"clareza {d_cl:+.1f}pp"
        else:
            cl = "clareza n/d"
        d_id = (d["sim"] - base["sim"])
        print(f"{d['nome']:<18} animacao {d_an:+5.0f}%   {cl:<16} voce {d_id:+.3f}   {os.path.basename(d['arq'])}")

    _json.dump(dados, open("work/refs/energia.json", "w"), ensure_ascii=False, indent=1)
    print("\nouca os arquivos work/refs/en_*.wav e me diga qual soa certo.")


if __name__ == "__main__":
    main()
