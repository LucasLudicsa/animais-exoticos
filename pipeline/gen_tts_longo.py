# -*- coding: utf-8 -*-
import os
from paths import PIPE, WORK, OUT
import asyncio, edge_tts, os, re, json

OUT=f"{WORK}/tts_longo"; VOZ="pt-BR-AntonioNeural"
RITMO={"1 ABERTURA":("-6%",0.42),"2 QUEM E ELA":("+6%",0.32),"3 CACADORA":("+8%",0.30),
 "4 O VENENO":("+4%",0.34),"5 OS ACIDENTES":("+8%",0.30),"6 QUEM MAIS PICA":("+8%",0.30),
 "7 NAO CONFUNDA":("+8%",0.30),"8 COMO RECONHECER":("+4%",0.34),"9 COMO EVITAR":("+6%",0.32),
 "10 O QUE FAZER":("+6%",0.32),"11 NO HOSPITAL":("+6%",0.32),"12 O SORO":("+4%",0.34),
 "13 VIRA REMEDIO":("+2%",0.36),"14 FECHO":("-6%",0.50)}
FALA={"Phoneutria":"Foneutria","PnTx2-6":"P N T X dois traço seis","SUS":"Sus"}
txt=open(f"{PIPE}/roteiro_longo.md").read()
linhas=[]; cap=None
for ln in txt.split("\n"):
    ln=ln.strip()
    if ln.startswith("## "): cap=ln[3:].strip(); continue
    if not ln or not cap: continue
    fal=ln
    for a,b in FALA.items(): fal=fal.replace(a,b)
    linhas.append({"i":len(linhas),"ato":cap,"texto":fal,"legenda":ln,
                   "rate":RITMO[cap][0],"pausa":RITMO[cap][1]})
async def main():
    os.makedirs(OUT,exist_ok=True)
    for m in linhas:
        c=edge_tts.Communicate(m["texto"],VOZ,rate=m["rate"],pitch="-6Hz")
        await c.save(f"{OUT}/{m['i']:03d}.mp3")
        if m["i"]%20==0: print(f"  {m['i']}/{len(linhas)}",flush=True)
    json.dump(linhas,open(f"{OUT}/meta.json","w"),ensure_ascii=False,indent=1)
    print(f"ok {len(linhas)} falas")
asyncio.run(main())
