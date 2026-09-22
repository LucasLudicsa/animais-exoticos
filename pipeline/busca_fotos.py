# -*- coding: utf-8 -*-
import os
from paths import PIPE
"""Busca fotos de licença livre no Commons e baixa as melhores por batida."""
import urllib.request, urllib.parse, json, os, re, ssl


DIR = f"{PIPE}/fotos"
os.makedirs(DIR, exist_ok=True)
UA = {"User-Agent": "ArmadeiraShort/1.0 (educational short film; contact: local)"}
CTX = ssl.create_default_context()

# quanto menor o número, melhor a licença para uso comercial sem contaminar a obra
def rank_lic(l):
    l = (l or "").lower()
    if "cc0" in l or "public domain" in l or "pd" == l.strip():
        return 0
    if "cc by-sa" in l or "cc-by-sa" in l:
        return 2
    if "cc by" in l or "cc-by" in l:
        return 1
    return 3

BATIDAS = {
    "aranha":  ["Phoneutria nigriventer", "Phoneutria"],
    "mata":    ["Mata Atlântica forest", "Atlantic Forest Brazil understory"],
    "banana":  ["Banana bunch harvest", "Banana crate"],
    "lab":     ["Laboratory pipette research", "Antivenom vial"],
    "porto":   ["Container ship port cargo", "Shipping containers port"],
}


def api(url):
    r = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(r, timeout=30, context=CTX))


def limpa(html):
    return re.sub(r"<[^>]+>", "", html or "").strip()[:80]


achados = {}
for chave, termos in BATIDAS.items():
    cands = []
    for termo in termos:
        u = ("https://commons.wikimedia.org/w/api.php?action=query&generator=search"
             f"&gsrsearch={urllib.parse.quote(termo)}&gsrnamespace=6&gsrlimit=14"
             "&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1400&format=json")
        try:
            d = api(u)
        except Exception as e:
            print(f"  ! {termo}: {e}")
            continue
        for p in d.get("query", {}).get("pages", {}).values():
            ii = p["imageinfo"][0]
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "?")
            if not p["title"].lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            if ii["width"] < 900:
                continue
            cands.append({
                "titulo": p["title"].replace("File:", ""),
                "url": ii.get("thumburl") or ii["url"],
                "lic": lic,
                "rank": rank_lic(lic),
                "autor": limpa(em.get("Artist", {}).get("value", "")),
                "pagina": ii.get("descriptionurl", ""),
                "w": ii["width"], "h": ii["height"],
            })
    cands.sort(key=lambda c: (c["rank"], -min(c["w"], 3000)))
    achados[chave] = cands[:4]
    print(f"\n=== {chave} ===")
    for c in cands[:4]:
        print(f"  [{c['lic']}] {c['titulo'][:56]}  — {c['autor'][:40]}")

# baixa o melhor de cada batida
creditos = []
for chave, lista in achados.items():
    for n, c in enumerate(lista[:2]):
        dest = f"{DIR}/{chave}_{n}.jpg"
        try:
            r = urllib.request.Request(c["url"], headers=UA)
            with urllib.request.urlopen(r, timeout=60, context=CTX) as resp, open(dest, "wb") as f:
                f.write(resp.read())
            c["arquivo"] = dest
            creditos.append(c)
            print(f"baixado {chave}_{n}: {os.path.getsize(dest)//1024} KB  [{c['lic']}]")
        except Exception as e:
            print(f"  ! falhou {chave}_{n}: {e}")

json.dump(creditos, open(f"{DIR}/creditos.json", "w"), ensure_ascii=False, indent=1)
print(f"\n{len(creditos)} arquivos | créditos em creditos.json")
