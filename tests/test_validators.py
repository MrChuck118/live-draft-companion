"""Unit tests for validators (M2/T22)."""

from __future__ import annotations

import json

import pytest

from app.models import DraftState, SuggestionItem, SuggestionOutput
from app.validators import (
    validator_champion_legality,
    validator_explanation_length,
    validator_format,
    validator_items_legality,
    validator_keystone_legality,
    validator_language,
    validator_utf8_encoding,
)


def _suggestion(rank=1, champion="Garen", build=None, keystone="Conqueror", explanation="ok"):
    return SuggestionItem(
        rank=rank,
        champion=champion,
        build_path=build or ["A", "B", "C"],
        keystone=keystone,
        explanation=explanation,
    )


def _make_so(items):
    return SuggestionOutput(patch="16.10.1", suggestions=items)


def _draft_state(bans=None, enemy=None, ally=None):
    return DraftState(
        patch="16.10.1",
        user_role="MID",
        bans=bans or ["", "", "", "", ""],
        enemy_team=enemy or [],
        ally_team=ally or [],
        actions=[],
        local_player_cell_id=2,
    )


def test_format_positive_valid_json():
    so = _make_so([_suggestion(rank=i, explanation="Pick per la lane") for i in (1, 2, 3)])
    ok, parsed = validator_format(so.model_dump_json())
    assert ok is True
    assert isinstance(parsed, SuggestionOutput)


def test_format_positive_build_4_items():
    so = _make_so([_suggestion(rank=i, build=["A", "B", "C", "D"]) for i in (1, 2, 3)])
    ok, parsed = validator_format(so.model_dump_json())
    assert ok is True
    assert isinstance(parsed, SuggestionOutput)


def test_format_negative_missing_patch():
    bad = json.dumps({"suggestions": []})
    ok, err = validator_format(bad)
    assert ok is False
    assert isinstance(err, str)


def test_format_negative_empty_suggestions():
    bad = json.dumps({"patch": "16.10.1", "suggestions": []})
    ok, err = validator_format(bad)
    assert ok is False
    assert isinstance(err, str)


@pytest.mark.asyncio
async def test_champion_legality_positive_clean():
    so = _make_so([
        _suggestion(rank=1, champion="Ahri"),
        _suggestion(rank=2, champion="Syndra"),
        _suggestion(rank=3, champion="Orianna"),
    ])
    ds = _draft_state(bans=["Yasuo", "", "", "", ""])
    ok, err = await validator_champion_legality(so, ds)
    assert ok is True
    assert err is None


@pytest.mark.asyncio
async def test_champion_legality_positive_with_other_bans():
    so = _make_so([
        _suggestion(rank=1, champion="Ahri"),
        _suggestion(rank=2, champion="Syndra"),
        _suggestion(rank=3, champion="Orianna"),
    ])
    ds = _draft_state(bans=["Yasuo", "Zed", "Akali", "", ""])
    ok, err = await validator_champion_legality(so, ds)
    assert ok is True


@pytest.mark.asyncio
async def test_champion_legality_negative_banned_champion():
    so = _make_so([
        _suggestion(rank=1, champion="Yasuo"),
        _suggestion(rank=2, champion="Syndra"),
        _suggestion(rank=3, champion="Orianna"),
    ])
    ds = _draft_state(bans=["Yasuo", "", "", "", ""])
    ok, err = await validator_champion_legality(so, ds)
    assert ok is False
    assert "Yasuo" in err


@pytest.mark.asyncio
async def test_champion_legality_negative_unknown_champion():
    so = _make_so([
        _suggestion(rank=1, champion="Invokerito"),
        _suggestion(rank=2, champion="Syndra"),
        _suggestion(rank=3, champion="Orianna"),
    ])
    ds = _draft_state()
    ok, err = await validator_champion_legality(so, ds)
    assert ok is False
    assert "Invokerito" in err


LIANDRY = "Liandry" + chr(39) + "s Torment"
LUDEN = "Luden" + chr(39) + "s Echo"


@pytest.mark.asyncio
async def test_items_legality_positive_same_item():
    so = _make_so([_suggestion(rank=i, build=[LIANDRY, LIANDRY, LIANDRY]) for i in (1, 2, 3)])
    ok, err = await validator_items_legality(so)
    assert ok is True


@pytest.mark.asyncio
async def test_items_legality_positive_mixed_items():
    so = _make_so([_suggestion(rank=i, build=[LIANDRY, LUDEN, LIANDRY]) for i in (1, 2, 3)])
    ok, err = await validator_items_legality(so)
    assert ok is True


@pytest.mark.asyncio
async def test_items_legality_negative_italian_name():
    so = _make_so([
        _suggestion(rank=i, build=[LIANDRY, "Tormento di Liandry", LIANDRY])
        for i in (1, 2, 3)
    ])
    ok, err = await validator_items_legality(so)
    assert ok is False
    assert "Tormento di Liandry" in err


