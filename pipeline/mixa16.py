# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK
import json, wave, sys
import numpy as np
sys.path.insert(0, PIPE)
import sfx

SR=48000
tl=json.load(open(f"{PIPE}/timeline_longo.json")); LIN=tl["linhas"]; TOT=tl["total"]
N=int(TOT*SR)+SR; mix=np.zeros(N)
def soma(sig,t0,g=1.0):
    i0=int(t0*SR)
    if i0<0 or i0>=N: return
    k=min(len(sig),N-i0); mix[i0:i0+k]+=sig[:k]*g
def ler(p):
    w=wave.open(p,"rb"); d=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768.0
    w.close(); return d
FOTOS={7,12,54,57,105}
GRANDE={1,3,20,25,26,34,36,38,42,49,52,61,64,81,87,94,98,106,109,111,114}
for m in LIN:
    d=ler(f"{WORK}/tts_longo/{m['i']:03d}.wav")
    fl=min(240,len(d)//8)
    if fl>4: d[:fl]*=np.linspace(0,1,fl); d[-fl:]*=np.linspace(1,0,fl)
    soma(d,m["in"],1.0)
G=0.38
for n,m in enumerate(LIN):
    ini = 0.0 if n==0 else m["in"]
    if m.get("cap_inicio"):
        soma(sfx.impacto(), max(0.0,ini-3.0), G*0.85)
        soma(sfx.brilho(), max(0.0,ini-2.85), G*0.5)
        soma(sfx.risco(), max(0.0,ini-2.55), G*0.8)
    if m["i"] in FOTOS:      soma(sfx.impacto(), ini, G*0.9)
    elif m["i"] in GRANDE:   soma(sfx.pop(480), ini, G*0.85); soma(sfx.boing(), ini, G*0.35)
    else:                    soma(sfx.toc(), ini, G*0.7)
    if m["i"] in (2,23,47,77): soma(sfx.tensao(0.9), ini, G*0.8)
    if m["i"] in (11,68,72,76,85,120): soma(sfx.erro(), ini+0.55, G*0.85)
    if m["i"] in (70,71,79,80,86,89): soma(sfx.ding(), ini+0.45, G*0.55)
    if m["i"] in (101,102,103): soma(sfx.boing(), ini+0.40, G*0.6)
    if m["i"] in (112,113,116,118,124): soma(sfx.brilho(), ini+0.55, G*0.7)
pico=np.max(np.abs(mix))
if pico>0: mix=mix/pico*0.89
out=(mix*32767).astype(np.int16)
w=wave.open(f"{WORK}/trilha16.wav","wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(out.tobytes()); w.close()
print(f"trilha16.wav {len(out)/SR:.1f}s pico {pico:.2f}")
