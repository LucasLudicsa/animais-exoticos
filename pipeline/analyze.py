import os
from paths import WORK
from PIL import Image, ImageChops, ImageStat
import glob, os, sys, math

SP = sys.argv[1]

def band(im):
    """Find vertical extent of non-black content band."""
    g = im.convert('L')
    w,h = g.size
    rows = []
    px = g.load()
    for y in range(h):
        s = sum(px[x,y] for x in range(0,w,4))/ (w/4)
        rows.append(s)
    top = next((y for y,v in enumerate(rows) if v > 18), 0)
    bot = next((y for y in range(h-1,-1,-1) if rows[y] > 18), h-1)
    return top, bot, bot-top+1

def yellowness(im):
    """Fraction of the content band that is the flat yellow card colour."""
    rgb = im.convert('RGB'); w,h = rgb.size; px = rgb.load()
    t,b,_ = band(im)
    tot = 0; yel = 0
    for y in range(t, b+1, 2):
        for x in range(0, w, 2):
            r,g,bl = px[x,y]; tot += 1
            if r>190 and 150<g<215 and bl<130 and (r-bl)>80:
                yel += 1
    return yel/max(tot,1)

for tag in ['A','B']:
    files = sorted(glob.glob(f"{WORK}/dense/{tag}/*.jpg"))
    print(f"\n===== {tag} =====  frames={len(files)}  ({len(files)/4:.1f}s @4fps)")
    prev = None
    rows = []
    for i,fp in enumerate(files):
        im = Image.open(fp)
        t,b,hh = band(im)
        y = yellowness(im)
        if prev is not None:
            d = ImageChops.difference(im.convert('L'), prev)
            diff = ImageStat.Stat(d).mean[0]
        else:
            diff = 0.0
        rows.append((i/4.0, t, b, hh, y, diff))
        prev = im.convert('L')
    # print compact table every 0.5s
    print(" time  bandtop bandbot bandH  yellow%  framediff")
    for r in rows:
        if abs(r[0]*2 - round(r[0]*2)) < 1e-6:
            print(f"{r[0]:6.2f} {r[1]:7d} {r[2]:7d} {r[3]:5d} {r[4]*100:7.1f}  {r[5]:8.2f}")
    import pickle
    pickle.dump(rows, open(f"{WORK}/rows_{tag}.pkl","wb"))