@pytest.mark.asyncio
async def test_items_legality_negative_unknown_item():
    so = _make_so([
        _suggestion(rank=i, build=[LIANDRY, "Pizza Margherita", LIANDRY])
        for i in (1, 2, 3)
    ])
    ok, err = await validator_items_legality(so)
    assert ok is False
    assert "Pizza Margherita" in err


@pytest.mark.asyncio
async def test_keystone_legality_positive_conqueror():
    so = _make_so([_suggestion(rank=i, keystone="Conqueror") for i in (1, 2, 3)])
    ok, err = await validator_keystone_legality(so)
    assert ok is True


@pytest.mark.asyncio
async def test_keystone_legality_positive_electrocute():
    so = _make_so([_suggestion(rank=i, keystone="Electrocute") for i in (1, 2, 3)])
    ok, err = await validator_keystone_legality(so)
    assert ok is True


@pytest.mark.asyncio
async def test_keystone_legality_negative_italian():
    so = _make_so([_suggestion(rank=i, keystone="Cometa Arcana") for i in (1, 2, 3)])
    ok, err = await validator_keystone_legality(so)
    assert ok is False


@pytest.mark.asyncio
async def test_keystone_legality_negative_minor_rune():
    so = _make_so([_suggestion(rank=i, keystone="Manaflow Band") for i in (1, 2, 3)])
    ok, err = await validator_keystone_legality(so)
    assert ok is False


def test_explanation_length_positive_100_chars():
    so = _make_so([_suggestion(rank=i, explanation="x" * 100) for i in (1, 2, 3)])
    ok, err = validator_explanation_length(so)
    assert ok is True


def test_explanation_length_positive_exact_150():
    so = _make_so([_suggestion(rank=i, explanation="x" * 150) for i in (1, 2, 3)])
    ok, err = validator_explanation_length(so)
    assert ok is True


def test_explanation_length_negative_200_chars():
    bad_item = SuggestionItem.model_construct(
        rank=1,
        champion="Garen",
        build_path=["A", "B", "C"],
        keystone="Conqueror",
        explanation="x" * 200,
    )
    so = SuggestionOutput.model_construct(patch="16.10.1", suggestions=[bad_item] * 3)
    ok, err = validator_explanation_length(so)
    assert ok is False


def test_explanation_length_negative_151_chars():
    bad_item = SuggestionItem.model_construct(
        rank=1,
        champion="Garen",
        build_path=["A", "B", "C"],
        keystone="Conqueror",
        explanation="x" * 151,
    )
    so = SuggestionOutput.model_construct(patch="16.10.1", suggestions=[bad_item] * 3)
    ok, err = validator_explanation_length(so)
    assert ok is False


CLEAN_E_GRAVE = chr(0x00E8)
MOJIBAKE_DOUBLE = chr(0x00C3) + chr(0x00C2) + chr(0x00A8)
MOJIBAKE_SINGLE_O = chr(0x00C3) + chr(0x00B2)


def test_utf8_positive_clean_italian():
    so = _make_so([
        _suggestion(rank=i, explanation="Orianna " + CLEAN_E_GRAVE + " immobile")
        for i in (1, 2, 3)
    ])
    ok, err = validator_utf8_encoding(so)
    assert ok is True


def test_utf8_positive_ascii_only():
    so = _make_so([
        _suggestion(rank=i, explanation="Plain ascii text only") for i in (1, 2, 3)
    ])
    ok, err = validator_utf8_encoding(so)
    assert ok is True


def test_utf8_negative_double_mojibake():
    so = _make_so([
        _suggestion(rank=i, explanation="Orianna " + MOJIBAKE_DOUBLE + " immobile")
        for i in (1, 2, 3)
    ])
    ok, err = validator_utf8_encoding(so)
    assert ok is False


def test_utf8_negative_single_mojibake():
    so = _make_so([
        _suggestion(rank=i, explanation="Ottimo " + MOJIBAKE_SINGLE_O + " contro tank")
        for i in (1, 2, 3)
    ])
    ok, err = validator_utf8_encoding(so)
    assert ok is False


def test_language_positive_four_markers():
    so = _make_so([
        _suggestion(rank=i, explanation="Counter forte e molto utile per la lane")
        for i in (1, 2, 3)
    ])
    ok, err = validator_language(so)
    assert ok is True


def test_language_positive_five_markers():
    so = _make_so([
        _suggestion(rank=i, explanation="Il pick e molto buono per la composizione del team")
        for i in (1, 2, 3)
    ])
    ok, err = validator_language(so)
    assert ok is True


def test_language_negative_english():
    so = _make_so([
        _suggestion(rank=i, explanation="Strong against high-mobility champions")
        for i in (1, 2, 3)
    ])
    ok, err = validator_language(so)
    assert ok is False


def test_language_negative_too_few_markers():
    so = _make_so([
        _suggestion(rank=i, explanation="Buon pick lane") for i in (1, 2, 3)
    ])
    ok, err = validator_language(so)
    assert ok is False
