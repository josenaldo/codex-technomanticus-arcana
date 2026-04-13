# Codex Technomanticus Arcana — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Anki flashcard generation system — repo setup, Python scripts, Claude Code skills, and CI/CD pipeline.

**Architecture:** Three-layer system: (1) Skills in `~/.agents/skills/arcana-*` orchestrate card generation via Claude Code, (2) Python scripts in the `codex-technomanticus-arcana` repo handle validation and .apkg build, (3) GitHub Actions CI/CD validates, builds, and releases decks. Cards live as YAML files organized by domain.

**Tech Stack:** Python 3.12, genanki, PyYAML, markdown, GitHub Actions

**Spec:** `docs/specs/2026-04-12-arcana-design.md`

**ADRs:** `docs/adrs/001-006`

---

## File Map

### Repo: `~/repos/personal/codex-technomanticus-arcana/`

| File | Responsibility | Task |
|------|---------------|------|
| `pyproject.toml` | Project metadata + dependencies | 1 |
| `requirements.txt` | Pinned deps for CI | 1 |
| `.gitignore` | Ignore dist/, __pycache__, .venv/ | 1 |
| `.last-carding` | Vault commit hash of last card generation | 1 |
| `cards/` (7 subdirs) | Empty domain directories | 1 |
| `README.md` | User-facing docs for Anki users | 1 |
| `scripts/__init__.py` | Package marker | 2 |
| `scripts/models.py` | YAML schema: dataclasses for cards, deck metadata | 2 |
| `scripts/validate_cards.py` | Validate YAML files against rules | 3 |
| `scripts/build_deck.py` | YAML → .apkg via genanki | 4 |
| `templates/card_styles.css` | Anki card HTML/CSS styles | 4 |
| `tests/test_models.py` | Tests for YAML parsing | 2 |
| `tests/test_validate.py` | Tests for validation rules | 3 |
| `tests/test_build.py` | Tests for deck building | 4 |
| `tests/fixtures/valid_sample.yaml` | Sample YAML for tests | 2 |
| `tests/fixtures/invalid_sample.yaml` | Invalid YAML for validation tests | 3 |
| `.github/workflows/build-release.yaml` | CI/CD pipeline | 5 |

### Skills: `~/.agents/skills/`

| File | Responsibility | Task |
|------|---------------|------|
| `arcana-cards/SKILL.md` | Micro-skill: nota → cards YAML | 6 |
| `arcana-constraint/SKILL.md` | Constraint: validate cards | 7 |
| `arcana-deck/SKILL.md` | Micro-skill: wrap build_deck.py | 8 |
| `arcana-forge/SKILL.md` | Meta-skill: orchestrate full flow | 9 |
| `arcana-forge/detect_changes.py` | Script: find changed vault notes | 9 |

---

## Task 1: Repo Scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `.last-carding`
- Create: `README.md`
- Create: `cards/fundamentos/.gitkeep`
- Create: `cards/arquitetura/.gitkeep`
- Create: `cards/java/.gitkeep`
- Create: `cards/javascript/.gitkeep`
- Create: `cards/infraestrutura/.gitkeep`
- Create: `cards/ia/.gitkeep`
- Create: `cards/aprendizado/.gitkeep`

- [ ] **Step 1: Initialize git repo**

```bash
cd ~/repos/personal/codex-technomanticus-arcana
git init
```

- [ ] **Step 2: Create pyproject.toml**

```toml
[project]
name = "codex-technomanticus-arcana"
version = "0.1.0"
description = "Anki flashcard decks generated from the Codex Technomanticus vault"
requires-python = ">=3.10"
license = "MIT"
dependencies = [
    "genanki>=0.13",
    "pyyaml>=6.0",
    "markdown>=3.5",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
]
```

- [ ] **Step 3: Create requirements.txt**

```
genanki==0.13.1
PyYAML==6.0.1
Markdown==3.5.2
pytest==8.3.5
pytest-cov==5.0.0
```

Run `pip install genanki` to ensure it's available locally (PyYAML and Markdown are already installed):

```bash
pip install genanki
```

- [ ] **Step 4: Create .gitignore**

```
dist/
__pycache__/
*.pyc
.venv/
*.egg-info/
.pytest_cache/
htmlcov/
*.apkg
```

- [ ] **Step 5: Create .last-carding**

This file will be empty initially. The first run of `arcana-forge` will populate it with the vault's current HEAD commit hash.

```
```

- [ ] **Step 6: Create card directories with .gitkeep**

```bash
mkdir -p cards/{fundamentos,arquitetura,java,javascript,infraestrutura,ia,aprendizado}
touch cards/{fundamentos,arquitetura,java,javascript,infraestrutura,ia,aprendizado}/.gitkeep
mkdir -p scripts tests/fixtures templates dist
```

- [ ] **Step 7: Create README.md**

```markdown
# Codex Technomanticus Arcana

Flashcards Anki gerados a partir do [Codex Technomanticus](https://github.com/josenaldo/codex-technomanticus) — um grimório digital de engenharia de software.

## Como usar

1. Vá em [Releases](../../releases)
2. Baixe o arquivo `Codex-Technomanticus.apkg`
3. Abra o Anki e vá em **File → Import**
4. Selecione o arquivo `.apkg`

O deck será importado com sub-decks organizados por domínio:

- **Codex::Fundamentos** — Algoritmos, Estruturas de Dados, OOP, Banco de Dados, Testes, Redes
- **Codex::Arquitetura** — System Design, Design Patterns, API Design
- **Codex::Java** — Core, Spring Boot, Kafka
- **Codex::JavaScript** — JS/TS, Node.js, React
- **Codex::Infraestrutura** — Docker, Kubernetes, CI/CD, Linux
- **Codex::IA** — LLMs, Agents, Prompting
- **Codex::Aprendizado** — Behavioral, STAR Method, Narrativa Profissional

## Atualização

Baixe a nova release e importe novamente. O Anki faz merge por ID — cards existentes são atualizados, novos são adicionados, e seu progresso de estudo é preservado.

## Tipos de cards

| Tipo | Descrição |
|------|-----------|
| **Basic** | Pergunta e resposta direta |
| **Cloze** | Preenchimento de lacuna |
| **Vocab** | Vocabulário bilíngue PT-BR ↔ EN |
| **Scenario** | Situação prática com pergunta |
| **Pitfall** | Armadilha comum e como evitar |

## Licença

MIT
```

- [ ] **Step 8: Commit scaffold**

```bash
git add -A
git commit -m "feat: initial repo scaffold with project config and directory structure"
```

---

## Task 2: YAML Schema — Data Models

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/models.py`
- Create: `tests/test_models.py`
- Create: `tests/__init__.py`
- Create: `tests/fixtures/valid_sample.yaml`

- [ ] **Step 1: Create test fixtures**

Create `tests/fixtures/valid_sample.yaml` with a complete sample covering all 5 card types:

```yaml
source: "Fundamentos/Algoritmos.md"
source_hash: "abc123def456"
deck: "Codex::Fundamentos"
generated: "2026-04-12"
tags:
  - fundamentos
  - entrevista

