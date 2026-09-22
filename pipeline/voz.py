# -*- coding: utf-8 -*-
"""Narracao com a sua propria voz, clonada localmente.

Backend padrao: Chatterbox Multilingual (Resemble AI, licenca MIT, uso comercial
liberado). Roda na CPU, custo zero por caractere, a voz nunca sai da maquina.

IMPORTANTE: este script roda num ambiente Python SEPARADO do resto do pipeline.
Chatterbox exige numpy<2 e o renderizador usa numpy 2.2. Por isso voz.py e um
executavel de linha de comando que so escreve .wav no disco -- o renderizador
consome os arquivos e nunca importa este modulo.

    python3 pipeline/voz.py teste  --ref roteiros/voz_ref.wav
    python3 pipeline/voz.py roteiro --ref roteiros/voz_ref.wav \
        --roteiro pipeline/roteiro_longo.md --out work/tts_voz

Use o atalho ./falar, que ja exporta o PYTHONPATH certo.
"""
import argparse
import os
import re
import sys
import time

VENDOR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vendor", "voz")
if os.path.isdir(VENDOR) and VENDOR not in sys.path:
    sys.path.insert(0, VENDOR)

IDIOMA = "pt"
SR_PIPELINE = 48000  # igual a mixa16.py / sfx.py
_modelo = None


def modelo():
    """Carrega uma vez so. O primeiro uso baixa ~1 GB do HuggingFace."""
    global _modelo
    if _modelo is None:
        import warnings
        warnings.filterwarnings("ignore")
        import torch
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS

        torch.set_num_threads(os.cpu_count() or 8)
        t = time.time()
        print(f"carregando modelo (cpu)...", flush=True)
        _modelo = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
        print(f"  pronto em {time.time()-t:.0f}s", flush=True)
    return _modelo


def falar(texto, saida, ref, exaggeration=0.5, cfg_weight=0.5, temperature=0.8):
    """Sintetiza um trecho e grava em `saida`.

    Grava PCM 16 bits a 48 kHz mono, que e exatamente o que mixa16.py espera.
    O Chatterbox devolve float32 a 24 kHz; gravar isso direto passa no player
    mas quebra o mixer, que le com o modulo `wave` e assume int16.
    """
    import torch
    import torchaudio

    m = modelo()
    wav = m.generate(
        texto,
        language_id=IDIOMA,
        audio_prompt_path=ref,
        exaggeration=exaggeration,
        cfg_weight=cfg_weight,
        temperature=temperature,
    )
    dur = wav.shape[-1] / m.sr
    if m.sr != SR_PIPELINE:
        wav = torchaudio.functional.resample(wav, m.sr, SR_PIPELINE)
    wav = wav.detach().to(torch.float32).clamp(-1.0, 1.0)
    if wav.dim() == 1:
        wav = wav.unsqueeze(0)
    wav = wav[:1]  # mono
    pcm = (wav * 32767.0).round().to(torch.int16)
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    torchaudio.save(saida, pcm, SR_PIPELINE, encoding="PCM_S", bits_per_sample=16)
    return saida, dur


def linhas_do_roteiro(caminho):
    """Mesma convencao do gen_tts_longo.py: '## ' abre capitulo, resto e fala."""
    linhas, cap = [], None
    for ln in open(caminho, encoding="utf-8").read().split("\n"):
        ln = ln.strip()
        if ln.startswith("## "):
            cap = ln[3:].strip()
            continue
        if not ln or ln.startswith("#") or not cap:
            continue
        linhas.append({"i": len(linhas), "ato": cap, "texto": ln})
    return linhas


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("modo", choices=["teste", "roteiro", "frase"])
    p.add_argument("--ref", required=True, help="seu audio de referencia (1-2 min, limpo)")
    p.add_argument("--roteiro", help="arquivo .md (modo roteiro)")
    p.add_argument("--texto", help="texto avulso (modo frase)")
    p.add_argument("--out", default="work/tts_voz")
    p.add_argument("--exaggeration", type=float, default=0.5, help="0.3 sobrio, 0.7 dramatico")
    p.add_argument("--cfg", type=float, default=0.5, help="menor = fala mais rapida e solta")
    a = p.parse_args()

    if not os.path.isfile(a.ref):
        sys.exit(f"audio de referencia nao encontrado: {a.ref}")

    if a.modo == "teste":
        frase = ("Ela nao foge. Quando se sente ameacada, levanta as duas primeiras "
                 "pernas, mostra as presas, e espera voce decidir o que fazer.")
        alvo = os.path.join(a.out, "teste.wav")
        _, dur = falar(frase, alvo, a.ref, a.exaggeration, a.cfg)
        print(f"ok {alvo} ({dur:.1f}s)")
        return

    if a.modo == "frase":
        if not a.texto:
            sys.exit("--texto obrigatorio no modo frase")
        alvo = os.path.join(a.out, "frase.wav")
        _, dur = falar(a.texto, alvo, a.ref, a.exaggeration, a.cfg)
        print(f"ok {alvo} ({dur:.1f}s)")
        return

    if not a.roteiro:
        sys.exit("--roteiro obrigatorio no modo roteiro")
    linhas = linhas_do_roteiro(a.roteiro)
    print(f"{len(linhas)} falas -> {a.out}")
    t0, total = time.time(), 0.0
    for m in linhas:
        alvo = os.path.join(a.out, f"{m['i']:03d}.wav")
        _, dur = falar(m["texto"], alvo, a.ref, a.exaggeration, a.cfg)
        total += dur
        print(f"  {m['i']+1}/{len(linhas)}  {dur:5.1f}s  {m['ato'][:28]}", flush=True)
    import json
    json.dump(linhas, open(os.path.join(a.out, "meta.json"), "w"), ensure_ascii=False, indent=1)
    gasto = time.time() - t0
    print(f"ok {len(linhas)} falas, {total:.0f}s de audio em {gasto:.0f}s ({total/max(gasto,1):.2f}x tempo real)")


if __name__ == "__main__":
    main()
