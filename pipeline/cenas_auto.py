# -*- coding: utf-8 -*-
"""Cartelas que MOSTRAM o que a narracao esta dizendo.

A primeira versao pegava uma palavra-chave da frase, jogava UM objeto no meio
da tela e parava ali. O resultado repetia, nao se mexia, e sobretudo nao
ilustrava: a voz dizia "ela quer o rato do seu quintal" e a tela mostrava uma
cobra sozinha, parada.

Aqui a frase vira uma CENA:
  - todos os conceitos da frase entram, nao so o primeiro
  - eles ganham uma RELACAO -- seta de um pro outro, um em cima do outro,
    um X carimbado por cima, comparacao lado a lado, queda
  - tudo entra em tempos diferentes dentro da fala, entao a tela nunca fica
    quatro segundos igual
  - o mesmo objeto nunca aparece em duas cartelas seguidas do mesmo jeito
  - onde existe foto de verdade, a foto entra no lugar do desenho

Contrato igual ao de cenas16.py: configura(), desenha(i, ctx), SETAS.
"""
import math
import random
import re

from art2 import (AMARELO, AZUL, BRANCO, CINZA, LARANJA, MARROM, PELE, PRETO,
                  ROSA, VERDE, VERMELHO, aranha, cola, font, menino, pop, seta,
                  suor, texto)
import obj16 as O
import obj_cobra as OC
import variacao

LINHAS = []
ESTILO = None
SETAS = {}
_ULTIMO = {}          # i -> conceito principal, para nao repetir seguido

MAPA = [
    (r"jararaca|bothrops|serpente|\bcobra\b|peconhent", "cobra"),
    (r"cascavel|crotal", "cascavel"),
    (r"folha seca|folha|capim|mato|chao|entulho|lenha", "folha"),
    (r"rato|roedor|presa", "rato"),
    (r"captopril|remedio|comprimido|medicament|farmac", "comprimido"),
    (r"pressao|coracao|vaso|sangu|circul", "coracao"),
    (r"soro|antiofidic|ampola|frasco|veneno", "frasco"),
    (r"hospital|posto|servico de saude|\bsus\b|atendiment", "hospital"),
    (r"estrada|distancia|longe|demora|chegar", "estrada"),
    (r"picad|mordid|presa|gota", "gota"),
    (r"laboratori|pesquisa|ferreira|cientist|estud|descobr|publica", "laboratorio"),
    (r"roca|quintal|lavoura|trabalhador rural|campo|fazenda", "roca"),
    (r"ano|1965|1981|decada|epoca|sessenta|oitenta", "calendario"),
    (r"bota|calcado|sapato|tenis|pisa", "bota"),
    (r"\bmao\b|enfia|buraco|pedra", "mao"),
    (r"medico|homem|cara|pessoa|gente|voce|alguem|vitima", "gente"),
    (r"olho|olhar|reparou|identificar|reconhec|ver\b", "lupa"),
    (r"arvore|mata|floresta", "arvore"),
]

# conceito -> arquivo em fotos/<episodio>/
FOTO_DE = {
    "cobra": "cobra2", "cascavel": "cobra", "folha": "chao", "rato": "rato",
    "comprimido": "remedio", "frasco": "soro", "hospital": "hospital",
    "laboratorio": "laboratorio", "roca": "roca", "arvore": "chao",
}

ESCALA = {
    "cobra": 1.00, "cascavel": 1.00, "folha": 1.05, "rato": 0.95,
    "comprimido": 1.15, "estrada": 1.45, "coracao": 1.75, "frasco": 1.55,
    "gota": 1.70, "calendario": 1.30, "errado": 0.85, "certo": 0.85,
    "bota": 1.45, "mao": 1.70, "gente": 1.25, "lupa": 1.40, "arvore": 1.20,
    "hospital": 1.30, "laboratorio": 1.30, "roca": 1.25,
}

VAZIAS = set(
    "existe quando porque aquilo sobre entre depois ainda muito todos toda todo "
    "coisa outra outro mesma mesmo nessa nesse essas esses desde nunca sempre "
    "agora antes assim onde como qual quais para pelos pelas sendo tinha temos "
    "vamos fazer feito ficar nao sim mais menos cada dela dele deles delas "
    "isso isto aquela aquele voce gente parte lugar jeito forma numero virgula "
    "novecentos oitenta sessenta setenta noventa cinquenta quarenta trinta "
    "quase apenas sobre ninguem alguem".split())

ANOS = [("mil novecentos e oitenta e um", "1981"),
        ("mil novecentos e sessenta e cinco", "1965"),
        ("mil novecentos e setenta e um", "1971"),
        ("anos sessenta", "ANOS 60")]