cards:
  - id: fund-algo-001
    type: basic
    front: "O que é complexidade de tempo (time complexity)?"
    back: |
      Medida de como o tempo de execução cresce
      em função do tamanho da entrada (n).
      Expressa em notação Big O.
    tags: [algoritmos, complexidade]

  - id: fund-algo-002
    type: cloze
    text: "A busca binária tem complexidade {{c1::O(log n)}} porque divide o espaço pela metade."
    tags: [algoritmos, busca]

  - id: fund-algo-003
    type: vocab
    term_pt: "Complexidade de tempo"
    term_en: "Time complexity"
    definition: "How the running time grows as a function of input size."
    usage: "The time complexity of this solution is O(n log n)."
    tags: [algoritmos, vocabulario]

  - id: fund-algo-004
    type: scenario
    situation: "Você precisa buscar um elemento em uma lista ordenada de 1 milhão de itens."
    question: "Qual algoritmo usar e qual a complexidade?"
    answer: "Busca binária — O(log n). No máximo ~20 comparações."
    tags: [algoritmos, busca]

  - id: fund-algo-005
    type: pitfall
    trap: "Usar busca binária em lista não ordenada"
    why: "Busca binária assume dados ordenados. Em lista desordenada, retorna resultado incorreto silenciosamente."
    prevention: "Sempre validar ou garantir ordenação antes de aplicar."
    tags: [algoritmos, armadilhas]
```

- [ ] **Step 2: Write failing tests for models**

Create `tests/__init__.py` (empty) and `tests/test_models.py`:

```python
import pytest
from pathlib import Path
from scripts.models import CardFile, Card, load_card_file

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_card_file_parses_metadata():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    assert cf.source == "Fundamentos/Algoritmos.md"
    assert cf.source_hash == "abc123def456"
    assert cf.deck == "Codex::Fundamentos"
    assert cf.generated == "2026-04-12"
    assert "fundamentos" in cf.tags


def test_load_card_file_parses_all_cards():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    assert len(cf.cards) == 5


def test_basic_card_fields():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[0]
    assert card.id == "fund-algo-001"
    assert card.type == "basic"
    assert card.front is not None
    assert card.back is not None


def test_cloze_card_fields():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[1]
    assert card.type == "cloze"
    assert card.text is not None
    assert "{{c1::" in card.text


def test_vocab_card_fields():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[2]
    assert card.type == "vocab"
    assert card.term_pt is not None
    assert card.term_en is not None
    assert card.definition is not None
    assert card.usage is not None


def test_scenario_card_fields():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[3]
    assert card.type == "scenario"
    assert card.situation is not None
    assert card.question is not None
    assert card.answer is not None


def test_pitfall_card_fields():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[4]
    assert card.type == "pitfall"
    assert card.trap is not None
    assert card.why is not None
    assert card.prevention is not None


def test_card_tags():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    for card in cf.cards:
        assert len(card.tags) >= 1


def test_load_nonexistent_file_raises():
    with pytest.raises(FileNotFoundError):
        load_card_file(Path("/nonexistent/file.yaml"))
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd ~/repos/personal/codex-technomanticus-arcana
python -m pytest tests/test_models.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.models'`

- [ ] **Step 4: Implement models.py**

Create `scripts/__init__.py` (empty) and `scripts/models.py`:

```python
"""Data models for Arcana card files."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Card:
    """A single flashcard."""

    id: str
    type: str  # basic, cloze, vocab, scenario, pitfall
    tags: list[str] = field(default_factory=list)

    # basic
    front: Optional[str] = None
    back: Optional[str] = None

    # cloze
    text: Optional[str] = None

    # vocab
    term_pt: Optional[str] = None
    term_en: Optional[str] = None
    definition: Optional[str] = None
    usage: Optional[str] = None

    # scenario
    situation: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None

    # pitfall
    trap: Optional[str] = None
    why: Optional[str] = None
    prevention: Optional[str] = None


@dataclass
class CardFile:
    """A YAML file containing cards for one source note."""

    source: str
    source_hash: str
    deck: str
    generated: str
    tags: list[str]
    cards: list[Card]


def load_card_file(path: Path) -> CardFile:
    """Load and parse a card YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Card file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    cards = []
    for card_data in data.get("cards", []):
        cards.append(Card(**card_data))

    return CardFile(
        source=data["source"],
        source_hash=data["source_hash"],
        deck=data["deck"],
        generated=str(data["generated"]),
        tags=data.get("tags", []),
        cards=cards,
    )
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd ~/repos/personal/codex-technomanticus-arcana
python -m pytest tests/test_models.py -v
```

Expected: all 9 tests PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/__init__.py scripts/models.py tests/__init__.py tests/test_models.py tests/fixtures/valid_sample.yaml
git commit -m "feat: add YAML card data models with parsing and tests"
```

---

## Task 3: Validation Script

**Files:**
- Create: `scripts/validate_cards.py`
- Create: `tests/test_validate.py`
- Create: `tests/fixtures/invalid_sample.yaml`

- [ ] **Step 1: Create invalid fixture**

Create `tests/fixtures/invalid_sample.yaml`:

```yaml
source: "Fundamentos/Teste.md"
source_hash: "bad123"
deck: "Codex::Fundamentos"
generated: "2026-04-12"
tags:
  - fundamentos

cards:
  # Missing back field
  - id: fund-teste-001
    type: basic
    front: "Pergunta sem resposta?"
    tags: [testes]

  # Invalid cloze — no {{c1::}}
  - id: fund-teste-002
    type: cloze
    text: "Texto sem cloze marker nenhum."
    tags: [testes]

  # Incomplete vocab — missing definition
  - id: fund-teste-003
    type: vocab
    term_pt: "Teste"
    term_en: "Test"
    tags: []

  # Invalid ID format
  - id: invalid_id_format
    type: basic
    front: "Pergunta?"
    back: "Resposta."
    tags: [testes]

  # Duplicate front
  - id: fund-teste-005
    type: basic
    front: "Pergunta sem resposta?"
    back: "Agora com resposta."
    tags: [testes]

  # Empty tags
  - id: fund-teste-006
    type: scenario
    situation: "Situação"
    question: "Pergunta"
    answer: "Resposta"
    tags: []
```

- [ ] **Step 2: Write failing tests for validation**

Create `tests/test_validate.py`:

```python
import pytest
from pathlib import Path
from scripts.models import load_card_file
from scripts.validate_cards import validate_card_file, validate_card, Violation

FIXTURES = Path(__file__).parent / "fixtures"


def test_valid_file_has_no_violations():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    violations = validate_card_file(cf)
    assert len(violations) == 0


def test_basic_missing_back():
    cf = load_card_file(FIXTURES / "invalid_sample.yaml")
    violations = validate_card_file(cf)
    ids = [v.card_id for v in violations]
    assert "fund-teste-001" in ids


