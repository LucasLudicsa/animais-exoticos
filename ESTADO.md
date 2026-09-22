# Onde paramos — 22/09/2026, 18:45

## Canal

- YouTube: **@matadensa** (conta de marca, e-mail lucas.ludicsa99@gmail.com)
  País Brasil · "não é conteúdo para crianças" ✅ · telefone verificado ✅ · 2FA ✅
  Arte do canal gerada por `pipeline/marca.py` (olhos na folhagem), já publicada.
- TikTok: conta criada, **username ainda é `lucasludicsa7`** — trocar para
  `matadensa`. Só pode ser trocado 1x a cada 30 dias. Nome e bio ainda vazios.
  Não dá para linkar o YouTube ainda: conta nova não tem essa opção.

## Episódio 2 (jararaca) — ENTREGUE, mas NÃO aprovado

    out/jararaca.LONGO.16x9.mp4    9min22s  1920x1080   656 MB
    out/jararaca.LONGO.LEVE.mp4    9min22s  1280x720    106 MB
    out/jararaca.SHORT.9x16.mp4    1min47s  1080x1920   114 MB
    out/jararaca.SHORT.LEVE.mp4    1min47s   720x1280    17 MB

Roteiro conferido em `roteiros/jararaca.FONTES.md` (todo número tem link).
9 fotos de licença livre em `pipeline/fotos/jararaca/`.

## O QUE ESTÁ ERRADO E PRECISA SER RESOLVIDO

1. **Metade das cartelas ainda não ilustra a narração.** Auditoria das 86 falas:
   20 sem nenhum conceito, 25 com um só, 57 sem relação. Frases abstratas
   ("e aqui eu preciso ser honesto com você") não têm objeto para desenhar, e
   o casamento por palavra-chave nunca vai resolver isso.
   **Correção proposta (não feita):** parar de fazer 1 cartela por fala. Agrupar
   falas em BLOCOS de 2–4 que compartilham um conceito, uma ilustração forte por
   bloco, segurando enquanto a legenda muda embaixo. Fala sem conceito herda a
   imagem do bloco em vez de inventar uma ruim. Foto entra na troca de bloco.
2. **Arquivos pesados demais.** 656 MB no longo e 114 MB num short de 1min47.
   `-tune grain` PIOROU (era 299 MB antes) — ele preserva o grão em vez de
   descartar. Correção: baixar `noise=alls` na grade (variacao.py) ou tirar o
   grão do filtro e deixar o x264 em crf 23 sem tune.
3. **Short saiu com 1min47, não 90s.** As pausas de `timeline_auto.py` inflaram.
   Apertar as pausas ou cortar 2–3 falas do roteiro do short.
4. **Rótulos pegam verbo, não sujeito** ("PRECISO", "DESCOBRIR", "MACHUCA").
   `_destaque()` escolhe a palavra mais longa fora da lista de vazias.
5. **PENDENTE DESDE O EPISÓDIO 1: revisão do trecho de primeiros socorros por
   profissional de saúde.** Vale para os dois episódios. Não publicar antes.

## Decisões já tomadas (não reabrir)

- Voz: clone da própria voz do Lucas, Chatterbox local (MIT, R$0).
  Ajustes travados em `pipeline/voz_config.json`: cfg 0.30, exagero 0.65,
  timbre −2 semitons. Referência: `work/refs/leve_00.wav` (10s do minuto 0).
  YouTube dispensa rótulo de IA para clone da própria voz.
- Formato: 90s no short (TikTok só paga acima de 1min; Shorts aceita até 3min).
- 3 vídeos/dia, 3 animais diferentes, horários sorteados com folga ≥4h
  (`pipeline/agenda.py`).
- **Perseguir o YPP pelo long-form antes de 01/02/2027**, quando o limiar dobra
  para 8.000 horas / 20M views. Entrar no programa ANTES dessa data trava o
  limiar atual. Revisão leva ~1 mês, então inscrever até dezembro/2026.

## Próximo passo imediato

Refazer as cartelas por BLOCO (item 1), corrigir peso (item 2) e duração do
short (item 3). Só então re-renderizar. O banco de temas tem 18 dias de
conteúdo — ampliar antes de começar a publicar.
