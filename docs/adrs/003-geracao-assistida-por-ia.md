# ADR-003: Geração de cards assistida por IA

## Status

Aceita

## Data

2026-04-12

## Contexto

As notas do vault seguem uma estrutura padronizada (Interview Note template) com seções como "O que é", "Como funciona", "Armadilhas comuns", "Key vocabulary". É possível extrair cards mecanicamente (regex/template), usar IA para gerar cards inteligentes, ou combinar ambos.

## Alternativas consideradas

1. **Extração mecânica** — Script parseia seções e gera cards por template. Rápido e barato, mas cards genéricos e sem cloze deletions inteligentes
2. **Assistida por IA** — Claude lê a nota, entende o conteúdo, gera cards com cloze positioning, perguntas contextuais e respostas concisas. Mais tokens, mas qualidade superior
3. **Híbrido** — Mecânico para vocabulary, IA para cloze/cenários

## Decisão

Geração assistida por IA (opção 2), com a IA rodando localmente via Claude Code.

## Justificativa

- Cards de qualidade exigem compreensão do conteúdo (onde colocar um cloze, que cenário criar)
- A skill `arcana-cards` já roda no Claude Code — o agente tem capacidade de leitura e geração
- A constraint-skill (`arcana-constraint`) garante que os cards sigam boas práticas independente de quem gerou
- O formato YAML intermediário permite revisão humana antes do commit
- Custo de tokens é aceitável: ~160 notas processadas incrementalmente, não de uma vez

## Consequências

- Geração depende do Claude Code (não roda em CI)
- Resultado pode variar entre execuções (não-determinístico) — mitigado pela constraint-skill
- Notas futuras podem ser processadas por API de IA quando disponível, sem mudar a arquitetura
