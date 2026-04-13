# ADR-004: Separação entre ambiente criativo (local) e mecânico (CI)

## Status

Aceita

## Data

2026-04-12

## Contexto

O sistema precisa de dois tipos de operação: geração inteligente de cards (requer IA) e build do deck .apkg (conversão mecânica YAML → binário). Esses dois processos poderiam rodar no mesmo ambiente ou serem separados.

## Alternativas consideradas

1. **Tudo local** — Skills geram cards E buildam .apkg, CI apenas publica
2. **Tudo CI** — Push no vault dispara IA + build automaticamente
3. **Local para criação, CI para build** — IA gera YAMLs localmente, CI converte em .apkg e publica

## Decisão

Separação clara: criação local (Claude Code) + build/release no CI (GitHub Actions).

## Justificativa

- O cardeamento é deliberado — o usuário decide quando e quais notas processar
- A IA precisa de interação (revisão, feedback) — não faz sentido em CI
- Build do .apkg é determinístico e não precisa de IA — perfeito para CI
- Espelha o modelo mental de "escrever código (local) vs deploy (CI)"
- O CI funciona como gate de qualidade: validação antes do build

## Consequências

- O fluxo exige dois passos conscientes: gerar cards (local) + push (dispara CI)
- Não há geração automática de cards — se o usuário esquecer, as notas ficam sem cards
- O .apkg sempre reflete o estado commitado dos YAMLs (source of truth)
