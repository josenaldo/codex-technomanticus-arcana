# ADR-001: YAML como formato intermediário dos cards

## Status

Aceita

## Data

2026-04-12

## Contexto

Os flashcards precisam de um formato intermediário entre a geração (IA) e o build final (.apkg). O formato deve ser legível, editável, versionável com diffs claros no git, e suportar texto multilinha (backs longos, code blocks).

## Alternativas consideradas

1. **JSON** — Estrutura rígida, bom para tooling, mas multilinha é verboso e diffs poluídos
2. **YAML** — Legível, familiar do frontmatter Obsidian, bom para texto multilinha com `|`
3. **Markdown com frontmatter** — Um arquivo por card, máxima consistência com Obsidian, mas gera explosão de arquivos (~800 .md para ~160 notas)
4. **CSV** — Universal para Anki import, mas limitado para HTML/code blocks e sem estrutura hierárquica

## Decisão

YAML, com múltiplos cards agrupados por nota-fonte em um único arquivo.

## Justificativa

- Familiaridade: o vault já usa YAML no frontmatter — mesma linguagem mental
- Multilinha natural: blocos `|` para backs longos e code snippets
- Diffs legíveis: mudança em um card aparece localizada no diff
- Agrupamento coeso: cards da mesma nota ficam juntos, facilitando revisão
- Sem explosão de arquivos: ~160 YAMLs vs ~800 Markdowns

## Consequências

- Scripts de build precisam parsear YAML (pyyaml)
- Editores de YAML podem reclamar de strings multilinha complexas com Markdown embutido
- Campos de texto precisam de escape cuidadoso (`:` no início de linha, por exemplo)