def _sa(s):
    return s.translate(str.maketrans("áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ",
                                     "aaaaeeiooouucAAAAEEIOOOUUC")).lower()


def configura(linhas, episodio):
    global LINHAS, ESTILO, _ULTIMO
    LINHAS = linhas
    ESTILO = variacao.estilo(episodio)
    _ULTIMO = {}
    return ESTILO


def _conceitos_pos(txt):
    """[(posicao, conceito)] na ordem em que aparecem na frase."""
    t = _sa(txt)
    achados, vistos = [], set()
    for padrao, nome in MAPA:
        m = re.search(padrao, t)
        if m and nome not in vistos:
            vistos.add(nome)
            achados.append((m.start(), nome))
    achados.sort()
    return achados


def _conceitos(txt):
    return [n for _, n in _conceitos_pos(txt)]


VERBO_ALVO = re.compile(r"\bquer\b|\bcaca\b|procura|atras de|vai atras")


def _alvo(txt):
    """O que vem DEPOIS do verbo. Em "ela quer o rato do seu quintal" o alvo e
    o rato; pegar o ultimo conceito dava "quintal", que desenha uma pessoa."""
    t = _sa(txt)
    ms = list(VERBO_ALVO.finditer(t))
    if not ms:
        return None
    # a frase costuma ter a negativa antes da afirmativa:
    # "nao QUER voce. Ela QUER o rato" -- o alvo esta depois da ULTIMA.
    m = ms[-1]
    for pos, nome in _conceitos_pos(txt):
        if pos > m.end():
            return nome
    return None


def _numero(txt):
    t = _sa(txt)
    for f, n in ANOS:
        if f in t:
            return n
    if "cada dez" in t and "nove" in t:
        return "9 de 10"
    if "trinta e oito" in t:
        return "0,38%"
    if "tres vezes" in t:
        return "3x"
    if "trinta e uma mil" in t or "trinta e um mil" in t:
        return "31 MIL"
    if "noventa virgula cinco" in t:
        return "90,5%"
    m = re.search(r"\b(\d{1,4}(?:[.,]\d+)?)\b", txt)
    return m.group(1) if m else None


def _relacao(txt):
    t = _sa(txt)
    if re.search(r"\bnao (amarr|corta|fura|queim|espreme|chupa|poe|bebe|enfia|deixa)|"
                 r"nunca|torniquete|garrote|esquece isso", t):
        return "nega"
    if re.search(r"tres vezes|mais que|menos que|maior que|em vez de|nao e .* e ", t):
        return "compara"
    if re.search(r"\bquer\b|\bcaca\b|procura|atras de|vai atras", t):
        return "alvo"
    if re.search(r"em cima de|deitada|no chao|embaixo|sob ", t):
        return "sobre"
    if re.search(r"derrub|\bcai\b|baixa|abaixa|despenca|relaxa", t):
        return "queda"
    return None


def _destaque(txt, conceitos):
    brutas = [w.strip(".,;:!?—–\"'") for w in txt.split()]
    pal = [w for w in brutas if len(w) > 4 and _sa(w) not in VAZIAS]
    for padrao, nome in MAPA:
        if conceitos and nome == conceitos[0]:
            for w in pal:
                if re.search(padrao, _sa(w)):
                    return w.upper()
            break
    return max(pal, key=len).upper() if pal else None


