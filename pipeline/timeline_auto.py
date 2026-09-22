# -*- coding: utf-8 -*-
"""Monta a linha do tempo a partir da narracao que o modelo acabou de gerar.

Le a duracao real de cada .wav em vez de estimar por contagem de palavras.
As pausas saem do estilo do episodio: mais longas na abertura e no fecho,
curtas no meio, e nunca as mesmas duas vezes -- ritmo identico em todo video
e mais um sinal de esteira.

    python3 pipeline/timeline_auto.py jararaca work/jararaca/tts
"""
import json
import os
import random
import sys
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import variacao


def dur(caminho):
    with wave.open(caminho) as w:
        return w.getnframes() / w.getframerate()


def monta(episodio, dir_tts, saida=None):
    meta = json.load(open(os.path.join(dir_tts, "meta.json"), encoding="utf-8"))
    est = variacao.estilo(episodio)
    r = random.Random(est["semente"])

    linhas = []
    tempo = 0.0
    visto = set()
    n = len(meta)
    for m in meta:
        wav = os.path.join(dir_tts, f"{m['i']:03d}.wav")
        if not os.path.isfile(wav):
            raise SystemExit(f"falta narracao: {wav}")
        d = dur(wav)
        p = m["i"] / max(n - 1, 1)
        # respiro: sobra mais ar no comeco e no fim, menos no miolo
        if p < 0.12 or p > 0.88:
            pausa = r.uniform(0.44, 0.62)
        else:
            pausa = r.uniform(0.20, 0.34)
        cap = m["ato"] not in visto
        if cap:
            visto.add(m["ato"])
            pausa += 0.25          # deixa a cartela de capitulo respirar
        linhas.append({
            "i": m["i"], "ato": m["ato"], "texto": m["texto"], "legenda": m["texto"],
            "pausa": round(pausa, 3), "in": round(tempo, 3), "dur": round(d, 3),
            "out": round(tempo + d, 3), "cap_inicio": cap,
        })
        tempo += d + pausa

    tl = {"total": round(tempo, 3), "linhas": linhas, "capitulos": sorted(visto)}
    saida = saida or os.path.join(os.path.dirname(dir_tts), "timeline.json")
    json.dump(tl, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    mm, ss = divmod(tl["total"], 60)
    print(f"{len(linhas)} falas, {len(visto)} capitulos")
    print(f"duracao: {int(mm)}min{int(ss):02d}s  ->  {saida}")
    return tl


if __name__ == "__main__":
    monta(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
