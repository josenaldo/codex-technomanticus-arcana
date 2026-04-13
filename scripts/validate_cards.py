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