def test_cloze_missing_marker():
    cf = load_card_file(FIXTURES / "invalid_sample.yaml")
    violations = validate_card_file(cf)
    cloze_violations = [v for v in violations if v.card_id == "fund-teste-002"]
    assert len(cloze_violations) > 0
    assert any("cloze" in v.rule.lower() for v in cloze_violations)


def test_vocab_missing_fields():
    cf = load_card_file(FIXTURES / "invalid_sample.yaml")
    violations = validate_card_file(cf)
    vocab_violations = [v for v in violations if v.card_id == "fund-teste-003"]
    assert len(vocab_violations) > 0


def test_invalid_id_format():
    cf = load_card_file(FIXTURES / "invalid_sample.yaml")
    violations = validate_card_file(cf)
    id_violations = [v for v in violations if v.card_id == "invalid_id_format"]
    assert len(id_violations) > 0
    assert any("id" in v.rule.lower() for v in id_violations)


def test_duplicate_front():
    cf = load_card_file(FIXTURES / "invalid_sample.yaml")
    violations = validate_card_file(cf)
    dup_violations = [v for v in violations if "duplicat" in v.rule.lower()]
    assert len(dup_violations) > 0


def test_empty_tags():
    cf = load_card_file(FIXTURES / "invalid_sample.yaml")
    violations = validate_card_file(cf)
    tag_violations = [v for v in violations if v.card_id == "fund-teste-006"]
    assert len(tag_violations) > 0


def test_violation_has_suggestion():
    cf = load_card_file(FIXTURES / "invalid_sample.yaml")
    violations = validate_card_file(cf)
    for v in violations:
        assert v.suggestion is not None
        assert len(v.suggestion) > 0
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
python -m pytest tests/test_validate.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.validate_cards'`

- [ ] **Step 4: Implement validate_cards.py**

Create `scripts/validate_cards.py`:

```python
"""Validate card YAML files against quality rules."""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from scripts.models import Card, CardFile, load_card_file

ID_PATTERN = re.compile(r"^[a-z]+-[a-z]+-\d{3}$")
CLOZE_PATTERN = re.compile(r"\{\{c\d+::")
VALID_TYPES = {"basic", "cloze", "vocab", "scenario", "pitfall"}


@dataclass
class Violation:
    """A single validation violation."""

    card_id: str
    rule: str
    suggestion: str


def validate_card(card: Card, seen_fronts: set[str]) -> list[Violation]:
    """Validate a single card against all rules."""
    violations = []

    # ID format
    if not ID_PATTERN.match(card.id):
        violations.append(Violation(
            card_id=card.id,
            rule="ID inválido",
            suggestion=f"ID deve seguir o padrão domínio-slug-NNN (ex: fund-algo-001). Atual: '{card.id}'",
        ))

    # Tags present
    if not card.tags:
        violations.append(Violation(
            card_id=card.id,
            rule="Tags ausentes",
            suggestion="Adicione pelo menos 1 tag ao card.",
        ))

    # Type-specific validations
    if card.type == "basic":
        if not card.front:
            violations.append(Violation(
                card_id=card.id,
                rule="Basic: front ausente",
                suggestion="Cards basic precisam do campo 'front'.",
            ))
        if not card.back:
            violations.append(Violation(
                card_id=card.id,
                rule="Basic: back ausente",
                suggestion="Cards basic precisam do campo 'back'.",
            ))
        if card.front:
            if card.front in seen_fronts:
                violations.append(Violation(
                    card_id=card.id,
                    rule="Duplicata: front idêntico",
                    suggestion=f"Já existe um card com front '{card.front[:50]}...'",
                ))
            seen_fronts.add(card.front)

    elif card.type == "cloze":
        if not card.text:
            violations.append(Violation(
                card_id=card.id,
                rule="Cloze: text ausente",
                suggestion="Cards cloze precisam do campo 'text'.",
            ))
        elif not CLOZE_PATTERN.search(card.text):
            violations.append(Violation(
                card_id=card.id,
                rule="Cloze: marker ausente",
                suggestion="Cards cloze precisam de pelo menos um {{c1::...}} no text.",
            ))

    elif card.type == "vocab":
        missing = []
        if not card.term_pt:
            missing.append("term_pt")
        if not card.term_en:
            missing.append("term_en")
        if not card.definition:
            missing.append("definition")
        if missing:
            violations.append(Violation(
                card_id=card.id,
                rule="Vocab: campos obrigatórios ausentes",
                suggestion=f"Campos faltando: {', '.join(missing)}",
            ))

    elif card.type == "scenario":
        missing = []
        if not card.situation:
            missing.append("situation")
        if not card.question:
            missing.append("question")
        if not card.answer:
            missing.append("answer")
        if missing:
            violations.append(Violation(
                card_id=card.id,
                rule="Scenario: campos obrigatórios ausentes",
                suggestion=f"Campos faltando: {', '.join(missing)}",
            ))

    elif card.type == "pitfall":
        missing = []
        if not card.trap:
            missing.append("trap")
        if not card.why:
            missing.append("why")
        if not card.prevention:
            missing.append("prevention")
        if missing:
            violations.append(Violation(
                card_id=card.id,
                rule="Pitfall: campos obrigatórios ausentes",
                suggestion=f"Campos faltando: {', '.join(missing)}",
            ))

    return violations


def validate_card_file(card_file: CardFile) -> list[Violation]:
    """Validate all cards in a card file."""
    violations = []
    seen_fronts: set[str] = set()
    for card in card_file.cards:
        violations.extend(validate_card(card, seen_fronts))
    return violations


def main() -> int:
    """CLI entry point: validate all YAML files in cards/."""
    cards_dir = Path(__file__).parent.parent / "cards"
    if not cards_dir.exists():
        print(f"ERROR: cards directory not found: {cards_dir}")
        return 1

    yaml_files = sorted(cards_dir.rglob("*.yaml"))
    if not yaml_files:
        print("No card files found. Nothing to validate.")
        return 0

    total_violations = 0
    for yaml_path in yaml_files:
        card_file = load_card_file(yaml_path)
        violations = validate_card_file(card_file)
        if violations:
            print(f"\n--- {yaml_path.relative_to(cards_dir)} ---")
            for v in violations:
                print(f"  [{v.card_id}] {v.rule}: {v.suggestion}")
            total_violations += len(violations)

    if total_violations > 0:
        print(f"\nFAIL: {total_violations} violation(s) found.")
        return 1

    print(f"OK: {len(yaml_files)} file(s) validated, no violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python -m pytest tests/test_validate.py -v
```

Expected: all 8 tests PASS

- [ ] **Step 6: Test CLI mode with valid fixture**

```bash
cd ~/repos/personal/codex-technomanticus-arcana
cp tests/fixtures/valid_sample.yaml cards/fundamentos/algoritmos.yaml
python -m scripts.validate_cards
```

Expected: `OK: 1 file(s) validated, no violations.`

