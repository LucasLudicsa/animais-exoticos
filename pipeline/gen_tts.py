# -*- coding: utf-8 -*-
import os
from paths import WORK, OUT
import asyncio, edge_tts, os, json


OUT = f"{WORK}/tts"
VOZ = "pt-BR-AntonioNeural"

# (ato, rate edge-tts, pausa depois da linha em s)
ATOS = {
 "1 GANCHO":   ("-34%", 0.80),
 "2 ORIGEM":   ("+7%",  0.34),
 "3 ESCALA":   ("+7%",  0.36),
 "4 CONCRETO": ("-5%",  0.46),
 "5 PAVOR":    ("+20%", 0.22),
 "6 PROVA":    ("+11%", 0.28),
 "7 VIRADA":   ("+7%",  0.36),
 "8 TESE":     ("-8%",  0.56),
}

LINHAS = [
 ("1 GANCHO",   "Armadeira. Foneutria nigriventer."),
 ("2 ORIGEM",   "A aranha mais venenosa do mundo não mora na Austrália."),
 ("2 ORIGEM",   "Mora aqui. Ela não tece teia, não espera."),
 ("2 ORIGEM",   "Ela caça a pé, no escuro, no chão da Mata Atlântica."),
 ("3 ESCALA",   "O veneno é uma neurotoxina que trava os nervos."),
 ("3 ESCALA",   "Seis microgramas bastam para matar um camundongo."),
 ("4 CONCRETO", "Um grão de sal pesa sessenta microgramas."),
 ("4 CONCRETO", "A dose cabe num décimo de um grão de sal."),
 ("5 PAVOR",    "O nome vem do que ela faz quando é encurralada."),
 ("5 PAVOR",    "Ela não foge. Ela se arma."),
 ("5 PAVOR",    "Levanta as duas primeiras pernas, expõe as presas,"),
 ("5 PAVOR",    "e avança na direção da ameaça."),
 ("5 PAVOR",    "Nenhuma outra aranha faz isso."),
 ("6 PROVA",    "Por isso o acidente quase sempre acontece dentro de casa."),
 ("6 PROVA",    "No sapato. Atrás da cortina. No cacho de banana."),
 ("6 PROVA",    "São cerca de quatro mil casos por ano no Brasil."),
 ("6 PROVA",    "E como ela viaja escondida em carga de fruta,"),
 ("6 PROVA",    "já apareceu em portos da Europa."),
 ("7 VIRADA",   "Quase todo caso termina em dor e soro antiaracnídico."),
 ("7 VIRADA",   "Mas em parte das vítimas apareceu um efeito que ninguém previu."),
 ("7 VIRADA",   "O veneno abria os vasos sanguíneos, e o efeito durava horas."),
 ("8 TESE",     "Pesquisadores brasileiros isolaram a molécula."),
 ("8 TESE",     "Hoje ela está em teste clínico como remédio."),
 ("8 TESE",     "A aranha mais venenosa do mundo virou farmácia."),
]

# legenda queimada (texto mostrado) pode diferir da fala (grafia fonetica)
LEGENDA = {0: "Armadeira.\nPhoneutria nigriventer."}

async def main():
    os.makedirs(OUT, exist_ok=True)
    meta = []
    for i, (ato, txt) in enumerate(LINHAS):
        rate, pausa = ATOS[ato]
        mp3 = f"{OUT}/{i:02d}.mp3"
        c = edge_tts.Communicate(txt, VOZ, rate=rate, pitch="-6Hz")
        await c.save(mp3)
        meta.append({"i": i, "ato": ato, "texto": txt,
                     "legenda": LEGENDA.get(i, txt), "rate": rate, "pausa": pausa})
        print(f"{i:02d} {ato:<12} {rate:>5} {os.path.getsize(mp3):>7}B  {txt[:52]}")
    json.dump(meta, open(f"{OUT}/meta.json","w"), ensure_ascii=False, indent=1)

asyncio.run(main())
