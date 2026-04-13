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
