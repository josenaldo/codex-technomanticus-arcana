# Codex Technomanticus Arcana — Design Spec

## Contexto

O Codex Technomanticus é um grimório digital pessoal de engenharia de software — um vault Obsidian com ~161 notas organizadas por domínio (Fundamentos, Arquitetura, Java, JavaScript, IA, Infraestrutura, etc.) seguindo o padrão Interview Note com seções bilíngues (PT-BR + inglês técnico).

O objetivo deste projeto é criar um sistema de flashcards Anki derivado do conteúdo do vault, permitindo estudo por repetição espaçada dos conceitos documentados nas notas.

## Objetivos

1. Gerar flashcards de qualidade a partir das notas do vault, usando IA (Claude) para criar cards inteligentes
2. Manter os cards em formato editável e versionado (YAML) no repositório `codex-technomanticus-arcana`
3. Publicar decks `.apkg` via GitHub Releases para que qualquer usuário do Anki possa baixar e usar
4. Fornecer skills para o Claude Code que automatizem o fluxo de detecção de notas alteradas, geração de cards e validação

## Não-objetivos

- Sincronização automática vault → cards (o cardeamento é sempre deliberado, invocado pelo usuário)
- Geração mecânica/template-based de cards (a IA gera conteúdo, não apenas extrai)
- Suporte a outros SRS além do Anki nesta versão

---

## 1. Arquitetura Geral

### Três repos, três responsabilidades

| Repo | Responsabilidade | Conteúdo |
|------|-----------------|----------|
| `codex-technomanticus` | Vault de conhecimento (fonte) | Notas Obsidian (.md) |
| `codex-technomanticus-arcana` | Cartas arcanas (derivado) | Cards YAML + scripts de build + CI/CD |
| `codex-technomanticus-site` | Publicação web (derivado) | Quartz site |

### Fluxo de trabalho

```
LOCAL (Claude Code)                          CI/CD (GitHub Actions)
┌─────────────────────────┐                  ┌──────────────────────┐
│ 1. Usuário invoca skill │                  │ Push no repo arcana  │
│                         │                  │         │            │
│ 2. detect_changes.py    │                  │         ▼            │
│    encontra notas       │                  │ validate_cards.py    │
│    alteradas            │                  │         │            │
│         │               │                  │         ▼            │
│ 3. IA lê notas e gera   │   commit/push   │ build_deck.py        │
│    cards YAML           │ ──────────────▶  │ (YAML → .apkg)      │
│         │               │                  │         │            │
│ 4. Constraint valida    │                  │         ▼            │
│         │               │                  │ GitHub Release       │
│ 5. Usuário revisa       │                  │ (publica .apkg)      │
│    e faz commit         │                  └──────────────────────┘
└─────────────────────────┘
```

Separação clara: ambiente criativo (local/IA) vs ambiente mecânico (CI/CD). O cardeamento nunca é disparado automaticamente — é sempre deliberado.

### Detecção de mudanças

Dois mecanismos complementares:

- **`.last-carding`** — Arquivo no repo arcana com o commit hash do vault na última execução. O `detect_changes.py` compara com `HEAD` do vault para listar notas alteradas/adicionadas desde então. Simples, versionado, sem dependência externa.
- **`source_hash`** — Hash MD5 do conteúdo da nota no momento da geração, armazenado no YAML. Permite detectar se uma nota mudou mesmo sem o `.last-carding` (fallback, ou para reprocessar notas específicas).

---

## 2. Formato dos Cards YAML

### Estrutura de arquivo

Cada arquivo YAML agrupa os cards de uma nota-fonte. Nomeação espelha o vault: `Fundamentos/Algoritmos.md` → `cards/fundamentos/algoritmos.yaml`.

