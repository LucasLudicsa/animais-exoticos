# -*- coding: utf-8 -*-
"""Gera as cartelas sozinho, a partir do texto do roteiro.

As 125 cartelas do primeiro episodio foram escritas a mao, uma a uma. Isso
funciona uma vez; nao funciona tres vezes por dia. Aqui a cartela sai do que
a frase DIZ: escolhe um objeto da biblioteca pelas palavras, escolhe um
arranjo pela semente do episodio, e anima.

Cumpre o mesmo contrato de cenas16.py -- desenha(i, ctx) e SETAS -- entao
entra no renderizador que ja existe sem mexer nele.

    import cenas_auto
    cenas_auto.configura(linhas, "jararaca")
"""
import math
import random
import re

from art2 import (AMARELO, AZUL, BRANCO, CINZA, LARANJA, MARROM, PELE, PRETO,
                  ROSA, VERDE, VERMELHO, aranha, balao_susto, cola, font,
                  menino, pop, suor, texto)
import obj16 as O
import obj_cobra as OC
import variacao

LINHAS = []
ESTILO = None
SETAS = {}

# palavra no roteiro -> como desenhar. A ordem importa: a primeira que casar
# manda, entao o que e mais especifico vem antes.
MAPA = [
    (r"jararaca|cobra|serpente|bothrops|peconhent", "cobra"),
    (r"cascavel", "cascavel"),
    (r"folha seca|folha|mata|capim|chao", "folha"),
    (r"rato|roedor|presa", "rato"),
    (r"remedio|comprimido|captopril|farmac|medicament", "comprimido"),
    (r"pressao|coracao|vaso|sangu", "coracao"),
    (r"soro|antiofidic|ampola|frasco", "frasco"),
    (r"hospital|posto|servico de saude|sus|estrada|distancia|longe", "estrada"),
    (r"veneno|gota|picad|mordid", "gota"),
    (r"por cento|letalidade|cada dez|nove em cada|numero|mil|registr", "numeros"),
    (r"mil novecentos|anos sessenta|ano|1965|1981|epoca|decada", "calendario"),
    (r"nao |nunca|jamais|esquece|torniquete|cortar|chupar", "errado"),
    (r"lava|calmo|erguer|leva|fazer", "certo"),
    (r"bota|calcado|sapato|tenis|pisa", "bota"),
    (r"mao|enfia|buraco|lenha|pedra", "mao"),
    (r"pesquisador|medico|cientista|ferreira|homem|cara|gente|pessoa", "gente"),
    (r"olho|olhar|reparou|identificar|reconhec|cabeca triangular", "lupa"),
    (r"arvore|roca|quintal|casa", "arvore"),
]

NUM = re.compile(r"(\d+[,.]?\d*)\s*(por cento|%)?|nove em cada dez|zero virgula trinta e oito")


def _sem_acento(s):
    tab = str.maketrans("áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ", "aaaaeeiooouucAAAAEEIOOOUUC")
    return s.translate(tab).lower()


def configura(linhas, episodio):
    """linhas = [{'i','ato','texto'}], episodio = nome que define o estilo."""
    global LINHAS, ESTILO
    LINHAS = linhas
    ESTILO = variacao.estilo(episodio)
    return ESTILO


def _assunto(txt):
    t = _sem_acento(txt)
    for padrao, nome in MAPA:
        if re.search(padrao, t):
            return nome
    return "cobra"


# palavras compridas que nao dizem nada. Sem isso o cartaz vira "EXISTE".
VAZIAS = set(_sem_acento(
    "existe quando porque aquilo sobre entre depois ainda muito todos toda todo "
    "coisa outra outro mesma mesmo nessa nesse essas esses desde nunca sempre "
    "agora antes assim onde como qual quais para pelos pelas sendo tinha temos "
    "vamos fazer feito ficar sendo nao sim mais menos cada dela dele deles delas "
    "isso isto aquela aquele voce gente parte lugar jeito forma numero virgula "
    "novecentos oitenta sessenta setenta noventa cinquenta quarenta trinta"
).split())


def _destaque(txt, assunto=None):
    """A palavra do cartaz. Prefere a que casou com o assunto; senao a mais
    comprida que nao esteja na lista de vazias."""
    brutas = [w.strip(".,;:!?\u2014\u2013") for w in txt.split()]
    pal = [w for w in brutas if len(w) > 4 and _sem_acento(w) not in VAZIAS]
    if assunto:
        for padrao, nome in MAPA:
            if nome == assunto:
                for w in pal:
                    if re.search(padrao, _sem_acento(w)):
                        return w.upper()
                break
    return max(pal, key=len).upper() if pal else None


# anos por extenso. O roteiro escreve assim porque a locucao le melhor,
# mas na tela o numero tem que aparecer como numero.
ANOS = [
    ("mil novecentos e oitenta e um", "1981"),
    ("mil novecentos e sessenta e cinco", "1965"),
    ("mil novecentos e setenta e um", "1971"),
    ("anos sessenta", "1960s"),
]


def _numero(txt):
    t = _sem_acento(txt)
    for frase, n in ANOS:
        if frase in t:
            return n
    if "cada dez" in t and "nove" in t:
        return "9 de 10"
    if "trinta e oito" in t:
        return "0,38%"
    if "tres vezes" in t:
        return "3x"
    if "trinta e uma mil" in t or "trinta e um mil" in t:
        return "31.000"
    m = re.search(r"\b(\d{1,3}(?:[.,]\d+)?)\b", txt)
    return m.group(1) if m else None


