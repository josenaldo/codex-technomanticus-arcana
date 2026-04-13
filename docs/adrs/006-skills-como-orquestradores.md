# ADR-006: Skills como orquestradores com scripts auxiliares

## Status

Aceita

## Data

2026-04-12

## Contexto

O projeto precisa de 4 skills para o Claude Code (arcana-cards, arcana-deck, arcana-forge, arcana-constraint). As skills podem conter toda a lógica (prompt-only) ou delegar trabalho mecânico para scripts.

## Alternativas consideradas

1. **Skills puras** — Toda lógica no prompt. Simples, mas lento para operações mecânicas e impossível de rodar fora do Claude
2. **Skills + scripts robustos** — Skills orquestram, scripts fazem trabalho pesado (parsing, validação, build). Cada peça faz uma coisa
3. **CLI Python completa + skills como wrappers** — CLI é o centro, skills são finas. Máxima reutilização, mas over-engineering

## Decisão

Skills como orquestradores (opção 2). Scripts auxiliares vivem junto das skills que os usam (`detect_changes.py` em `arcana-forge/`) ou no repo arcana quando têm duplo uso (`validate_cards.py` no CI e invocável pela constraint-skill).

## Justificativa

- A IA é essencial para gerar cards de qualidade — não dá para automatizar tudo em scripts
- Detecção de mudanças (git diff) e validação de regras são operações mecânicas que scripts fazem melhor e mais rápido
- Scripts junto das skills: ferramentas do agente ficam com o agente
- Scripts no repo arcana: ferramentas de build ficam com o build
- Se no futuro quiser escalar para CLI, os scripts já são a base

## Consequências

- Scripts de skills vivem em `~/.agents/skills/arcana-*/`
- Scripts de build vivem em `codex-technomanticus-arcana/scripts/`
- `validate_cards.py` tem duplo uso: invocado pela constraint-skill (local) e pelo CI
- Atualizar uma skill não exige commit no repo arcana e vice-versa
