# -*- coding: utf-8 -*-
"""Escolhe a melhor janela de 10s do audio de referencia.

O Chatterbox so olha os primeiros 10 segundos do arquivo (DEC_COND_LEN) e os
primeiros 6 para os tokens do encoder. Gravar 2 minutos nao melhora o clone por
si so -- serve para termos de onde ESCOLHER os 10 segundos certos.

Criterio: fala continua, nivel estavel, silencio curto, maior relacao
sinal-ruido e nada clipado.
"""
import array
import math
import sys
import wave

JANELA = 10.0
PASSO = 0.25
QUADRO = 0.05


def db(x):
    return 20 * math.log10(max(x, 1e-9) / 32768)


def analisa(caminho):
    w = wave.open(caminho)
    sr, n = w.getframerate(), w.getnframes()
    d = array.array("h")
    d.frombytes(w.readframes(n))
    q = int(sr * QUADRO)
    niveis = []
    for i in range(0, len(d) - q, q):
        seg = d[i:i + q]
        niveis.append(math.sqrt(sum(x * x for x in seg) / q))
    return d, sr, niveis, q


def pontua(niveis, ini, fim, piso_global, fala_global):
    jan = niveis[ini:fim]
    if not jan:
        return None
    lim = fala_global * 0.08
    frac_fala = sum(1 for l in jan if l > lim) / len(jan)
    falados = [l for l in jan if l > lim]
    if len(falados) < 10:
        return None
    med = sorted(falados)[len(falados) // 2]
    ordenado = sorted(jan)
    piso = ordenado[int(len(ordenado) * 0.10)]
    snr = db(med) - db(piso)
    # desvio do nivel de fala: queremos constancia
    var = math.sqrt(sum((db(l) - db(med)) ** 2 for l in falados) / len(falados))
    nota = (frac_fala * 40) + (snr * 1.5) - (var * 1.2)
    return {"nota": nota, "frac_fala": frac_fala, "snr": snr, "var": var, "nivel": db(med)}


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "roteiros/voz_ref.wav"
    d, sr, niveis, q = analisa(src)
    ordenado = sorted(niveis)
    piso_g = ordenado[int(len(ordenado) * 0.10)]
    fala_g = ordenado[int(len(ordenado) * 0.90)]

    por_quadro = int(JANELA / QUADRO)
    passo_q = max(1, int(PASSO / QUADRO))
    melhores = []
    for ini in range(0, len(niveis) - por_quadro, passo_q):
        r = pontua(niveis, ini, ini + por_quadro, piso_g, fala_g)
        if r:
            r["t"] = ini * QUADRO
            melhores.append(r)
    melhores.sort(key=lambda r: -r["nota"])
    print(f"{src}: {len(d)/sr:.0f}s, piso {db(piso_g):+.1f} dBFS\n")
    print(f"{'#':>2} {'inicio':>8} {'nota':>6} {'fala%':>6} {'SNR':>5} {'estab':>6} {'nivel':>7}")
    for i, r in enumerate(melhores[:8], 1):
        print(f"{i:>2} {r['t']:>7.1f}s {r['nota']:>6.1f} {r['frac_fala']*100:>5.0f}% "
              f"{r['snr']:>4.0f}dB {r['var']:>5.1f}dB {r['nivel']:>6.1f}dB")
    b = melhores[0]
    print(f"\nmelhor janela: {b['t']:.2f}s -> {b['t']+JANELA:.2f}s")
    print(f"RECORTE={b['t']:.2f}")


if __name__ == "__main__":
    main()
