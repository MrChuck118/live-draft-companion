"""Validators for AI suggestion output (M2/T15+)."""

from __future__ import annotations

import re

from pydantic import ValidationError
from sqlalchemy import select

from app.db import AsyncSessionLocal, Champion, Item, Rune
from app.models import DraftState, SuggestionOutput


def validator_format(json_string: str) -> tuple[bool, SuggestionOutput | str]:
    """Parse a JSON string into SuggestionOutput; return (True, model) or (False, error)."""
    try:
        parsed = SuggestionOutput.model_validate_json(json_string)
    except ValidationError as exc:
        return False, str(exc)
    return True, parsed


async def _load_champion_names() -> set[str]:
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(Champion.name))).scalars().all()
    return set(rows)


async def validator_champion_legality(
    suggestion: SuggestionOutput,
    draft_state: DraftState,
) -> tuple[bool, str | None]:
    """Check that suggested champions exist in Data Dragon and are not banned/picked."""
    known = await _load_champion_names()
    banned = {ban for ban in draft_state.bans if ban}
    enemy_picks = {pick.champion for pick in draft_state.enemy_team if pick.champion}
    ally_picks = {pick.champion for pick in draft_state.ally_team if pick.champion}

    for item in suggestion.suggestions:
        champ = item.champion
        if champ not in known:
            return False, f"champion '{champ}' not in Data Dragon cache"
        if champ in banned:
            return False, f"champion '{champ}' is banned"
        if champ in enemy_picks:
            return False, f"champion '{champ}' already picked by enemy"
        if champ in ally_picks:
            return False, f"champion '{champ}' already picked by ally"
    return True, None


async def _load_item_names() -> set[str]:
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(Item.name))).scalars().all()
    return set(rows)


async def validator_items_legality(
    suggestion: SuggestionOutput,
) -> tuple[bool, str | None]:
    """Check that every item in every build_path exists in Data Dragon cache."""
    known = await _load_item_names()
    for sugg in suggestion.suggestions:
        for item_name in sugg.build_path:
            if item_name not in known:
                return False, f"item '{item_name}' not in Data Dragon cache"
    return True, None


async def _load_keystone_names() -> set[str]:
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(Rune.name))).scalars().all()
    return set(rows)


async def validator_keystone_legality(
    suggestion: SuggestionOutput,
) -> tuple[bool, str | None]:
    """Check that every suggestion keystone exists in the cached Data Dragon keystones."""
    known = await _load_keystone_names()
    for sugg in suggestion.suggestions:
        if sugg.keystone not in known:
            return False, f"keystone '{sugg.keystone}' not in Data Dragon keystones"
    return True, None


def validator_explanation_length(
    suggestion: SuggestionOutput,
) -> tuple[bool, str | None]:
    """Defense-in-depth length check on the AI explanation field."""
    for sugg in suggestion.suggestions:
        if len(sugg.explanation) > 150:
            return False, f"explanation len {len(sugg.explanation)} > 150"
    return True, None


MOJIBAKE_RE = re.compile(r"Ã(Â|[ -¿])")


def validator_utf8_encoding(
    suggestion: SuggestionOutput,
) -> tuple[bool, str | None]:
    """Detect UTF-8 mojibake in every string field of the suggestion output."""
    if MOJIBAKE_RE.search(suggestion.patch):
        return False, f"mojibake in patch: {suggestion.patch!r}"
    for sugg in suggestion.suggestions:
        for label, value in (
            ("champion", sugg.champion),
            ("keystone", sugg.keystone),
            ("explanation", sugg.explanation),
        ):
            if MOJIBAKE_RE.search(value):
                return False, f"mojibake in {label}: {value!r}"
        for idx, item in enumerate(sugg.build_path):
            if MOJIBAKE_RE.search(item):
                return False, f"mojibake in build_path[{idx}]: {item!r}"
    return True, None


ITALIAN_WORDS: frozenset[str] = frozenset(
    {"il", "la", "di", "e", "che", "per", "con", "non", "su", "del", "della", "anche", "molto"}
)

_WORD_RE = re.compile(r"[a-zA-Z']+")


def _count_italian_words(text: str) -> int:
    return sum(1 for token in _WORD_RE.findall(text.lower()) if token in ITALIAN_WORDS)


def validator_language(
    suggestion: SuggestionOutput,
) -> tuple[bool, str | None]:
    """Heuristic check: each explanation must contain >=3 Italian marker words."""
    for sugg in suggestion.suggestions:
        count = _count_italian_words(sugg.explanation)
        if count < 3:
            return False, f"explanation has {count} Italian markers (need >=3)"
    return True, None