```bash
rm cards/fundamentos/algoritmos.yaml
```

- [ ] **Step 7: Commit**

```bash
git add scripts/validate_cards.py tests/test_validate.py tests/fixtures/invalid_sample.yaml
git commit -m "feat: add card validation script with rules for all card types"
```

---

## Task 4: Build Script (YAML → .apkg)

**Files:**
- Create: `scripts/build_deck.py`
- Create: `templates/card_styles.css`
- Create: `tests/test_build.py`

- [ ] **Step 1: Create card styles**

Create `templates/card_styles.css`:

```css
/* Codex Technomanticus Arcana — Anki Card Styles */

.card {
    font-family: "Source Sans Pro", "Segoe UI", system-ui, sans-serif;
    font-size: 18px;
    line-height: 1.6;
    color: #1a1a2e;
    background: #f5f5f5;
    padding: 24px;
    max-width: 640px;
    margin: 0 auto;
}

.card.nightMode {
    color: #e0e0e0;
    background: #1a1a2e;
}

.front {
    font-size: 20px;
    font-weight: 600;
    text-align: center;
}

.back {
    text-align: left;
}

.label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #6c63ff;
    margin-bottom: 8px;
}

.nightMode .label {
    color: #9d97ff;
}

.vocab-term {
    font-size: 24px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 4px;
}

.vocab-lang {
    font-size: 13px;
    color: #888;
    text-align: center;
    margin-bottom: 16px;
}

.separator {
    border: none;
    border-top: 1px solid #ddd;
    margin: 16px 0;
}

.nightMode .separator {
    border-top-color: #333;
}

pre {
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: "IBM Plex Mono", "Fira Code", monospace;
    font-size: 14px;
}

code {
    font-family: "IBM Plex Mono", "Fira Code", monospace;
    font-size: 14px;
    background: #e8e8e8;
    padding: 2px 6px;
    border-radius: 3px;
}

.nightMode code {
    background: #333;
}

pre code {
    background: none;
    padding: 0;
}

.tags {
    font-size: 12px;
    color: #999;
    margin-top: 16px;
    text-align: right;
}
```

- [ ] **Step 2: Write failing tests for build**

Create `tests/test_build.py`:

```python
import pytest
from pathlib import Path
from scripts.build_deck import build_apkg, create_basic_note, create_cloze_note, create_vocab_note, create_scenario_note, create_pitfall_note, md_to_html
from scripts.models import load_card_file

FIXTURES = Path(__file__).parent / "fixtures"
DIST = Path(__file__).parent.parent / "dist"


def test_md_to_html_bold():
    assert "<strong>" in md_to_html("**bold**")


def test_md_to_html_code():
    assert "<code>" in md_to_html("`code`")


def test_md_to_html_plain():
    result = md_to_html("plain text")
    assert "plain text" in result


def test_create_basic_note():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[0]
    note = create_basic_note(card, cf.tags)
    assert note is not None


def test_create_cloze_note():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[1]
    note = create_cloze_note(card, cf.tags)
    assert note is not None


def test_create_vocab_note():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[2]
    note = create_vocab_note(card, cf.tags)
    assert note is not None


def test_create_scenario_note():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[3]
    note = create_scenario_note(card, cf.tags)
    assert note is not None


def test_create_pitfall_note():
    cf = load_card_file(FIXTURES / "valid_sample.yaml")
    card = cf.cards[4]
    note = create_pitfall_note(card, cf.tags)
    assert note is not None


def test_build_apkg_creates_file(tmp_path):
    output = tmp_path / "test.apkg"
    card_files = [load_card_file(FIXTURES / "valid_sample.yaml")]
    build_apkg(card_files, output)
    assert output.exists()
    assert output.stat().st_size > 0
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
python -m pytest tests/test_build.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.build_deck'`

- [ ] **Step 4: Implement build_deck.py**

Create `scripts/build_deck.py`:

```python
"""Build Anki .apkg deck from YAML card files."""

import hashlib
import sys
from pathlib import Path

import genanki
import markdown
import yaml

from scripts.models import Card, CardFile, load_card_file

STYLES_PATH = Path(__file__).parent.parent / "templates" / "card_styles.css"

# Stable model IDs (generated once, never change — Anki uses these for merge)
MODEL_BASIC_ID = 1607392319
MODEL_CLOZE_ID = 1607392320
MODEL_VOCAB_ID = 1607392321
MODEL_SCENARIO_ID = 1607392322
MODEL_PITFALL_ID = 1607392323
DECK_ROOT_ID = 1607392300


def _load_styles() -> str:
    if STYLES_PATH.exists():
        return STYLES_PATH.read_text(encoding="utf-8")
    return ""


def _deck_id(name: str) -> int:
    """Generate a stable deck ID from deck name."""
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def md_to_html(text: str) -> str:
    """Convert Markdown text to HTML."""
    if not text:
        return ""
    return markdown.markdown(text.strip(), extensions=["fenced_code"])


def _make_basic_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_BASIC_ID,
        "Codex Basic",
        fields=[
            {"name": "Front"},
            {"name": "Back"},
            {"name": "Tags"},
        ],
        templates=[{
            "name": "Card",
            "qfmt": '<div class="front">{{Front}}</div>',
            "afmt": (
                '{{FrontSide}}<hr class="separator">'
                '<div class="back">{{Back}}</div>'
                '<div class="tags">{{Tags}}</div>'
            ),
        }],
        css=css,
    )


def _make_cloze_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_CLOZE_ID,
        "Codex Cloze",
        model_type=genanki.Model.CLOZE,
        fields=[
            {"name": "Text"},
            {"name": "Tags"},
        ],
        templates=[{
            "name": "Cloze",
            "qfmt": '<div class="front">{{cloze:Text}}</div>',
            "afmt": (
                '<div class="back">{{cloze:Text}}</div>'
                '<div class="tags">{{Tags}}</div>'
            ),
        }],
        css=css,
    )


def _make_vocab_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_VOCAB_ID,
        "Codex Vocab",
        fields=[
            {"name": "TermPT"},
            {"name": "TermEN"},
            {"name": "Definition"},
            {"name": "Usage"},
            {"name": "Tags"},
        ],
        templates=[
            {
                "name": "PT → EN",
                "qfmt": (
                    '<div class="vocab-term">{{TermPT}}</div>'
                    '<div class="vocab-lang">Português → English</div>'
                ),
                "afmt": (
                    '{{FrontSide}}<hr class="separator">'
                    '<div class="vocab-term">{{TermEN}}</div>'
                    '<div class="label">Definition</div>'
                    '<div class="back">{{Definition}}</div>'
                    '<div class="label">Usage</div>'
                    '<div class="back">{{Usage}}</div>'
                    '<div class="tags">{{Tags}}</div>'
                ),
            },
            {
                "name": "EN → PT",
                "qfmt": (
                    '<div class="vocab-term">{{TermEN}}</div>'
                    '<div class="vocab-lang">English → Português</div>'
                ),
                "afmt": (
                    '{{FrontSide}}<hr class="separator">'
                    '<div class="vocab-term">{{TermPT}}</div>'
                    '<div class="label">Definição</div>'
                    '<div class="back">{{Definition}}</div>'
                    '<div class="tags">{{Tags}}</div>'
                ),
            },
        ],
        css=css,
    )


def _make_scenario_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_SCENARIO_ID,
        "Codex Scenario",
        fields=[
            {"name": "Situation"},
            {"name": "Question"},
            {"name": "Answer"},
            {"name": "Tags"},
        ],
        templates=[{
            "name": "Card",
            "qfmt": (
                '<div class="label">Cenário</div>'
                '<div class="back">{{Situation}}</div>'
                '<hr class="separator">'
                '<div class="front">{{Question}}</div>'
            ),
            "afmt": (
                '{{FrontSide}}<hr class="separator">'
                '<div class="back">{{Answer}}</div>'
                '<div class="tags">{{Tags}}</div>'
            ),
        }],
        css=css,
    )


def _make_pitfall_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_PITFALL_ID,
        "Codex Pitfall",
        fields=[
            {"name": "Trap"},
            {"name": "Why"},
            {"name": "Prevention"},
            {"name": "Tags"},
        ],
        templates=[{
            "name": "Card",
            "qfmt": (
                '<div class="label">⚠ Armadilha</div>'
                '<div class="front">{{Trap}}</div>'
            ),
            "afmt": (
                '{{FrontSide}}<hr class="separator">'
                '<div class="label">Por quê</div>'
                '<div class="back">{{Why}}</div>'
                '<div class="label">Prevenção</div>'
                '<div class="back">{{Prevention}}</div>'
                '<div class="tags">{{Tags}}</div>'
            ),
        }],
        css=css,
    )


def _card_guid(card_id: str) -> str:
    """Stable GUID from card ID for Anki merge."""
    return genanki.guid_for(card_id)


def create_basic_note(card: Card, file_tags: list[str]) -> genanki.Note:
    css = _load_styles()
    model = _make_basic_model(css)
    all_tags = list(set(file_tags + card.tags))
    return genanki.Note(
        model=model,
        fields=[md_to_html(card.front), md_to_html(card.back), " ".join(card.tags)],
        guid=_card_guid(card.id),
        tags=all_tags,
    )


def create_cloze_note(card: Card, file_tags: list[str]) -> genanki.Note:
    css = _load_styles()
    model = _make_cloze_model(css)
    all_tags = list(set(file_tags + card.tags))
    return genanki.Note(
        model=model,
        fields=[md_to_html(card.text), " ".join(card.tags)],
        guid=_card_guid(card.id),
        tags=all_tags,
    )


def create_vocab_note(card: Card, file_tags: list[str]) -> genanki.Note:
    css = _load_styles()
    model = _make_vocab_model(css)
    all_tags = list(set(file_tags + card.tags))
    return genanki.Note(
        model=model,
        fields=[
            card.term_pt or "",
            card.term_en or "",
            md_to_html(card.definition),
            md_to_html(card.usage),
            " ".join(card.tags),
        ],
        guid=_card_guid(card.id),
        tags=all_tags,
    )


def create_scenario_note(card: Card, file_tags: list[str]) -> genanki.Note:
    css = _load_styles()
    model = _make_scenario_model(css)
    all_tags = list(set(file_tags + card.tags))
    return genanki.Note(
        model=model,
        fields=[
            md_to_html(card.situation),
            md_to_html(card.question),
            md_to_html(card.answer),
            " ".join(card.tags),
        ],
        guid=_card_guid(card.id),
        tags=all_tags,
    )


def create_pitfall_note(card: Card, file_tags: list[str]) -> genanki.Note:
    css = _load_styles()
    model = _make_pitfall_model(css)
    all_tags = list(set(file_tags + card.tags))
    return genanki.Note(
        model=model,
        fields=[
            md_to_html(card.trap),
            md_to_html(card.why),
            md_to_html(card.prevention),
            " ".join(card.tags),
        ],
        guid=_card_guid(card.id),
        tags=all_tags,
    )


NOTE_CREATORS = {
    "basic": create_basic_note,
    "cloze": create_cloze_note,
    "vocab": create_vocab_note,
    "scenario": create_scenario_note,
    "pitfall": create_pitfall_note,
}


def build_apkg(card_files: list[CardFile], output_path: Path) -> None:
    """Build .apkg from a list of CardFile objects."""
    decks: dict[str, genanki.Deck] = {}

    for cf in card_files:
        deck_name = cf.deck
        if deck_name not in decks:
            decks[deck_name] = genanki.Deck(_deck_id(deck_name), deck_name)

        deck = decks[deck_name]
        for card in cf.cards:
            creator = NOTE_CREATORS.get(card.type)
            if creator:
                note = creator(card, cf.tags)
                deck.add_note(note)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    package = genanki.Package(list(decks.values()))
    package.write_to_file(str(output_path))


def main() -> int:
    """CLI entry point: build .apkg from all YAML files in cards/."""
    cards_dir = Path(__file__).parent.parent / "cards"
    output = Path(__file__).parent.parent / "dist" / "Codex-Technomanticus.apkg"

    yaml_files = sorted(cards_dir.rglob("*.yaml"))
    if not yaml_files:
        print("No card files found. Nothing to build.")
        return 0

    card_files = [load_card_file(f) for f in yaml_files]
    total_cards = sum(len(cf.cards) for cf in card_files)

    build_apkg(card_files, output)

    decks = set(cf.deck for cf in card_files)
    print(f"Built {output}: {total_cards} cards in {len(decks)} deck(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python -m pytest tests/test_build.py -v
```

Expected: all 10 tests PASS

- [ ] **Step 6: End-to-end test — build from fixture**

```bash
cp tests/fixtures/valid_sample.yaml cards/fundamentos/algoritmos.yaml
python -m scripts.build_deck
ls -la dist/
```

Expected: `Built dist/Codex-Technomanticus.apkg: 5 cards in 1 deck(s)`, file exists and is > 0 bytes.

```bash
rm cards/fundamentos/algoritmos.yaml
rm dist/Codex-Technomanticus.apkg
```

- [ ] **Step 7: Commit**

```bash
git add scripts/build_deck.py templates/card_styles.css tests/test_build.py
git commit -m "feat: add build script to generate .apkg decks from YAML cards"
```

---

## Task 5: CI/CD Pipeline

**Files:**
- Create: `.github/workflows/build-release.yaml`

- [ ] **Step 1: Create workflow file**

```bash
mkdir -p ~/repos/personal/codex-technomanticus-arcana/.github/workflows
```

Create `.github/workflows/build-release.yaml`:

