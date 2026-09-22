# -*- coding: utf-8 -*-
"""Baixa fotos de licenca livre do Wikimedia Commons por episodio.

busca_fotos.py tinha os termos da armadeira escritos dentro do arquivo. Aqui os
termos vem por episodio, e as fotos caem em fotos/<episodio>/ -- o long e o
short do mesmo episodio usam o MESMO conjunto, que e o que faz o espectador
reconhecer o canal quando ve os dois.

Ordena por licenca: CC0 e dominio publico primeiro, CC BY depois.

    python3 pipeline/busca_fotos_auto.py jararaca
"""
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request

from paths import PIPE

UA = {"User-Agent": "MataDensa/1.0 (educational video; contact: local)"}
CTX = ssl.create_default_context()

TERMOS = {
    "jararaca": {
        "cobra":      ["Bothrops jararaca", "Bothrops jararaca snake"],
        "cobra2":     ["Bothrops atrox", "Bothrops snake Brazil"],
        "chao":       ["leaf litter forest floor", "dry leaves ground forest"],
        "rato":       ["wild rat rodent", "Rattus rattus"],
        "soro":       ["antivenom vial", "Instituto Butantan"],
        "hospital":   ["hospital emergency room", "hospital corridor"],
        "remedio":    ["blister pack pills", "medication tablets"],
        "laboratorio":["laboratory pipette research", "science laboratory flask"],
        "roca":       ["rural worker field Brazil", "sugarcane field worker"],
    },
}


def rank_lic(l):
    l = (l or "").lower()
    if "cc0" in l or "public domain" in l:
        return 0
    if "cc by-sa" in l or "cc-by-sa" in l:
        return 2
    if "cc by" in l or "cc-by" in l:
        return 1
    return 3


def api(url):
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=30, context=CTX))


def limpa(h):
    return re.sub(r"<[^>]+>", "", h or "").strip()[:90]


def busca(episodio):
    batidas = TERMOS[episodio]
    dest_dir = os.path.join(PIPE, "fotos", episodio)
    os.makedirs(dest_dir, exist_ok=True)
    creditos = []
    for chave, termos in batidas.items():
        cands = []
        for termo in termos:
            u = ("https://commons.wikimedia.org/w/api.php?action=query&generator=search"
                 f"&gsrsearch={urllib.parse.quote(termo)}&gsrnamespace=6&gsrlimit=14"
                 "&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1600&format=json")
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
                if ii["width"] < 1000:
                    continue
                cands.append({"chave": chave, "titulo": p["title"].replace("File:", ""),
                              "url": ii.get("thumburl") or ii["url"], "lic": lic,
                              "rank": rank_lic(lic),
                              "autor": limpa(em.get("Artist", {}).get("value", "")),
                              "pagina": ii.get("descriptionurl", ""),
                              "w": ii["width"], "h": ii["height"]})
        cands.sort(key=lambda c: (c["rank"], -min(c["w"], 3000)))
        if not cands:
            print(f"=== {chave}: NADA ENCONTRADO")
            continue
        c = cands[0]
        dest = os.path.join(dest_dir, f"{chave}.jpg")
        try:
            r = urllib.request.Request(c["url"], headers=UA)
            with urllib.request.urlopen(r, timeout=60, context=CTX) as resp, open(dest, "wb") as f:
                f.write(resp.read())
            c["arquivo"] = dest
            creditos.append(c)
            print(f"{chave:<12} [{c['lic']:<14}] {c['titulo'][:46]}")
        except Exception as e:
            print(f"  ! falhou {chave}: {e}")
    json.dump(creditos, open(os.path.join(dest_dir, "creditos.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"\n{len(creditos)} fotos em {dest_dir}")
    return creditos


if __name__ == "__main__":
    busca(sys.argv[1])
