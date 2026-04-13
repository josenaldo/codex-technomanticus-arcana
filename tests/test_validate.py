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