```yaml
name: Build & Release Arcana

on:
  push:
    branches: [main]
    tags: ['v*']
  workflow_dispatch:

jobs:
  validate-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: python -m pytest tests/ -v

      - name: Validate cards
        run: python -m scripts.validate_cards

      - name: Build deck
        run: python -m scripts.build_deck

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: Codex-Technomanticus
          path: dist/Codex-Technomanticus.apkg

  release:
    needs: validate-and-build
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: Codex-Technomanticus

      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          files: Codex-Technomanticus.apkg
          generate_release_notes: true
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/build-release.yaml
git commit -m "ci: add build and release workflow for .apkg generation"
```

---

## Task 6: Skill — arcana-cards

**Files:**
- Create: `~/.agents/skills/arcana-cards/SKILL.md`

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p ~/.agents/skills/arcana-cards
```

- [ ] **Step 2: Write SKILL.md**

Create `~/.agents/skills/arcana-cards/SKILL.md`:

````markdown
---
name: arcana-cards
description: Generate Anki flashcards from a single Obsidian note. Use when asked to create cards for a specific note, or when invoked by arcana-forge for batch processing. Reads the note, generates cards using AI, writes YAML to the arcana repo.
metadata:
  author: josenaldo
  version: "0.1.0"
  domain: study
  triggers: anki, flashcard, cards, arcana, gerar cards, criar cards
  role: generator
  scope: implementation
  output-format: yaml
  related-skills: arcana-forge, arcana-constraint, arcana-deck, obsidian-markdown
---

# Arcana Cards — Flashcard Generator

Generate high-quality Anki flashcards from an Obsidian note.

## Input

You will receive either:
- A file path to a note in the vault (`~/repos/personal/codex-technomanticus/`)
- Note content directly (when invoked by arcana-forge)

## Output

A YAML file written to `~/repos/personal/codex-technomanticus-arcana/cards/<domain>/<slug>.yaml`

## Workflow

1. **Read the note** — parse frontmatter (title, tags, type, status) and all sections
2. **Determine the domain** — map the note's folder to a domain prefix:
   - `Fundamentos/` → `fund-`, deck `Codex::Fundamentos`
   - `Arquitetura/` → `arq-`, deck `Codex::Arquitetura`
   - `Java/` → `java-`, deck `Codex::Java`
   - `JavaScript/` → `js-`, deck `Codex::JavaScript`
   - `Infraestrutura/` → `infra-`, deck `Codex::Infraestrutura`
   - `IA/` → `ia-`, deck `Codex::IA`
   - `Aprendizado/` → `aprend-`, deck `Codex::Aprendizado`
3. **Check for existing YAML** — if a YAML file already exists for this note:
   - Read it and note existing card IDs
   - Preserve existing IDs when updating content
   - Assign new sequential IDs for new cards (continue from highest existing)
4. **Generate cards** following these rules:
   - **Minimum 3, maximum ~15 cards** per note
   - **At least 1 cloze** per note
   - **At least 1 vocab** if the note has a "Key vocabulary" section
   - Cards must be **atomic** — 1 concept per card
   - **back/answer ≤ 50 words**
   - IDs follow pattern: `{prefix}-{slug}-{NNN}`

## Card Type Selection

Map note sections to card types:

| Note Section | Card Type(s) to Generate |
|---|---|
| "O que é" | 1-2 `basic` cards (definition, key properties) |
| "Como funciona" | 1-2 `basic` or `cloze` (mechanism, steps) |
| "Quando usar" | 1 `scenario` (practical situation) |
| "Armadilhas comuns" | 1-2 `pitfall` cards |
| "How to explain in English" | Extract key phrasing for `vocab` cards |
| "Key vocabulary" | 1 `vocab` card per term |
| Any section with key facts | `cloze` cards for important relationships |

## YAML Format

```yaml
source: "Domain/Note Name.md"
source_hash: "<md5 of note content>"
deck: "Codex::Domain"
generated: "YYYY-MM-DD"
tags:
  - <from note frontmatter>

cards:
  - id: prefix-slug-001
    type: basic|cloze|vocab|scenario|pitfall
    # ... type-specific fields (see spec)
    tags: [topic-specific]
```

## Quality Rules (enforced by arcana-constraint)

- Back/answer ≤ 50 words
- Front must have one clear answer (no ambiguity)
- Cloze: max 2 `{{cN::}}` per card
- All fields for the card type must be filled
- At least 1 tag per card
- No duplicate fronts within the same file

## Computing source_hash

```bash
md5sum "path/to/note.md" | cut -d' ' -f1
```

Or in the YAML generation, use the first 12 chars of the MD5 of the note content.

## After Generation

Report to the user:
- How many cards were generated (by type)
- Which file was written
- Any decisions made (e.g., "skipped Key vocabulary — section not found")
````

- [ ] **Step 3: Commit**

```bash
cd ~/.agents/skills
git add arcana-cards/SKILL.md 2>/dev/null || true
```

Note: `~/.agents/skills` may not be a git repo. The skill file is installed locally and ready to use.

---

## Task 7: Skill — arcana-constraint

**Files:**
- Create: `~/.agents/skills/arcana-constraint/SKILL.md`

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p ~/.agents/skills/arcana-constraint
```

- [ ] **Step 2: Write SKILL.md**

Create `~/.agents/skills/arcana-constraint/SKILL.md`:

````markdown
---
name: arcana-constraint
description: Validate Anki flashcards against quality rules. Use after generating cards (arcana-cards) or when reviewing existing cards. Checks atomicity, completeness, ID format, duplicates, and SRS best practices.
metadata:
  author: josenaldo
  version: "0.1.0"
  domain: study
  triggers: validar cards, validate, constraint, arcana validate
  role: validator
  scope: constraint
  output-format: report
  related-skills: arcana-cards, arcana-forge
---

# Arcana Constraint — Card Validator

Validate flashcards against Anki/SRS best practices.

## When to Run

- After `arcana-cards` generates new cards
- When reviewing existing card YAML files
- Before committing cards to the repo

## Validation Rules

Apply ALL of the following rules to each card:

### Structural Rules

| Rule | Check | Fix |
|------|-------|-----|
| **ID format** | Must match `^[a-z]+-[a-z]+-\d{3}$` | Reformat ID |
| **Tags present** | At least 1 tag per card | Add topic tag |
| **Type valid** | Must be: basic, cloze, vocab, scenario, pitfall | Fix type |
| **Required fields** | All fields for the type must be non-empty | Fill missing fields |

### Content Quality Rules

| Rule | Check | Fix |
|------|-------|-----|
| **Atomicity** | back/answer ≤ 50 words | Split into multiple cards |
| **No ambiguity** | Front/question must have one clear answer | Rephrase to be specific |
| **Cloze well-formed** | Text contains `{{c1::...}}`, max 2 clozes | Fix markers |
| **No duplicates** | No identical front/text within same file | Remove or differentiate |
| **Vocab complete** | term_pt + term_en + definition all present | Fill missing |
| **Scenario complete** | situation + question + answer all present | Fill missing |
| **Pitfall complete** | trap + why + prevention all present | Fill missing |

### File-Level Rules

