# -*- coding: utf-8 -*-
"""Faz cada episodio parecer e soar diferente do anterior.

A politica de conteudo inautentico do YouTube mira o que parece feito com
template. Como o renderizador e o mesmo todo dia, a diferenca precisa ser
gerada de proposito: uma semente por episodio decide a paleta, o contraste,
a granulacao, a vinheta, o conjunto de transicoes, o par tipografico e ate
a curva de energia da locucao.

Mesma semente, mesmo visual -- da para reproduzir um episodio. Sementes
diferentes nunca caem no mesmo conjunto, porque as escolhas saem de listas
embaralhadas e nao de sorteios independentes.

    python3 pipeline/variacao.py jararaca
    python3 pipeline/variacao.py jararaca --json
"""
import argparse
import colorsys
import hashlib
import json
import random

TRANSICOES = [
    "corte_seco", "chicote", "rabisco", "mancha_tinta", "dobra_papel",
    "zoom_estalo", "varredura", "piscada", "rasgo", "empurrao",
    "giro_tosco", "queima", "persiana", "pingo", "tremor",
]

OVERLAYS = [
    ("granulado", "ruido fino, como papel de jornal"),
    ("papel", "textura de caderno com fibras"),
    ("linhas", "risco horizontal de tv velha"),
    ("vinheta_suja", "cantos escurecidos e irregulares"),
    ("mancha_luz", "vazamento de luz num canto"),
    ("meio_tom", "pontilhado de impressao barata"),
    ("poeira", "sujeira e cabelos de scanner"),
]

TIPOGRAFIA = [
    ("Marker.ttf", "Hand.ttf"),
    ("Hand.ttf", "Marker.ttf"),
    ("Marker.ttf", "SplineSans.ttf"),
    ("Bricolage.ttf", "Hand.ttf"),
]

# (nome, matiz base 0-1, saturacao, luz de fundo)
PALETAS = [
    ("caderno", 0.12, 0.35, 0.94), ("giz", 0.58, 0.28, 0.16),
    ("jornal", 0.09, 0.10, 0.90), ("neon_barato", 0.78, 0.65, 0.12),
    ("mata", 0.30, 0.45, 0.88), ("alerta", 0.03, 0.70, 0.93),
    ("agua", 0.52, 0.40, 0.91), ("terra", 0.07, 0.40, 0.89),
]


HISTORICO = "roteiros/estilos_usados.json"
JANELA = 4   # nenhum episodio repete paleta/tipografia dos 4 anteriores


def _historico():
    try:
        return json.load(open(HISTORICO, encoding="utf-8"))
    except Exception:
        return []


def registra(e):
    """Guarda o estilo usado, para que os proximos episodios se afastem dele."""
    h = _historico()
    h = [x for x in h if x["episodio"] != e["episodio"]]
    h.append({"episodio": e["episodio"], "paleta": e["paleta"]["nome"],
              "tipografia": e["tipografia"]["titulo"]})
    json.dump(h[-20:], open(HISTORICO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def estilo(episodio, evitar_recentes=True):
    """Estilo completo de um episodio, deterministico pelo nome.

    Com evitar_recentes, paleta e tipografia dos ultimos JANELA episodios ficam
    fora do sorteio -- dois videos seguidos nunca saem parecidos.
    """
    semente = int(hashlib.sha256(episodio.encode()).hexdigest()[:12], 16)
    r = random.Random(semente)

    pal_proibidas, tipo_proibidos = set(), set()
    if evitar_recentes:
        for x in _historico()[-JANELA:]:
            if x["episodio"] != episodio:
                pal_proibidas.add(x["paleta"])
                tipo_proibidos.add(x["tipografia"])

    disp = [p for p in PALETAS if p[0] not in pal_proibidas] or PALETAS
    pal = r.choice(disp)
    nome_pal, matiz, sat, luz = pal
    escuro = luz < 0.5

    # 3 a 5 transicoes por episodio, sempre um conjunto diferente
    baralho = TRANSICOES[:]
    r.shuffle(baralho)
    trans = baralho[: r.randint(3, 5)]

    tipo_disp = [x for x in TIPOGRAFIA if x[0] not in tipo_proibidos] or TIPOGRAFIA
    _par_tipo = r.choice(tipo_disp)   # um PAR, nao duas escolhas soltas

    ovl = OVERLAYS[:]
    r.shuffle(ovl)
    overlays = [o[0] for o in ovl[: r.randint(1, 2)]]

    # grade de cor: quanto mais forte, mais o episodio se distingue
    grade = {
        "contraste": round(r.uniform(1.05, 1.35), 3),
        "saturacao": round(r.uniform(0.85, 1.45), 3),
        "brilho": round(r.uniform(-0.04, 0.06), 3),
        "gama": round(r.uniform(0.88, 1.12), 3),
        "temperatura": round(r.uniform(-0.12, 0.12), 3),  # <0 frio, >0 quente
        "vinheta": round(r.uniform(0.0, 0.45), 3),
        "grao": round(r.uniform(2.0, 11.0), 1),
    }

    # curva de energia da locucao: comeca alto, cede, sobe no fim
    pico_ini = round(r.uniform(0.62, 0.78), 2)
    vale = round(r.uniform(0.42, 0.55), 2)
    pico_fim = round(r.uniform(0.60, 0.80), 2)

    cor = lambda h, s, v: "#%02x%02x%02x" % tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))
    return {
        "episodio": episodio,
        "semente": semente,
        "paleta": {
            "nome": nome_pal,
            "fundo": cor(matiz, 0.06 if not escuro else 0.35, luz),
            "traco": "#111111" if not escuro else "#f2f2f2",
            "destaque": cor((matiz + 0.5) % 1.0, min(sat + 0.25, 1.0), 0.85 if not escuro else 0.95),
            "apoio": cor((matiz + 0.08) % 1.0, sat, 0.75),
            "escuro": escuro,
        },
        "transicoes": trans,
        "overlays": overlays,
        "tipografia": dict(zip(("titulo", "corpo"), _par_tipo)),
        "grade": grade,
        "energia": {"abertura": pico_ini, "meio": vale, "fecho": pico_fim,
                    "cfg": round(r.uniform(0.32, 0.52), 2)},
    }


