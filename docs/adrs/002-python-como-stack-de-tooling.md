# ADR-002: Python como stack de tooling

## Status

Aceita

## Data

2026-04-12

## Contexto

O projeto precisa de scripts para build (YAML → .apkg), validação de cards, e detecção de notas alteradas. O repo do site usa Node/TypeScript (Quartz), então havia a opção de manter consistência de stack.

## Alternativas consideradas

1. **Python** — `genanki` é a lib padrão e madura para gerar .apkg, ecossistema forte para parsing de texto
2. **Node/TypeScript** — Consistente com o site, mas sem lib equivalente ao genanki tão madura
3. **Híbrido** — Node para orquestração, Python só para o build final

## Decisão

Python puro para todo o tooling.

## Justificativa

- `genanki` é a ferramenta certa para o job — madura, bem mantida, API simples
- Python é excelente para processamento de Markdown/YAML (pyyaml, markdown)
- O repo arcana é independente do site — não precisa de consistência de stack
- Benefício adicional: exercitar Python como linguagem secundária do autor
- Menos complexidade que híbrido (um runtime, um gerenciador de deps)

## Consequências

- CI precisa de setup-python no workflow
- Desenvolvedores que quiserem contribuir precisam de Python 3.10+
- Sem compartilhamento de código com o site (aceitável — são domínios diferentes)