| Rule | Check | Fix |
|------|-------|-----|
| **Minimum cards** | At least 3 cards per file | Generate more |
| **Has cloze** | At least 1 cloze card per file | Add cloze |
| **Has vocab** | At least 1 vocab if source has "Key vocabulary" | Add vocab |

## How to Validate

### Option A: Read YAML and validate manually

1. Read the YAML file
2. Check each card against the rules above
3. Report violations

### Option B: Run the validation script

```bash
cd ~/repos/personal/codex-technomanticus-arcana
python -m scripts.validate_cards
```

The script checks structural rules. Content quality rules (atomicity, ambiguity) require AI judgment — apply those by reading the cards yourself.

## Output Format

For each violation found, report:

```
[card-id] Rule: description
  Suggestion: how to fix
```

End with either:
- **OK** — all cards pass validation
- **FAIL** — N violation(s) found, with fixes applied or suggested

## Auto-Fix

When invoked by `arcana-forge`, automatically fix these issues:
- Missing tags → add the file-level tags
- ID format → reformat to match pattern
- Word count over 50 → suggest shortened version

For issues requiring judgment (ambiguity, atomicity), flag them for the user.
````

- [ ] **Step 3: Verify skill is readable**

```bash
cat ~/.agents/skills/arcana-constraint/SKILL.md | head -5
```

Expected: shows the YAML frontmatter header.

---

## Task 8: Skill — arcana-deck

**Files:**
- Create: `~/.agents/skills/arcana-deck/SKILL.md`

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p ~/.agents/skills/arcana-deck
```

- [ ] **Step 2: Write SKILL.md**

Create `~/.agents/skills/arcana-deck/SKILL.md`:

````markdown
---
name: arcana-deck
description: Build Anki .apkg deck from YAML card files. Use for local preview of the deck before pushing to CI. Wraps the build_deck.py script.
metadata:
  author: josenaldo
  version: "0.1.0"
  domain: study
  triggers: build deck, gerar deck, apkg, arcana build, preview deck
  role: builder
  scope: implementation
  output-format: binary
  related-skills: arcana-cards, arcana-forge, arcana-constraint
---

# Arcana Deck — Local Deck Builder

Build an Anki `.apkg` file from the YAML cards for local preview.

## When to Use

- To preview the deck locally before pushing to CI
- To test card rendering in Anki
- To generate a one-off deck for personal use

**Note:** The primary build path is via CI/CD (GitHub Actions). This skill is for local preview only.

## Prerequisites

Python dependencies must be installed:

```bash
cd ~/repos/personal/codex-technomanticus-arcana
pip install -r requirements.txt
```

## Workflow

1. **Validate first** — run validation to catch issues before building

```bash
cd ~/repos/personal/codex-technomanticus-arcana
python -m scripts.validate_cards
```

If validation fails, fix issues before building.

2. **Build the deck**

```bash
cd ~/repos/personal/codex-technomanticus-arcana
python -m scripts.build_deck
```

Output: `dist/Codex-Technomanticus.apkg`

3. **Report results**

Tell the user:
- Number of cards built
- Number of decks (sub-decks)
- Path to the `.apkg` file
- How to import: open Anki → File → Import → select the file

## Troubleshooting

- **"No card files found"** — no `.yaml` files exist in `cards/`. Generate cards first with `arcana-cards` or `arcana-forge`.
- **YAML parse error** — check the YAML file for syntax issues (indentation, special characters).
- **genanki not installed** — run `pip install -r requirements.txt`.
````

---

## Task 9: Skill — arcana-forge + detect_changes.py

**Files:**
- Create: `~/.agents/skills/arcana-forge/SKILL.md`
- Create: `~/.agents/skills/arcana-forge/detect_changes.py`

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p ~/.agents/skills/arcana-forge
```

- [ ] **Step 2: Write detect_changes.py**

Create `~/.agents/skills/arcana-forge/detect_changes.py`:

```python
#!/usr/bin/env python3
"""Detect vault notes changed since the last carding session.

Usage:
    python detect_changes.py <vault_path> <last_carding_file>

Output:
    One changed file path per line (relative to vault root).
    Exit code 0 if changes found, 1 if no changes, 2 on error.
"""

import subprocess
import sys
from pathlib import Path


def get_vault_head(vault_path: Path) -> str:
    """Get the current HEAD commit hash of the vault repo."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=vault_path,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_changed_notes(vault_path: Path, since_commit: str) -> list[str]:
    """List .md files changed since a given commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", since_commit, "HEAD", "--", "*.md"],
        cwd=vault_path,
        capture_output=True,
        text=True,
        check=True,
    )
    files = [f for f in result.stdout.strip().split("\n") if f]
    # Exclude private/meta directories
    excluded_prefixes = ("00 - Inbox/", "_templates/", "_guia/", ".obsidian/", ".tmp/", "docs/")
    return [f for f in files if not any(f.startswith(p) for p in excluded_prefixes)]


def get_all_notes(vault_path: Path) -> list[str]:
    """List all .md note files (for first run when no last-carding exists)."""
    result = subprocess.run(
        ["git", "ls-files", "--", "*.md"],
        cwd=vault_path,
        capture_output=True,
        text=True,
        check=True,
    )
    files = [f for f in result.stdout.strip().split("\n") if f]
    excluded_prefixes = ("00 - Inbox/", "_templates/", "_guia/", ".obsidian/", ".tmp/", "docs/")
    return [f for f in files if not any(f.startswith(p) for p in excluded_prefixes)]


def main() -> int:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <vault_path> <last_carding_file>", file=sys.stderr)
        return 2

    vault_path = Path(sys.argv[1])
    last_carding_file = Path(sys.argv[2])

    if not vault_path.exists():
        print(f"ERROR: vault path not found: {vault_path}", file=sys.stderr)
        return 2

    # Read last carding commit
    since_commit = ""
    if last_carding_file.exists():
        since_commit = last_carding_file.read_text().strip()

    # Get changed files
    if since_commit:
        try:
            changed = get_changed_notes(vault_path, since_commit)
        except subprocess.CalledProcessError:
            print(f"WARNING: commit {since_commit} not found, listing all notes", file=sys.stderr)
            changed = get_all_notes(vault_path)
    else:
        print("First run — no .last-carding found, listing all notes", file=sys.stderr)
        changed = get_all_notes(vault_path)

    if not changed:
        print("No changes detected.", file=sys.stderr)
        return 1

    # Output changed files and current HEAD
    for f in sorted(changed):
        print(f)

    # Print current HEAD as last line prefixed with COMMIT:
    current_head = get_vault_head(vault_path)
    print(f"COMMIT:{current_head}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Make script executable**

```bash
chmod +x ~/.agents/skills/arcana-forge/detect_changes.py
```

- [ ] **Step 4: Test detect_changes.py**

```bash
# Create a temporary .last-carding to test
echo "" > /tmp/test-last-carding
python3 ~/.agents/skills/arcana-forge/detect_changes.py ~/repos/personal/codex-technomanticus /tmp/test-last-carding
```

Expected: lists all vault .md files (first run behavior) followed by `COMMIT:<hash>`

```bash
rm /tmp/test-last-carding
```

- [ ] **Step 5: Write SKILL.md**

Create `~/.agents/skills/arcana-forge/SKILL.md`:

````markdown
---
name: arcana-forge
description: Orchestrate Anki card generation for changed vault notes. Use when asked to "generate cards", "update cards", "cardear notas", or process vault changes into flashcards. Detects changed notes, generates cards via arcana-cards, validates via arcana-constraint.
metadata:
  author: josenaldo
  version: "0.1.0"
  domain: study
  triggers: gerar cards, forge, arcana, cardear, criar flashcards, notas recentes, update cards
  role: orchestrator
  scope: workflow
  output-format: report
  related-skills: arcana-cards, arcana-constraint, arcana-deck
---

# Arcana Forge — Card Generation Orchestrator

Orchestrate the full card generation flow: detect changed notes → generate cards → validate → report.

## Paths

- **Vault:** `~/repos/personal/codex-technomanticus/`
- **Arcana repo:** `~/repos/personal/codex-technomanticus-arcana/`
- **Last carding marker:** `~/repos/personal/codex-technomanticus-arcana/.last-carding`
- **Detect script:** `~/.agents/skills/arcana-forge/detect_changes.py`

## Workflow

### Step 1: Detect Changed Notes

Run the detection script:

```bash
python3 ~/.agents/skills/arcana-forge/detect_changes.py \
  ~/repos/personal/codex-technomanticus \
  ~/repos/personal/codex-technomanticus-arcana/.last-carding
