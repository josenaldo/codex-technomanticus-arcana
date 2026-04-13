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
