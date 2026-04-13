# ADR-005: Organização de decks por domínio

## Status

Aceita

## Data

2026-04-12

## Contexto

O Anki suporta hierarquia de decks via separador `::` (ex: `Codex::Fundamentos::Algoritmos`). Os cards poderiam ser organizados por fase da trilha de estudo, por domínio do vault, por tipo de card, ou uma combinação.

## Alternativas consideradas

1. **Por fase da trilha** — `Codex::Fase 1`, `Codex::Fase 3`. Segue ordem de estudo, mas acopla ao roadmap
2. **Por domínio/pasta** — `Codex::Fundamentos`, `Codex::Java`. Espelha o vault, intuitivo
3. **Por tipo de card** — `Codex::Conceitos`, `Codex::Vocabulário`. Agrupa por natureza, mas fragmenta domínios
4. **Híbrido domínio + tipo** — `Codex::Fundamentos::Conceitos`. Máxima granularidade, mas muitos sub-decks

## Decisão

Organização por domínio com hierarquia rasa (máximo 2 níveis), usando tags do Anki para metadados complementares (fase, tipo de card).

## Justificativa

- Espelha a estrutura do vault — mapa mental consistente entre Obsidian e Anki
- Hierarquia rasa evita fragmentação (poucos cards por sub-deck prejudica o SRS)
- Tags permitem filtrar por fase ou tipo sem criar sub-decks
- Intuitivo para navegação: "quero estudar Java" → abrir deck Java
- Simples para outros usuários que baixarem o .apkg

## Consequências

- Decks resultantes: `Codex::Fundamentos`, `Codex::Arquitetura`, `Codex::Java`, `Codex::JavaScript`, `Codex::Infraestrutura`, `Codex::IA`, `Codex::Aprendizado`
- Se o vault ganhar novos domínios, novos decks são criados automaticamente
- Usuários não conseguem filtrar por fase apenas pela hierarquia de decks — precisam usar tags ou filtered decks
