# -*- coding: utf-8 -*-
"""Banco de temas: escolhe o que gravar, garantindo variedade.

A politica de conteudo inautentico do YouTube mira repeticao e formato de
template. A defesa nao e so visual: os tres videos de um mesmo dia nao podem
ser tres versoes do mesmo video. Por isso a escolha diaria e forcada a pegar
CATEGORIAS DIFERENTES, e temas de risco alto nunca saem no automatico.

    python3 pipeline/temas.py dia              # sugere os 3 de hoje
    python3 pipeline/temas.py lista --categoria veneno_remedio
    python3 pipeline/temas.py usar jararaca    # marca como usado
    python3 pipeline/temas.py saldo            # quanto banco ainda resta
"""
import argparse
import datetime as dt
import json
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(AQUI, "banco_temas.json")
USADOS = os.path.join(os.path.dirname(AQUI), "roteiros", "usados.json")

POR_DIA = 3


def carrega():
    return json.load(open(BANCO, encoding="utf-8"))


def usados():
    if os.path.isfile(USADOS):
        return json.load(open(USADOS, encoding="utf-8"))
    return {}


def salva_usados(u):
    os.makedirs(os.path.dirname(USADOS), exist_ok=True)
    json.dump(u, open(USADOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def disponiveis(d, u, incluir_alto=False):
    out = []
    for t in d["temas"]:
        if t["id"] in u or t.get("status") == "PUBLICADO":
            continue
        if t["risco"] == "alto" and not incluir_alto:
            continue
        out.append(t)
    return out


def escolhe_dia(d, u, data, n=POR_DIA, incluir_alto=False):
    """Sorteio deterministico pela data, com categorias obrigatoriamente distintas."""
    pool = disponiveis(d, u, incluir_alto)
    if not pool:
        return []
    r = random.Random(f"{data}")
    # prioriza o que esta marcado PROXIMO, depois sorteia
    pool.sort(key=lambda t: (t.get("status") != "PROXIMO", r.random()))
    escolhidos, cats = [], set()
    for t in pool:
        if t["categoria"] in cats:
            continue
        escolhidos.append(t)
        cats.add(t["categoria"])
        if len(escolhidos) == n:
            break
    # se o banco ficou estreito demais pra 3 categorias, completa como der
    if len(escolhidos) < n:
        for t in pool:
            if t not in escolhidos:
                escolhidos.append(t)
            if len(escolhidos) == n:
                break
    return escolhidos


def imprime(t, i=None):
    cab = f"{i}. " if i else ""
    print(f"{cab}[{t['categoria']}] {t['titulo']}   (risco {t['risco']})")
    print(f"   gancho: {t['gancho']}")
    print(f"   virada: {t['virada']}")
    print(f"   CHECAR: {t['checar']}")
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pd = sub.add_parser("dia", help="sugere os temas de um dia")
    pd.add_argument("--data", default=dt.date.today().isoformat())
    pd.add_argument("--n", type=int, default=POR_DIA)
    pd.add_argument("--incluir-alto", action="store_true", help="inclui temas de risco alto")

    pl = sub.add_parser("lista")
    pl.add_argument("--categoria")
    pl.add_argument("--risco")

    pu = sub.add_parser("usar")
    pu.add_argument("id")

    sub.add_parser("saldo")

    a = p.parse_args()
    d, u = carrega(), usados()

    if a.cmd == "dia":
        esc = escolhe_dia(d, u, a.data, a.n, a.incluir_alto)
        print(f"\n=== {a.data} — {len(esc)} temas ===\n")
        for i, t in enumerate(esc, 1):
            imprime(t, i)
        print("Nada foi marcado como usado. Confirme com: temas.py usar <id>")
        return

    if a.cmd == "lista":
        for t in d["temas"]:
            if a.categoria and t["categoria"] != a.categoria:
                continue
            if a.risco and t["risco"] != a.risco:
                continue
            marca = "x" if t["id"] in u or t.get("status") == "PUBLICADO" else " "
            print(f"[{marca}] {t['id']:22} {t['categoria']:16} {t['titulo']}")
        return

    if a.cmd == "usar":
        alvo = [t for t in d["temas"] if t["id"] == a.id]
        if not alvo:
            raise SystemExit(f"tema desconhecido: {a.id}")
        u[a.id] = dt.date.today().isoformat()
        salva_usados(u)
        print(f"marcado: {a.id}")
        return

    if a.cmd == "saldo":
        total = len(d["temas"])
        livres = disponiveis(d, u)
        alto = [t for t in d["temas"] if t["risco"] == "alto" and t["id"] not in u]
        print(f"banco: {total} temas")
        print(f"livres (risco baixo/medio): {len(livres)}")
        print(f"retidos por risco alto: {len(alto)}")
        dias = len(livres) // POR_DIA
        print(f"\na {POR_DIA}/dia isso cobre {dias} dias (~{dias/30:.1f} meses)")
        if dias < 30:
            print("ATENCAO: menos de um mes de banco. Amplie antes de comecar a publicar.")
        from collections import Counter
        print("\npor categoria (livres):")
        for c, n in Counter(t["categoria"] for t in livres).most_common():
            print(f"  {c:18} {n}")


if __name__ == "__main__":
    main()
