# -*- coding: utf-8 -*-
import re, sys, unicodedata

V = "aeiouáéíóúâêôãõàäëïöü"
# ditongos decrescentes/crescentes tratados como 1 nucleo
DIT = ["ai","ei","oi","ui","au","eu","iu","ou","ãe","õe","ão","ãi",
       "ia","ie","io","iu","ua","ue","ui","uo"]

def silabas(palavra):
    p = palavra.lower()
    p = re.sub(r"[^a-záéíóúâêôãõàçüñ]", "", p)
    if not p: return 0
    n = 0; i = 0
    while i < len(p):
        if p[i] in V:
            n += 1
            # consome grupo vocalico como 1 nucleo (aproximacao de ditongo)
            j = i+1
            while j < len(p) and p[j] in V:
                par = p[j-1]+p[j]
                if par in DIT:
                    j += 1
                else:
                    break   # hiato -> nova silaba
            i = j
        else:
            i += 1
    return max(n,1)

def analisa(texto):
    palavras = re.findall(r"[A-Za-zÀ-ÿ]+", texto)
    s = sum(silabas(w) for w in palavras)
    return len(palavras), s

if __name__ == "__main__":
    txt = sys.stdin.read()
    blocos = re.split(r"^##\s*", txt, flags=re.M)
    tot_w = tot_s = 0
    print(f"{'BLOCO':<34}{'pal':>5}{'síl':>6}{'seg@5.0':>9}{'seg@5.3':>9}")
    print("-"*63)
    for b in blocos:
        if not b.strip(): continue
        linhas = b.split("\n")
        nome = linhas[0].strip()
        corpo = "\n".join(linhas[1:])
        corpo = re.sub(r"\[.*?\]", "", corpo)          # remove anotacoes
        w,s = analisa(corpo)
        if w == 0: continue
        tot_w += w; tot_s += s
        print(f"{nome:<34}{w:>5}{s:>6}{s/5.0:>9.1f}{s/5.3:>9.1f}")
    print("-"*63)
    print(f"{'TOTAL':<34}{tot_w:>5}{tot_s:>6}{tot_s/5.0:>9.1f}{tot_s/5.3:>9.1f}")
    print()
    for r in (4.8,5.0,5.3):
        fala = tot_s/r
        print(f"  a {r} síl/s -> {fala:.1f}s de fala + 9.0s de pausas = {fala+9:.1f}s total")
