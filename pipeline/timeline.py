# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK, OUT, ROTEIROS
import re, json
import importlib.util
spec = importlib.util.spec_from_file_location("s", os.path.join(PIPE, 'silabas.py'))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)

# taxa (síl/s) e pausa depois da linha (s), por ato — espelha a curva medida do vídeo A
ATOS = {
 "1 GANCHO":   (2.6, 0.90),
 "2 ORIGEM":   (5.2, 0.40),
 "3 ESCALA":   (5.2, 0.42),
 "4 CONCRETO": (4.6, 0.55),
 "5 PAVOR":    (5.8, 0.30),
 "6 PROVA":    (5.4, 0.35),
 "7 VIRADA":   (5.2, 0.42),
 "8 TESE":     (4.5, 0.65),
}

txt = open(os.path.join(ROTEIROS, 'roteiro_v3.md')).read()
blocos = [b for b in re.split(r"^##\s*", txt, flags=re.M) if b.strip()]

t = 0.0; out = []
print(f"{'IN':>7}{'OUT':>8}{'dur':>6}{'síl':>5}{'síl/s':>7}  LINHA")
print("-"*96)
for b in blocos:
    ls = b.split("\n"); nome = ls[0].strip()
    rate, pausa = ATOS[nome]
    print(f"\n── {nome} ──")
    for linha in [l.strip() for l in ls[1:] if l.strip()]:
        w, s = S.analisa(linha)
        d = s/rate
        print(f"{t:7.2f}{t+d:8.2f}{d:6.2f}{s:5d}{rate:7.1f}  {linha}")
        out.append({"ato":nome,"in":round(t,2),"out":round(t+d,2),"dur":round(d,2),"sil":s,"texto":linha})
        t += d + pausa
    t += 0.08   # respiro extra entre atos
print("\n" + "="*96)
print(f"DURAÇÃO TOTAL: {t:.1f}s   (vídeo A original = 87.9s, vídeo B = 77.7s)")
fala = sum(o['dur'] for o in out)
print(f"fala {fala:.1f}s ({fala/t*100:.0f}%) | pausas {t-fala:.1f}s ({(t-fala)/t*100:.0f}%)")
print(f"{len(out)} linhas = {len(out)} cartelas -> 1 corte a cada {t/len(out):.1f}s")
json.dump(out, open(os.path.join(WORK, 'timeline.json'),"w"), ensure_ascii=False, indent=1)
