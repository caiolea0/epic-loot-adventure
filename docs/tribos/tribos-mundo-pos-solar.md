---
name: tribos-mundo-pos-solar
description: "Direção de mundo nova (Caio, 10/10): pós-apocalipse solar, 3% sobreviventes, dominar infraestrutura abandonada dá lucro. Amostras visuais em docs/tribos/guia-visual.html."
metadata:
  node_type: memory
  type: project
  modified: 2026-10-10
---

# TRIBOS — Mundo pós-solar (direção proposta, 10/10)

## A premissa

Uma labareda solar queimou a Terra e matou **97% da população**. Os **3%** que sobraram estavam
abrigados ou tiveram sorte. O meio ambiente e a vida animal foram atingidos em cheio: plantas e
bichos voltaram errados, e parte dos humanos mutou.

Tudo que o velho mundo construiu ficou de pé e abandonado: **fábricas, bunkers, aeroportos, usinas,
pátios ferroviários**. Quem domina uma dessas estruturas lucra, porque passa a negociar com os
assentamentos dos 3% — em boa parte **NPCs e IAs que jogam o jogo junto com os jogadores**.

## O que isso muda no desenho

| Ponto | Consequência |
|---|---|
| **A cidade é farmada, não construída à mão** | O jogador escolhe um tipo de cidade (ex.: uma que produz muito metal, com água encanada), farma o custo, recebe o aviso, escolhe a região no mapa e ela sobe num **template padrão** que só muda detalhe conforme o nível |
| **Build deixa de ser o foco** | Com PvP por **lanes** (referência League of Legends), construir peça por peça perde importância diante do confronto |
| **Exploração é solitária** | Andando no mapa o jogador vê a cidade dos outros e as dungeons, mas **não encontra outros jogadores** |
| **O confronto é assíncrono** | Atacou a cidade ou a fábrica de alguém: o dono é notificado e **defende manualmente**, ou a defesa roda **automática** se ele estiver fora |
| **Tropas são variadas e estranhas** | Animais, coisas robóticas, sucata viva — detalhar depois |

A cidade precisa ser **harmônica com o cenário**, lida tanto nas câmeras de primeira e terceira
pessoa quanto no mapa.

## Amostras visuais

**[docs/tribos/guia-visual.html](guia-visual.html)** — arquivo único, abre no navegador, 40 amostras
em 10 painéis: 4 direções de arte comparadas no mesmo conteúdo, 8 cidades (com progressão de nível
visível), 8 personagens e criaturas, 4 cenários, 4 quadros de mapa e confronto.

Geradas com GPT Image dirigido por `gpt-5.6-luna` em esforço médio. Pipeline em `art/concept/`:
`concepts.json` descreve cada quadro, `generate.py` gera, `build_guide.py` monta a página.

## O que precisa ser decidido

1. **Qual direção de arte** (A low-poly refinado / B pintado à mão / C cel-shaded / D realismo sujo).
   Decide custo de produção e quanto a arte envelhece.
2. **Como o nível aparece na cidade**: mais estrutura (chaminés, guindastes, torres) ou melhor
   material no mesmo volume.
3. **Quanto de rosto o personagem mostra** — máscara e capuz facilitam variedade e envelhecem melhor.
4. **Até onde vai a mutação** — hoje está em "crescimento errado", não em monstro de fantasia.

## Relação com o que existe

O jogo atual é protótipo visual. Esta direção **substitui** o visual, não as mecânicas: progressão,
coleta, combate, acampamentos e a base persistente continuam valendo. A base da Fase 3 (claim no
grid, perímetro, estágios) encaixa aqui como "dominar uma estrutura abandonada".
