"""Build Anki .apkg deck from YAML card files."""

import hashlib
import sys
from pathlib import Path

import genanki
import markdown

from scripts.models import Card, CardFile, load_card_file

STYLES_PATH = Path(__file__).parent.parent / "templates" / "card_styles.css"

MODEL_BASIC_ID = 1607392319
MODEL_CLOZE_ID = 1607392320
MODEL_VOCAB_ID = 1607392321
MODEL_SCENARIO_ID = 1607392322
MODEL_PITFALL_ID = 1607392323


def _load_styles() -> str:
    if STYLES_PATH.exists():
        return STYLES_PATH.read_text(encoding="utf-8")
    return ""


def _deck_id(name: str) -> int:
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def md_to_html(text: str) -> str:
    if not text:
        return ""
    return markdown.markdown(text.strip(), extensions=["fenced_code"])


def _make_basic_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_BASIC_ID,
        "Codex Basic",
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Tags"}],
        templates=[{
            "name": "Card",
            "qfmt": '<div class="front">{{Front}}</div>',
            "afmt": '{{FrontSide}}<hr class="separator"><div class="back">{{Back}}</div><div class="tags">{{Tags}}</div>',
        }],
        css=css,
    )


def _make_cloze_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_CLOZE_ID,
        "Codex Cloze",
        model_type=genanki.Model.CLOZE,
        fields=[{"name": "Text"}, {"name": "Tags"}],
        templates=[{
            "name": "Cloze",
            "qfmt": '<div class="front">{{cloze:Text}}</div>',
            "afmt": '<div class="back">{{cloze:Text}}</div><div class="tags">{{Tags}}</div>',
        }],
        css=css,
    )


def _make_vocab_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_VOCAB_ID,
        "Codex Vocab",
        fields=[
            {"name": "TermPT"}, {"name": "TermEN"},
            {"name": "Definition"}, {"name": "Usage"}, {"name": "Tags"},
        ],
        templates=[
            {
                "name": "PT → EN",
                "qfmt": '<div class="vocab-term">{{TermPT}}</div><div class="vocab-lang">Português → English</div>',
                "afmt": '{{FrontSide}}<hr class="separator"><div class="vocab-term">{{TermEN}}</div><div class="label">Definition</div><div class="back">{{Definition}}</div><div class="label">Usage</div><div class="back">{{Usage}}</div><div class="tags">{{Tags}}</div>',
            },
            {
                "name": "EN → PT",
                "qfmt": '<div class="vocab-term">{{TermEN}}</div><div class="vocab-lang">English → Português</div>',
                "afmt": '{{FrontSide}}<hr class="separator"><div class="vocab-term">{{TermPT}}</div><div class="label">Definição</div><div class="back">{{Definition}}</div><div class="tags">{{Tags}}</div>',
            },
        ],
        css=css,
    )


def _make_scenario_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_SCENARIO_ID,
        "Codex Scenario",
        fields=[
            {"name": "Situation"}, {"name": "Question"},
            {"name": "Answer"}, {"name": "Tags"},
        ],
        templates=[{
            "name": "Card",
            "qfmt": '<div class="label">Cenário</div><div class="back">{{Situation}}</div><hr class="separator"><div class="front">{{Question}}</div>',
            "afmt": '{{FrontSide}}<hr class="separator"><div class="back">{{Answer}}</div><div class="tags">{{Tags}}</div>',
        }],
        css=css,
    )


def _make_pitfall_model(css: str) -> genanki.Model:
    return genanki.Model(
        MODEL_PITFALL_ID,
        "Codex Pitfall",
        fields=[
            {"name": "Trap"}, {"name": "Why"},
            {"name": "Prevention"}, {"name": "Tags"},
        ],
        templates=[{
            "name": "Card",
            "qfmt": '<div class="label">⚠ Armadilha</div><div class="front">{{Trap}}</div>',
            "afmt": '{{FrontSide}}<hr class="separator"><div class="label">Por quê</div><div class="back">{{Why}}</div><div class="label">Prevenção</div><div class="back">{{Prevention}}</div><div class="tags">{{Tags}}</div>',
        }],
        css=css,
    )


def _card_guid(card_id: str) -> str:
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
            card.term_pt or "", card.term_en or "",
            md_to_html(card.definition), md_to_html(card.usage),
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
            md_to_html(card.situation), md_to_html(card.question),
            md_to_html(card.answer), " ".join(card.tags),
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
            md_to_html(card.trap), md_to_html(card.why),
            md_to_html(card.prevention), " ".join(card.tags),
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
