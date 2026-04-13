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