def filtro_ffmpeg(e):
    """Traduz a grade de cor num filtro -vf do ffmpeg."""
    g = e["grade"]
    t = g["temperatura"]
    partes = [
        f"eq=contrast={g['contraste']}:saturation={g['saturacao']}"
        f":brightness={g['brilho']}:gamma={g['gama']}",
    ]
    if abs(t) > 0.01:
        rg, bg = 1 + t * 0.5, 1 - t * 0.5
        partes.append(f"colorbalance=rm={t:.3f}:bm={-t:.3f}")
    if g["vinheta"] > 0.05:
        partes.append(f"vignette=a={g['vinheta']:.3f}")
    if g["grao"] > 1:
        partes.append(f"noise=alls={int(g['grao'])}:allf=t+u")
    return ",".join(partes)


def energia_da_fala(e, i, total):
    """Exagero da locucao na posicao i de total falas: alto, cede, sobe."""
    en = e["energia"]
    p = i / max(total - 1, 1)
    if p < 0.18:
        v = en["abertura"]
    elif p > 0.82:
        v = en["fecho"]
    else:
        q = (p - 0.18) / 0.64
        v = en["meio"] + (en["abertura"] - en["meio"]) * abs(0.5 - q) * 0.7
    r = random.Random(e["semente"] + i)
    return round(min(max(v + r.uniform(-0.05, 0.05), 0.3), 0.9), 2), en["cfg"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("episodio")
    p.add_argument("--json", action="store_true")
    p.add_argument("--registrar", action="store_true", help="grava no historico de estilos")
    a = p.parse_args()
    e = estilo(a.episodio)
    if a.registrar:
        registra(e)
    if a.json:
        print(json.dumps(e, ensure_ascii=False, indent=1))
        return
    print(f"\n=== estilo de '{a.episodio}' (semente {e['semente']}) ===\n")
    pal = e["paleta"]
    print(f"paleta      {pal['nome']}  fundo {pal['fundo']}  traco {pal['traco']}  destaque {pal['destaque']}")
    print(f"tipografia  titulo {e['tipografia']['titulo']}  corpo {e['tipografia']['corpo']}")
    print(f"transicoes  {', '.join(e['transicoes'])}")
    print(f"overlays    {', '.join(e['overlays'])}")
    print(f"grade       {e['grade']}")
    print(f"\nfiltro ffmpeg:\n  {filtro_ffmpeg(e)}")
    print("\nenergia da locucao (exagero por posicao):")
    for i in range(0, 10):
        exa, cfg = energia_da_fala(e, i, 10)
        print(f"  fala {i+1}/10  exagero {exa}  cfg {cfg}")


if __name__ == "__main__":
    main()