```yaml
# Metadados do grupo
source: "Fundamentos/Algoritmos.md"
source_hash: "a1b2c3d4"
deck: "Codex::Fundamentos"
generated: "2026-04-12"
tags:
  - fundamentos
  - entrevista

# Cards
cards:
  # Conceito (frente/verso)
  - id: fund-algo-001
    type: basic
    front: "O que é complexidade de tempo (time complexity)?"
    back: |
      Medida de como o tempo de execução de um algoritmo cresce
      em função do tamanho da entrada (n).

      Expressa em notação **Big O** — descreve o pior caso.
    tags: [algoritmos, complexidade]

  # Cloze (preenchimento de lacuna)
  - id: fund-algo-002
    type: cloze
    text: |
      A busca binária tem complexidade {{c1::O(log n)}} porque
      divide o espaço de busca pela {{c2::metade}} a cada iteração.
    tags: [algoritmos, busca]

  # Vocabulário bilíngue
  - id: fund-algo-003
    type: vocab
    term_pt: "Complexidade de tempo"
    term_en: "Time complexity"
    definition: |
      How the running time of an algorithm grows as a function
      of the input size. Expressed using Big O notation.
    usage: |
      "The time complexity of this solution is O(n log n)
      because we sort the array first."
    tags: [algoritmos, vocabulario]

  # Cenário/aplicação
  - id: fund-algo-004
    type: scenario
    situation: |
      Você precisa buscar um elemento em uma lista ordenada
      de 1 milhão de itens.
    question: "Qual algoritmo usar e qual a complexidade?"
    answer: |
      **Busca binária** — O(log n).
      Em 1M de itens, no máximo ~20 comparações.
      Busca linear seria O(n) = 1M comparações no pior caso.
    tags: [algoritmos, busca]

  # Armadilha
  - id: fund-algo-005
    type: pitfall
    trap: "Usar busca binária em lista não ordenada"
    why: |
      Busca binária assume que os dados estão ordenados.
      Em lista desordenada, o resultado é incorreto silenciosamente
      — não dá erro, só retorna a resposta errada.
    prevention: "Sempre validar ou garantir ordenação antes de aplicar."
    tags: [algoritmos, armadilhas]
```

### Tipos de card

| Tipo | Campos obrigatórios | Origem na nota |
|------|---------------------|----------------|
| `basic` | front, back | "O que é", "Como funciona", "Quando usar" |
| `cloze` | text (com `{{c1::...}}`) | Qualquer seção, fatos-chave |
| `vocab` | term_pt, term_en, definition, usage | "Key vocabulary" |
| `scenario` | situation, question, answer | "Quando usar", "Na prática" |
| `pitfall` | trap, why, prevention | "Armadilhas comuns" |

### Regras de ID

- Prefixo do domínio: `fund-`, `arq-`, `java-`, `js-`, `infra-`, `ia-`, `aprend-`
- Slug da nota: `algo`, `spring`, `react`
- Sequencial: `001`, `002`
- Exemplo: `fund-algo-001`, `java-spring-003`

### Renderização HTML

O `build_deck.py` converte Markdown dos campos para HTML. Suporte a bold/italic, code blocks (`<pre><code>`), e listas.

---

## 3. Skills

### Visão geral

```
arcana-forge (meta-skill)
    │
    ├── invoca detect_changes.py
    ├── para cada nota alterada:
    │   ├── invoca arcana-cards (gera cards)
    │   └── invoca arcana-constraint (valida)
    └── relatório final
```

### 3.1 arcana-cards (micro-skill)

**Responsabilidade:** Recebe uma nota (path ou conteúdo) e gera cards YAML.

**Fluxo:**
1. Lê a nota Markdown
2. Identifica seções (O que é, Como funciona, Key vocabulary, etc.)
3. Gera cards usando IA — escolhendo o tipo adequado por seção
4. Se já existir YAML para essa nota, faz merge (preserva IDs, atualiza conteúdo, adiciona novos)
5. Escreve o YAML no repo arcana

**Regras de geração:**
- Mínimo 3, máximo ~15 cards por nota (depende da profundidade)
- Cards atômicos — 1 conceito por card
- Back/answer com no máximo ~50 palavras
- Pelo menos 1 card de vocab se a nota tiver "Key vocabulary"
- Pelo menos 1 cloze por nota
- IDs sequenciais seguindo o padrão do domínio

### 3.2 arcana-deck (micro-skill)

**Responsabilidade:** Gera o `.apkg` a partir dos YAMLs. Wrapper do `build_deck.py`.

**Fluxo:**
1. Coleta todos os YAMLs de `cards/`
2. Invoca `build_deck.py`
3. Reporta: quantos cards, quantos decks, path do `.apkg`

**Uso:** Preview local antes do CI. Não é o caminho principal.

### 3.3 arcana-forge (meta-skill)

**Responsabilidade:** Coordena o fluxo completo para um diretório ou conjunto de notas.

