# -*- coding: utf-8 -*-
"""Quando publicar. Tres posts por dia, em horarios que nunca se repetem.

Publicar 09:00, 13:00 e 19:00 todo santo dia e um padrao de robo. A agenda
aqui sorteia horarios diferentes a cada dia, respeitando uma folga minima de
4 horas entre posts e mantendo tudo dentro da janela em que gente brasileira
esta acordada.

O sorteio e deterministico pela data: rodar duas vezes da o mesmo resultado,
entao a agenda pode ser recalculada sem bagunçar o que ja foi programado.

    python3 pipeline/agenda.py dia
    python3 pipeline/agenda.py semana --de 2026-09-23
    python3 pipeline/agenda.py semana --com-temas
"""
import argparse
import datetime as dt
import hashlib
import json
import random

POR_DIA = 3
FOLGA_MIN_H = 4.0        # exigencia do usuario: nunca menos que isso
JANELA = (8.0, 22.5)     # horario de Brasilia
PRIMEIRO_ATE = 12.0      # o primeiro post sai ate meio-dia


def _rnd(data):
    s = int(hashlib.sha256(f"agenda:{data}".encode()).hexdigest()[:12], 16)
    return random.Random(s)


def horarios(data, n=POR_DIA):
    """n horarios no dia, espacados por pelo menos FOLGA_MIN_H."""
    r = _rnd(data)
    ini, fim = JANELA
    # espaco livre depois de reservar as folgas minimas
    folga_total = FOLGA_MIN_H * (n - 1)
    sobra = (fim - ini) - folga_total
    if sobra < 0:
        raise SystemExit(f"janela curta demais para {n} posts com {FOLGA_MIN_H}h de folga")

    # distribui a sobra em n+1 pedacos aleatorios (inicio, entre, fim)
    cortes = sorted(r.uniform(0, sobra) for _ in range(n))
    ts = []
    for i, c in enumerate(cortes):
        ts.append(ini + c + FOLGA_MIN_H * i)
    # nao deixa o primeiro cair tarde demais
    if ts[0] > PRIMEIRO_ATE:
        desloca = ts[0] - PRIMEIRO_ATE
        ts = [t - desloca for t in ts]
    return [round(t, 3) for t in ts]


def hhmm(h):
    m = int(round(h * 60))
    return f"{m//60:02d}:{m%60:02d}"


def dia(data, com_temas=False, n=POR_DIA):
    ts = horarios(data, n)
    itens = [{"hora": hhmm(t), "h": t} for t in ts]
    if com_temas:
        try:
            import temas
            d, u = temas.carrega(), temas.usados()
            esc = temas.escolhe_dia(d, u, data, n)
            for it, t in zip(itens, esc):
                it["tema"] = t["id"]
                it["titulo"] = t["titulo"]
                it["categoria"] = t["categoria"]
        except Exception as ex:
            print(f"  (sem temas: {ex})")
    return itens


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pd = sub.add_parser("dia")
    pd.add_argument("--data", default=dt.date.today().isoformat())
    pd.add_argument("--com-temas", action="store_true")
    ps = sub.add_parser("semana")
    ps.add_argument("--de", default=dt.date.today().isoformat())
    ps.add_argument("--dias", type=int, default=7)
    ps.add_argument("--com-temas", action="store_true")
    a = p.parse_args()

    if a.cmd == "dia":
        itens = dia(a.data, a.com_temas)
        print(f"\n{a.data}")
        for it in itens:
            extra = f"  {it['titulo']}" if "titulo" in it else ""
            print(f"  {it['hora']}{extra}")
        return

    d0 = dt.date.fromisoformat(a.de)
    print(f"\n{'data':<12}{'posts':<28}{'folgas'}")
    tudo = {}
    for k in range(a.dias):
        data = (d0 + dt.timedelta(days=k)).isoformat()
        itens = dia(data, a.com_temas)
        hs = [it["h"] for it in itens]
        folgas = [f"{hs[i+1]-hs[i]:.1f}h" for i in range(len(hs) - 1)]
        print(f"{data:<12}{' '.join(it['hora'] for it in itens):<28}{' '.join(folgas)}")
        tudo[data] = itens
    json.dump(tudo, open("roteiros/agenda.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # confere que nenhum horario se repete entre dias
    from collections import Counter
    c = Counter(it["hora"] for v in tudo.values() for it in v)
    rep = [h for h, n in c.items() if n > 1]
    print(f"\nhorarios repetidos na semana: {rep if rep else 'nenhum'}")
    menor = min(v[i+1]["h"] - v[i]["h"] for v in tudo.values() for i in range(len(v) - 1))
    print(f"menor folga observada: {menor:.2f}h (exigido {FOLGA_MIN_H}h)")


if __name__ == "__main__":
    main()
