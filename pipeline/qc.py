import os
from paths import WORK
import sys, glob
from PIL import Image, ImageChops, ImageStat

fs=sorted(glob.glob(f"{WORK}/qc/N/*.jpg"))
prev=None; diffs=[]
for i,f in enumerate(fs):
    im=Image.open(f).convert('L')
    if prev is not None:
        diffs.append((i/4.0, ImageStat.Stat(ImageChops.difference(im,prev)).mean[0]))
    prev=im
ev=[];inb=False
for t,d in diffs:
    if d>=2.0 and not inb: ev.append(t);inb=True
    elif d<2.0: inb=False
dur=len(fs)/4.0
static=sum(1 for _,d in diffs if d<0.5)
print(f"duracao {dur:.1f}s | transicoes {len(ev)} (1 a cada {dur/max(len(ev),1):.1f}s) | parado {static/len(diffs)*100:.0f}%")
print(f"original A: 21 / 4.2s / 58% parado")
print(f"original B: 20 / 3.9s / 70% parado")
