# -*- coding: utf-8 -*-
"""Mede se a narracao esta INTELIGIVEL, nao se esta parecida.

Semelhanca de locutor e a metrica errada quando a gravacao original e um pouco
enrolada: um clone mais fiel reproduz o enrolado. Aqui a pergunta e outra --
uma maquina consegue entender o que foi dito?

Transcreve com Whisper e compara com o texto pretendido (WER). Quanto menor,
mais clara a diccao.
"""
import os
import re
import sys

# SO o ambiente do Whisper. Misturar com vendor/voz quebra os dois:
# o asr traz tokenizers novo demais para o transformers que o Chatterbox exige.
_asr = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vendor", "asr")
if os.path.isdir(_asr):
    sys.path.insert(0, _asr)

_modelo = None


def normaliza(t):
    t = t.lower()
    t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
    ac = str.maketrans("áàâãéêíóôõúüç", "aaaaeeiooouuc")
    return t.translate(ac).split()


def wer(ref, hip):
    r, h = normaliza(ref), normaliza(hip)
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            c = 0 if r[i - 1] == h[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + c)
    return d[len(r)][len(h)] / max(len(r), 1)


def modelo():
    global _modelo
    if _modelo is None:
        from faster_whisper import WhisperModel
        _modelo = WhisperModel("small", device="cpu", compute_type="int8")
    return _modelo


def transcreve(caminho):
    segs, _ = modelo().transcribe(caminho, language="pt", beam_size=5)
    return " ".join(s.text.strip() for s in segs)


def main():
    alvo = sys.argv[1]
    arquivos = sys.argv[2:]
    print(f"alvo: {alvo}\n")
    print(f"{'arquivo':<24}{'WER':>7}   transcricao")
    linhas = []
    for f in arquivos:
        if not os.path.isfile(f):
            continue
        t = transcreve(f)
        e = wer(alvo, t)
        linhas.append((e, f, t))
        print(f"{os.path.basename(f):<24}{e*100:>6.1f}%   {t[:70]}", flush=True)
    linhas.sort()
    print(f"\nmais claro: {os.path.basename(linhas[0][1])} (WER {linhas[0][0]*100:.1f}%)")


if __name__ == "__main__":
    main()
