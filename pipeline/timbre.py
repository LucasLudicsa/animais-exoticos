# -*- coding: utf-8 -*-
"""Da peso e cadencia a narracao: mais grave, mais densa, mais seria.

O Chatterbox nao tem controle de tom. Entao o peso vem depois, com a mesma
cadeia que radio e documentario usam ha decadas:

  grave       desce o tom alguns semitons sem acelerar a fala
  corpo       reforca 120-200 Hz, que e o peito da voz
  limpeza     tira 300-450 Hz, onde mora o embolado
  presenca    levanta 3-5 kHz, onde a consoante fica nitida
  densidade   compressao 3:1, que aproxima a voz do microfone
  cadencia    o 'groove' e a compressao + o grave juntos: a voz para de
              flutuar e passa a assentar

Sem dependencia nova: tudo sai no ffmpeg que o imageio ja traz.

    python3 pipeline/timbre.py entrada.wav saida.wav --semitons -2
"""
import argparse
import os
import subprocess
import sys


def ffmpeg():
    for v in ("vendor/voz", "vendor/asr"):
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), v)
        if os.path.isdir(p):
            sys.path.insert(0, p)
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    cache = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "_ffmpeg_path.txt")
    if os.path.isfile(cache):
        return open(cache).read().strip()
    return "ffmpeg"


def cadeia(semitons=-2.0, corpo=2.5, presenca=2.5, compressao=True, sr=48000):
    """Monta o filtro. semitons negativos = voz mais grave."""
    r = 2 ** (semitons / 12.0)
    f = [
        # desce o tom reamostrando, depois devolve a duracao original
        f"asetrate={int(sr*r)}",
        f"aresample={sr}",
        f"atempo={1/r:.6f}",
        "highpass=f=75",
        f"equalizer=f=160:t=q:w=1.0:g={corpo}",       # peito
        "equalizer=f=380:t=q:w=1.2:g=-2.0",           # tira o embolado
        f"equalizer=f=4000:t=q:w=1.4:g={presenca}",   # consoante nitida
        "deesser=i=0.4",
    ]
    if compressao:
        f.append("acompressor=threshold=-20dB:ratio=3:attack=8:release=140:makeup=3")
    f.append("alimiter=limit=0.95")
    f.append("loudnorm=I=-16:TP=-1.5:LRA=9")
    return ",".join(f)


def taxa(caminho):
    """Le a taxa real do arquivo. Chutar 48k num arquivo de 24k desloca o tom
    uma oitava inteira e corta a duracao pela metade."""
    import wave
    try:
        with wave.open(caminho) as w:
            return w.getframerate()
    except Exception:
        return 48000


def aplica(entrada, saida, **kw):
    kw.setdefault("sr", taxa(entrada))
    cmd = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-i", entrada,
           "-af", cadeia(**kw), "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", saida]
    subprocess.run(cmd, check=True)
    return saida


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada")
    p.add_argument("saida")
    p.add_argument("--semitons", type=float, default=-2.0)
    p.add_argument("--corpo", type=float, default=2.5)
    p.add_argument("--presenca", type=float, default=2.5)
    p.add_argument("--sem-compressao", action="store_true")
    a = p.parse_args()
    aplica(a.entrada, a.saida, semitons=a.semitons, corpo=a.corpo,
           presenca=a.presenca, compressao=not a.sem_compressao)
    print(f"ok {a.saida}")


if __name__ == "__main__":
    main()