```

The script outputs:
- One file path per line (notes that changed since last carding)
- Last line: `COMMIT:<hash>` (current vault HEAD, to save in `.last-carding` after success)

If no changes detected (exit code 1), inform the user and stop.

### Step 2: Present Changes to User

Show the list of changed/new notes and ask for confirmation:

```
Encontrei N notas alteradas desde o último cardeamento:
  - Fundamentos/Algoritmos.md (modificada)
  - Java/Spring Boot.md (nova)
  - ...

Deseja gerar cards para todas, ou selecionar específicas?
```

### Step 3: Generate Cards

For each selected note, invoke the **arcana-cards** skill:

1. Read the note content
2. Determine domain and slug from the file path
3. Generate cards following arcana-cards rules
4. Write YAML to `~/repos/personal/codex-technomanticus-arcana/cards/<domain>/<slug>.yaml`

When processing multiple notes, work through them sequentially, reporting progress.

### Step 4: Validate Cards

For each generated YAML, invoke the **arcana-constraint** skill:

1. Read the generated YAML
2. Apply all validation rules
3. Auto-fix what's possible (tags, ID format)
4. Flag issues requiring judgment

Alternatively, run the validation script for structural checks:

```bash
cd ~/repos/personal/codex-technomanticus-arcana
python -m scripts.validate_cards
```

### Step 5: Update Last Carding

After successful generation and validation, update the marker:

```bash
echo "<COMMIT_HASH from step 1>" > ~/repos/personal/codex-technomanticus-arcana/.last-carding
```

### Step 6: Report

Present a summary:

```
Cardeamento concluído:
  - 3 notas processadas
  - 27 cards gerados (12 basic, 5 cloze, 4 vocab, 3 scenario, 3 pitfall)
  - 0 violações encontradas
  - Arquivos criados/atualizados:
    - cards/fundamentos/algoritmos.yaml (9 cards)
    - cards/java/spring-boot.yaml (12 cards)
    - cards/infraestrutura/docker.yaml (6 cards)

Pronto para commit.
```

## Options

The user can customize the run:

- **Process specific notes:** "gere cards para Algoritmos.md"
  → Skip detection, process only the named note
- **Process a directory:** "gere cards para todas as notas de Fundamentos"
  → Filter detection to notes in `Fundamentos/`
- **Force reprocess:** "regenere os cards de Algoritmos"
  → Ignore `.last-carding`, reprocess even if unchanged
- **First run:** If `.last-carding` is empty, list ALL notes and ask user which domains to process first

## Error Handling

- If a note can't be parsed (no frontmatter, empty), skip it and report
- If card generation fails for a note, continue with others and report failures at the end
- If validation finds issues that can't be auto-fixed, present them and ask the user how to proceed
````

- [ ] **Step 6: Verify both files exist**

```bash
ls -la ~/.agents/skills/arcana-forge/
```

Expected: `SKILL.md` and `detect_changes.py`

- [ ] **Step 7: Commit the arcana repo docs and plans**

```bash
cd ~/repos/personal/codex-technomanticus-arcana
git add -A
git commit -m "docs: add implementation plan, ADRs, and project documentation"
```

---

## Task 10: End-to-End Smoke Test

**Files:** No new files — test the full flow.

- [ ] **Step 1: Run detect_changes against vault**

```bash
python3 ~/.agents/skills/arcana-forge/detect_changes.py \
  ~/repos/personal/codex-technomanticus \
  ~/repos/personal/codex-technomanticus-arcana/.last-carding
```

Expected: list of all vault notes (first run) + COMMIT hash

- [ ] **Step 2: Generate sample cards manually**

Copy the test fixture as a real card file to verify the full pipeline:

```bash
cd ~/repos/personal/codex-technomanticus-arcana
cp tests/fixtures/valid_sample.yaml cards/fundamentos/algoritmos.yaml
```

- [ ] **Step 3: Run validation**

```bash
python -m scripts.validate_cards
```

Expected: `OK: 1 file(s) validated, no violations.`

- [ ] **Step 4: Run build**

```bash
python -m scripts.build_deck
```

Expected: `Built dist/Codex-Technomanticus.apkg: 5 cards in 1 deck(s)`

- [ ] **Step 5: Verify .apkg file**

```bash
ls -lh dist/Codex-Technomanticus.apkg
```

Expected: file exists, size > 0

- [ ] **Step 6: Clean up test data**

```bash
rm cards/fundamentos/algoritmos.yaml
rm dist/Codex-Technomanticus.apkg
```

- [ ] **Step 7: Run all tests**

```bash
python -m pytest tests/ -v
```

Expected: all tests pass

- [ ] **Step 8: Final commit**

```bash
git add -A
git commit -m "chore: verify end-to-end pipeline works"
```

---

## Task 11: Create GitHub Repo and Push

- [ ] **Step 1: Create remote repo**

```bash
cd ~/repos/personal/codex-technomanticus-arcana
gh repo create josenaldo/codex-technomanticus-arcana --public --source=. --description "Anki flashcard decks from the Codex Technomanticus vault" --push
```

- [ ] **Step 2: Verify repo is live**

```bash
gh repo view josenaldo/codex-technomanticus-arcana --web
```

- [ ] **Step 3: Verify CI runs (no cards yet, should pass with "nothing to validate/build")**

```bash
gh run list --repo josenaldo/codex-technomanticus-arcana --limit 1
```