**Fluxo:**
1. Roda `detect_changes.py` apontando para o vault + `.last-carding`
2. Apresenta lista de notas alteradas/novas ao usuário
3. Para cada nota: invoca `arcana-cards` + `arcana-constraint`
4. Corrige falhas de validação automaticamente
5. Atualiza `.last-carding`
6. Apresenta relatório final

**Interação típica:**
```
Usuário: "gere cards das notas recentes"
Claude: [invoca arcana-forge]
  → 3 notas alteradas desde último cardeamento
  → gera cards para cada uma
  → valida
  → "Gerados 27 cards para 3 notas: Algoritmos (9), Spring Boot (12), Docker (6).
     Todos passaram na validação. Pronto para commit."
```

### 3.4 arcana-constraint (constraint-skill)

**Responsabilidade:** Valida se os cards seguem boas práticas.

**Regras:**

| Regra | Critério |
|-------|----------|
| Atomicidade | 1 conceito por card, back ≤ 50 palavras |
| Sem ambiguidade | Front deve ter resposta clara e única |
| Cloze bem formado | `{{c1::...}}` presente, máx 2 clozes por card |
| Vocab completo | term_pt + term_en + definition preenchidos |
| Sem duplicatas | Sem cards com front/text idêntico no mesmo deck |
| IDs válidos | Seguem padrão `domínio-slug-NNN` |
| Tags presentes | Pelo menos 1 tag por card |
| Scenario completo | situation + question + answer preenchidos |

**Output:** Lista de violações com card ID, regra e sugestão de correção. Retorna OK/FAIL.

### Localização das skills

```
~/.agents/skills/
├── arcana-cards/
│   └── skill.md
├── arcana-deck/
│   └── skill.md
├── arcana-forge/
│   ├── skill.md
│   └── detect_changes.py
├── arcana-constraint/
│   └── skill.md
└── obsidian-markdown/          ← já instalada (kepano)
```

---

## 4. CI/CD e Distribuição

### Pipeline

```
Push na main
    │
    ▼
┌─────────────────────────────┐
│ 1. Validação                │
│    python validate_cards.py │
│    (falha = bloqueia build) │
├─────────────────────────────┤
│ 2. Build                    │
│    python build_deck.py     │
│    → Codex-Technomanticus.apkg │
├─────────────────────────────┤
│ 3. Release                  │
│    Se tag vX.Y.Z:           │
│    → GitHub Release + .apkg │
│                             │
│    Se push normal:          │
│    → artefato do workflow   │
└─────────────────────────────┘
```

### Versionamento

- **Patch** (v1.0.X): correções de cards existentes
- **Minor** (v1.X.0): novos cards adicionados
- **Major** (vX.0.0): reestruturação de decks ou mudança de formato

### Para outros usuários

1. Ir em Releases do repo
2. Baixar `Codex-Technomanticus.apkg`
3. Anki → File → Import
4. Atualização: importar nova release por cima — Anki faz merge por ID, preservando progresso

---

## 5. Estrutura do Repo

```
codex-technomanticus-arcana/
├── cards/                          ← YAMLs por domínio
│   ├── fundamentos/
│   ├── arquitetura/
│   ├── java/
│   ├── javascript/
│   ├── infraestrutura/
│   ├── ia/
│   └── aprendizado/
├── scripts/
│   ├── build_deck.py               ← YAML → .apkg via genanki
│   └── validate_cards.py           ← validação mecânica (CI gate)
├── templates/
│   └── card_styles.css             ← estilos dos cards no Anki
├── dist/                           ← gitignored, output do build
├── docs/
│   ├── specs/                      ← este documento
│   └── adrs/                       ← decisões de arquitetura
├── .last-carding                   ← commit hash do último cardeamento
├── .github/
│   └── workflows/
│       └── build-release.yaml
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 6. Organização dos Decks

Hierarquia rasa por domínio, espelhando a estrutura do vault:

```
Codex
├── Codex::Fundamentos
├── Codex::Arquitetura
├── Codex::Java
├── Codex::JavaScript
├── Codex::Infraestrutura
├── Codex::IA
└── Codex::Aprendizado
```

Tags do Anki complementam com metadados: tipo de card, fase da trilha, tópico específico.

---

## 7. Dependências

```toml
[project]
name = "codex-technomanticus-arcana"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "genanki>=0.13",
    "pyyaml>=6.0",
    "markdown>=3.5",
]
```

---

## 8. Pré-requisitos

- Python 3.10+
- Anki (para testar decks localmente)
- Claude Code (para invocar skills de geração)