def _obj(nome, p, cx, cy, tam, s, ac, var=0):
    tam = tam * ESCALA.get(nome, 1.0)
    if nome in ("cobra", "cascavel"):
        OC.cobra(p, cx, cy, tam, s,
                 ondas=[2.0, 1.5, 2.6, 1.2][var % 4],
                 cabeca_erguida=(var % 3 == 1),
                 boca=1.0 if var % 3 == 2 else 0.0,
                 fill=OC.BEGE if nome == "cobra" else (170, 150, 110))
    elif nome == "folha":
        for k in range(3):
            OC.folha(p, cx + (k - 1) * tam * 0.42, cy + (k % 2) * tam * 0.12,
                     tam * 0.62, s + k * 7)
    elif nome == "rato":
        OC.rato(p, cx, cy, tam * 0.8, s)
    elif nome == "comprimido":
        for k in range(2):
            OC.comprimido(p, cx + (k - 0.5) * tam * 0.5, cy + (k - 0.5) * tam * 0.3,
                          tam * 0.55, s + k * 5)
    elif nome in ("estrada", "hospital"):
        OC.estrada(p, cx, cy, tam * 1.4, s)
    elif nome == "coracao":
        O.coracao(p, cx, cy, tam * 0.8, s)
    elif nome in ("frasco", "laboratorio"):
        O.frascoL(p, cx, cy, tam * 0.9, s)
    elif nome == "gota":
        O.gota(p, cx, cy, tam * 0.7, s)
    elif nome == "calendario":
        O.calendario(p, cx, cy, tam * 0.9, s)
    elif nome == "errado":
        O.errado(p, cx, cy, tam * 0.6, s)
    elif nome == "certo":
        O.certo(p, cx, cy, tam * 0.6, s)
    elif nome == "bota":
        O.botaL(p, cx, cy, tam * 0.8, s)
    elif nome == "mao":
        O.mao(p, cx, cy, tam * 0.8, s)
    elif nome == "gente":
        menino(p, cx, cy, tam * 0.9, s, cara="ok", bob=0.0)
    elif nome == "roca":
        O.arvore(p, cx - tam * 0.26, cy, tam * 0.75, s)
        OC.folha(p, cx + tam * 0.30, cy + tam * 0.22, tam * 0.42, s + 4)
    elif nome == "lupa":
        O.lupa(p, cx, cy, tam * 0.8, s)
    elif nome == "arvore":
        O.arvore(p, cx, cy, tam, s)
    else:
        OC.cobra(p, cx, cy, tam, s)


def _T(p, txt, x, y, tam, cor, esc=1.0, fonte="marker", max_w=None):
    if esc < 0.02 or not txt:
        return
    tam = max(8, int(tam * esc))
    im = texto(txt, font(fonte, tam), cor, BRANCO, 8)
    if max_w and im.width > max_w:
        im = texto(txt, font(fonte, max(8, int(tam * max_w / im.width))), cor, BRANCO, 8)
    cola(p.im, im, x, y)