# ------------------------------------------------------------------ objetos
def _obj(nome, p, cx, cy, tam, s, ac):
    if nome == "cobra":
        OC.cobra(p, cx, cy, tam, s, ondas=2.0)
    elif nome == "cascavel":
        OC.cobra(p, cx, cy, tam, s, ondas=1.5, fill=(170, 150, 110))
    elif nome == "folha":
        OC.folha(p, cx, cy, tam, s)
    elif nome == "rato":
        OC.rato(p, cx, cy, tam * 0.8, s)
    elif nome == "comprimido":
        OC.comprimido(p, cx, cy, tam * 1.0, s)
    elif nome == "estrada":
        OC.estrada(p, cx, cy, tam * 1.5, s)
    elif nome == "coracao":
        O.coracao(p, cx, cy, tam * 0.8, s)
    elif nome == "frasco":
        O.frascoL(p, cx, cy, tam * 1.15, s)
    elif nome == "gota":
        O.gota(p, cx, cy, tam * 0.95, s)
    elif nome == "calendario":
        O.calendario(p, cx, cy, tam * 0.9, s)
    elif nome == "errado":
        O.errado(p, cx, cy, tam * 1.0, s)
    elif nome == "certo":
        O.certo(p, cx, cy, tam * 1.0, s)
    elif nome == "bota":
        O.botaL(p, cx, cy, tam * 0.8, s)
    elif nome == "mao":
        O.mao(p, cx, cy, tam * 0.8, s)
    elif nome == "gente":
        menino(p, cx, cy, tam * 0.9, s, cara="ok")
    elif nome == "lupa":
        O.lupa(p, cx, cy, tam * 1.0, s)
    elif nome == "arvore":
        O.arvore(p, cx, cy, tam, s)
    else:
        OC.cobra(p, cx, cy, tam, s)


def _T(p, txt, x, y, tam, cor, esc=1.0, fonte="marker", max_w=None):
    """Escreve e, se pedirem largura maxima, encolhe ate caber.

    Sem isso "9 DE 10" em corpo 367 saia pela borda direita da tela.
    """
    if esc < 0.02 or not txt:
        return
    tam = max(8, int(tam * esc))
    im = texto(txt, font(fonte, tam), cor, BRANCO, 8)
    if max_w and im.width > max_w:
        tam = max(8, int(tam * max_w / im.width))
        im = texto(txt, font(fonte, tam), cor, BRANCO, 8)
    cola(p.im, im, x, y)


# ------------------------------------------------------------------ arranjos
def desenha(i, c):
    p, t, d, s, ac = c["p"], c["t"], c["d"], c["s"], c["ac"]
    W, H, CY = c["W"], c["H"], c["CY"]
    if i >= len(LINHAS):
        return
    m = LINHAS[i]
    txt = m["texto"]
    assunto = _assunto(txt)
    num = _numero(txt)
    dest = _destaque(txt, assunto)

    r = random.Random((ESTILO["semente"] if ESTILO else 0) + i * 17)
    vertical = H > W
    base = min(W, H)

    # numero na tela ganha de tudo: e o que o espectador leva embora
    if num:
        # metade esquerda pro desenho, metade direita pro numero, sem invadir
        _obj(assunto, p, W * 0.25, CY, base * 0.40, s, ac)
        e = pop(t, 0.10, 0.25)
        _T(p, num, W * 0.71, CY - base * 0.02, int(base * 0.40), ac, e,
           max_w=W * 0.46)
        return

    arranjo = r.choice(["centro", "lado", "par", "cartaz"])
    respira = 1.0 + 0.035 * math.sin(t * 2.1 + i)

    if arranjo == "centro":
        _obj(assunto, p, W * 0.5, CY + base * 0.08, base * 0.72 * respira, s, ac)
        _T(p, dest, W * 0.5, CY - base * 0.34, int(base * 0.15), ac, pop(t, 0.25),
           max_w=W * 0.82)

    elif arranjo == "lado":
        esq = r.random() < 0.5
        ox = W * (0.30 if esq else 0.70)
        _obj(assunto, p, ox, CY, base * 0.56 * respira, s, ac)
        _T(p, dest, W * (0.72 if esq else 0.28), CY, int(base * 0.135), PRETO,
           pop(t, 0.20), max_w=W * 0.40)

    elif arranjo == "par":
        seg = "folha" if assunto == "cobra" else "cobra"
        _obj(assunto, p, W * 0.28, CY + base * 0.04, base * 0.46 * respira, s, ac)
        _obj(seg, p, W * 0.72, CY + base * 0.04, base * 0.42, s + 77, ac)
        _T(p, dest, W * 0.5, CY - base * 0.32, int(base * 0.125), PRETO,
           pop(t, 0.30), max_w=W * 0.80)

    else:  # cartaz: palavra grande, objeto pequeno de apoio
        _T(p, dest, W * 0.5, CY - base * 0.14, int(base * 0.23), ac, pop(t, 0.08),
           max_w=W * 0.88)
        _obj(assunto, p, W * 0.5, CY + base * 0.30, base * 0.36, s, ac)
