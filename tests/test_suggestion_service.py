"""Tests for SuggestionService orchestrator (M7a/T45b).

AI call is mocked (no real network/model: Demo Mode First / OPEN-001).
"""

from types import SimpleNamespace

import pytest
from sqlalchemy import select

from app.db import AsyncSessionLocal, CacheEntry, Champion, HistoryEntry, Item, Rune, init_db
from app.models import ChampionPick, DraftState, SuggestionItem, SuggestionOutput
from app.suggestion_service import (
    CacheService,
    HistoryRepository,
    SuggestionError,
    SuggestionService,
    draft_state_hash,
)

SENTINEL_MODEL = "t45b-test-model"
BAN_POOL = ["Yasuo", "Zed", "Yone", "Akali", "Sylas"]
EXPL = "Buona scelta per la corsia e il controllo con la squadra."


def _draft(user_role: str = "MID") -> DraftState:
    return DraftState(
        patch="16.10.1",
        user_role=user_role,
        bans=BAN_POOL,
        enemy_team=[ChampionPick(role="TOP", champion=None)],
        ally_team=[ChampionPick(role="MID", champion=None)],
        actions=[],
        local_player_cell_id=2,
    )


async def _valid_output() -> SuggestionOutput:
    async with AsyncSessionLocal() as session:
        champs = (await session.execute(select(Champion.name))).scalars().all()
        items = (await session.execute(select(Item.name))).scalars().all()
        runes = (await session.execute(select(Rune.name))).scalars().all()

    chosen_champs = [c for c in sorted(champs) if c not in BAN_POOL][:3]
    chosen_items = sorted(items)[:3]
    keystone = sorted(runes)[0]

    return SuggestionOutput(
        patch="16.10.1",
        suggestions=[
            SuggestionItem(
                rank=i + 1,
                champion=chosen_champs[i],
                build_path=chosen_items,
                keystone=keystone,
                explanation=EXPL,
            )
            for i in range(3)
        ],
    )


def _fake_response(content: str):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        model=SENTINEL_MODEL,
    )


async def _cleanup(state_hash: str) -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            entry = await session.get(CacheEntry, state_hash)
            if entry is not None:
                await session.delete(entry)
            rows = (
                await session.execute(
                    select(HistoryEntry).where(HistoryEntry.model_used == SENTINEL_MODEL)
                )
            ).scalars().all()
            for row in rows:
                await session.delete(row)


@pytest.mark.asyncio
async def test_cache_miss_calls_ai_caches_and_saves_history() -> None:
    await init_db()
    draft = _draft()
    state_hash = draft_state_hash(draft)
    await _cleanup(state_hash)
    calls: list[tuple[str, str]] = []
    try:
        output = await _valid_output()

        def fake_ai(system: str, user: str):
            calls.append((system, user))
            return _fake_response(output.model_dump_json())

        service = SuggestionService(ai_call=fake_ai)
        result = await service.suggest(draft)

        assert len(calls) == 1
        assert isinstance(result, SuggestionOutput)
        assert result.model_dump() == output.model_dump()

        async with AsyncSessionLocal() as session:
            cache_row = await session.get(CacheEntry, state_hash)
            assert cache_row is not None
            assert cache_row.model_used == SENTINEL_MODEL
            hist = (
                await session.execute(
                    select(HistoryEntry).where(HistoryEntry.model_used == SENTINEL_MODEL)
                )
            ).scalars().all()
            assert len(hist) == 1
            assert hist[0].feedback == "unrated"
    finally:
        await _cleanup(state_hash)


@pytest.mark.asyncio
async def test_cache_hit_no_ai_call() -> None:
    await init_db()
    draft = _draft("ADC")
    state_hash = draft_state_hash(draft)
    await _cleanup(state_hash)
    try:
        output = await _valid_output()
        await CacheService().set(state_hash, output, model_used=SENTINEL_MODEL)

        def fail_ai(system: str, user: str):
            raise AssertionError("AI must not be called on a cache hit")

        service = SuggestionService(ai_call=fail_ai)
        result = await service.suggest(draft)

        assert result.model_dump() == output.model_dump()
        async with AsyncSessionLocal() as session:
            hist = (
                await session.execute(
                    select(HistoryEntry).where(HistoryEntry.model_used == SENTINEL_MODEL)
                )
            ).scalars().all()
            assert len(hist) == 1
            assert hist[0].feedback == "unrated"
    finally:
        await _cleanup(state_hash)


@pytest.mark.asyncio
async def test_chain_exhausted_raises_suggestion_error() -> None:
    await init_db()
    draft = _draft()
    await _cleanup(draft_state_hash(draft))

    def boom(system: str, user: str):
        raise RuntimeError("AI chain exhausted after trying 2 models")

    with pytest.raises(SuggestionError):
        await SuggestionService(ai_call=boom).suggest(draft)


@pytest.mark.asyncio
async def test_invalid_ai_output_raises_suggestion_error() -> None:
    await init_db()
    draft = _draft()
    await _cleanup(draft_state_hash(draft))

    def bad(system: str, user: str):
        return _fake_response("not a valid json output")

    with pytest.raises(SuggestionError):
        await SuggestionService(ai_call=bad).suggest(draft)


def test_draft_state_hash_deterministic() -> None:
    a = _draft("MID")
    b = _draft("MID")
    c = _draft("TOP")
    assert draft_state_hash(a) == draft_state_hash(b)
    assert draft_state_hash(a) != draft_state_hash(c)


@pytest.mark.asyncio
async def test_no_personal_data_in_records() -> None:
    await init_db()
    draft = _draft()
    state_hash = draft_state_hash(draft)
    await _cleanup(state_hash)
    try:
        output = await _valid_output()
        service = SuggestionService(ai_call=lambda s, u: _fake_response(output.model_dump_json()))
        await service.suggest(draft)

        async with AsyncSessionLocal() as session:
            cache_row = await session.get(CacheEntry, state_hash)
            hist = (
                await session.execute(
                    select(HistoryEntry).where(HistoryEntry.model_used == SENTINEL_MODEL)
                )
            ).scalars().all()

        blob = (cache_row.output_json + hist[0].draft_state_json + hist[0].output_json).lower()
        for forbidden in ("summoner", "gamename", "displayname", "api_key", "deepseek_api_key"):
            assert forbidden not in blob
    finally:
        await _cleanup(state_hash)