def desenha(i, c):
    p, t, d, s, ac = c["p"], c["t"], c["d"], c["s"], c["ac"]
    W, H, CY = c["W"], c["H"], c["CY"]
    foto, tem_foto = c["foto"], c.get("tem_foto", lambda n: False)
    if i >= len(LINHAS):
        return
    txt = LINHAS[i]["texto"]
    base = min(W, H)
    prog = min(1.0, t / max(d, 0.01))

    conc = _conceitos(txt)
    num = _numero(txt)
    rel = _relacao(txt)
    r = random.Random((ESTILO["semente"] if ESTILO else 0) + i * 17)

    # nunca o mesmo objeto principal que a cartela anterior
    ant = _ULTIMO.get(i - 1)
    if conc and len(conc) > 1 and conc[0] == ant:
        conc = conc[1:] + conc[:1]
    principal = conc[0] if conc else "cobra"
    secundario = conc[1] if len(conc) > 1 else None
    # Em "ela QUER o rato", o alvo e o ultimo conceito citado, nao o segundo.
    # Com conc = [cobra, gente, rato] a seta apontava para "voce" -- o oposto
    # do que a frase diz.
    if rel == "alvo":
        alvo = _alvo(txt)
        if alvo:
            secundario = alvo
    _ULTIMO[i] = principal
    var = (s // 37 + i) % 4

    # deriva continua: nada fica parado
    dx = math.sin(t * 1.3 + i) * base * 0.012
    dy = math.cos(t * 1.1 + i * 2) * base * 0.010
    respira = 1.0 + 0.045 * math.sin(t * 2.2 + i)

    # ---------- foto a cada poucas cartelas, quando existe ----------
    # Foto so quando ela REALMENTE ilustra a frase:
    #  - nunca numa proibicao: ali o que tem que aparecer e o X sobre o desenho
    #    (antes, "nao amarra torniquete" puxava a foto do laboratorio porque a
    #     palavra "veneno" estava na frase -- imagem solta, exatamente o que o
    #     episodio 1 foi criticado por ter)
    #  - so quando o conceito da foto e o PRIMEIRO da frase, isto e, o assunto
    #  - e espacada, senao vira album de fotos com legenda
    nome_foto = FOTO_DE.get(principal)
    usa_foto = (nome_foto and tem_foto(nome_foto)
                and rel not in ("nega", "compara", "queda")
                and conc and conc[0] == principal
                and i % 3 == 2)
    if usa_foto:
        foto(nome_foto, cx=W * 0.5 + dx * 0.4, cy=CY + dy * 0.4)
        dest = _destaque(txt, conc)
        _T(p, dest, W * 0.5, CY - base * 0.36, int(base * 0.12), ac,
           pop(t, 0.35), max_w=W * 0.8)
        if num:
            _T(p, num, W * 0.74, CY + base * 0.30, int(base * 0.20), ac,
               pop(t, 0.55), max_w=W * 0.4)
        return

    # ---------- numero manda ----------
    if num:
        _obj(principal, p, W * 0.26 + dx, CY + dy, base * 0.40 * respira, s, ac, var)
        _T(p, num, W * 0.71, CY - base * 0.02, int(base * 0.40), ac,
           pop(t, 0.12, 0.25), max_w=W * 0.46)
        return

    # ---------- relacoes ----------
    if rel == "nega":
        _obj(principal, p, W * 0.5 + dx, CY + dy, base * 0.50 * respira, s, ac, var)
        if t > d * 0.42:                       # o X carimba DEPOIS, nao junto
            e = pop(t, d * 0.42, 0.20)
            p.xis(W * 0.5, CY, base * 0.30 * e, VERMELHO, int(base * 0.045), s + 3)
        _T(p, _destaque(txt, conc), W * 0.5, CY - base * 0.36,
           int(base * 0.12), VERMELHO, pop(t, 0.15), max_w=W * 0.82)
        return

    if rel == "compara" and secundario:
        _obj(principal, p, W * 0.27 + dx, CY + dy, base * 0.40 * respira, s, ac, var)
        if t > d * 0.30:
            _obj(secundario, p, W * 0.73, CY, base * 0.38, s + 77, ac, var + 1)
        _T(p, "X", W * 0.5, CY, int(base * 0.13), CINZA, pop(t, d * 0.25))
        _T(p, _destaque(txt, conc), W * 0.5, CY - base * 0.34,
           int(base * 0.11), ac, pop(t, 0.20), max_w=W * 0.8)
        return

    if rel == "alvo" and secundario:
        _obj(principal, p, W * 0.24 + dx, CY + dy, base * 0.40 * respira, s, ac, var)
        if t > d * 0.28:
            _obj(secundario, p, W * 0.76, CY, base * 0.34, s + 55, ac, var + 2)
        if t > d * 0.48:                        # a seta se desenha
            pr = min(1.0, (t - d * 0.48) / max(d * 0.30, 0.01))
            seta(p, W * 0.40, CY - base * 0.05, W * 0.63, CY - base * 0.05,
                 ac, s + 9, int(base * 0.016), pr, 0.25)
        _T(p, _destaque(txt, conc), W * 0.5, CY - base * 0.34,
           int(base * 0.11), ac, pop(t, 0.18), max_w=W * 0.8)
        return

    if rel == "sobre" and secundario:
        _obj(secundario, p, W * 0.5, CY + base * 0.20, base * 0.50, s + 33, ac, var + 1)
        if t > d * 0.25:
            e = pop(t, d * 0.25, 0.25)
            _obj(principal, p, W * 0.5 + dx, CY - base * 0.06 - (1 - e) * base * 0.18,
                 base * 0.44 * respira, s, ac, var)
        _T(p, _destaque(txt, conc), W * 0.5, CY - base * 0.36,
           int(base * 0.11), ac, pop(t, 0.20), max_w=W * 0.8)
        return

    if rel == "queda":
        _obj(principal, p, W * 0.32 + dx, CY + dy, base * 0.42 * respira, s, ac, var)
        if t > d * 0.35:
            pr = min(1.0, (t - d * 0.35) / max(d * 0.35, 0.01))
            seta(p, W * 0.64, CY - base * 0.24, W * 0.64,
                 CY - base * 0.24 + base * 0.42 * pr, VERMELHO, s + 11,
                 int(base * 0.020), 1.0, 0.05)
        _T(p, _destaque(txt, conc), W * 0.5, CY - base * 0.36,
           int(base * 0.12), ac, pop(t, 0.15), max_w=W * 0.8)
        return

    # ---------- sem relacao: dois objetos entrando em tempos diferentes ----------
    if secundario:
        _obj(principal, p, W * 0.30 + dx, CY + dy, base * 0.44 * respira, s, ac, var)
        if t > d * 0.32:
            e = pop(t, d * 0.32, 0.22)
            _obj(secundario, p, W * 0.71, CY + base * 0.04 * (1 - e),
                 base * 0.38 * e, s + 41, ac, var + 3)
        _T(p, _destaque(txt, conc), W * 0.5, CY - base * 0.34,
           int(base * 0.115), ac, pop(t, 0.22), max_w=W * 0.8)
    else:
        _obj(principal, p, W * 0.5 + dx, CY + base * 0.06 + dy,
             base * 0.62 * respira, s, ac, var)
        _T(p, _destaque(txt, conc), W * 0.5, CY - base * 0.34,
           int(base * 0.145), ac, pop(t, 0.20), max_w=W * 0.84)
