"""Tests for HistoryRepository.save (M7a/T53)."""

import pytest

from app.db import AsyncSessionLocal, HistoryEntry, init_db
from app.models import ChampionPick, DraftState, SuggestionItem, SuggestionOutput
from app.suggestion_service import HistoryRepository


def _draft(role: str) -> DraftState:
    return DraftState(
        patch="16.10.1",
        user_role=role,
        bans=["Yasuo", "Zed", "Yone", "Akali", "Sylas"],
        enemy_team=[ChampionPick(role="TOP", champion="Ornn")],
        ally_team=[ChampionPick(role=role, champion=None)],
        actions=[],
        local_player_cell_id=2,
    )


def _output() -> SuggestionOutput:
    return SuggestionOutput(
        patch="16.10.1",
        suggestions=[
            SuggestionItem(
                rank=i,
                champion=f"Champ{i}",
                build_path=["Item A", "Item B", "Item C"],
                keystone="Conqueror",
                explanation="Buona scelta per il draft.",
            )
            for i in range(1, 4)
        ],
    )


async def _delete(ids: list[int]) -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            for history_id in ids:
                row = await session.get(HistoryEntry, history_id)
                if row is not None:
                    await session.delete(row)


@pytest.mark.asyncio
async def test_save_three_rows_unrated_with_model_used() -> None:
    """DoD T53: 3 saves -> 3 rows, feedback='unrated', model_used populated."""
    await init_db()
    repo = HistoryRepository()
    ids: list[int] = []
    try:
        for role in ("TOP", "MID", "ADC"):
            ids.append(await repo.save(_draft(role), _output(), model_used="deepseek-chat"))

        assert len(ids) == 3
        assert len(set(ids)) == 3

        async with AsyncSessionLocal() as session:
            for history_id in ids:
                row = await session.get(HistoryEntry, history_id)
                assert row is not None
                assert row.feedback == "unrated"
                assert row.model_used == "deepseek-chat"
    finally:
        await _delete(ids)


@pytest.mark.asyncio
async def test_saved_json_roundtrips() -> None:
    """draft_state_json / output_json are parseable back into the models."""
    await init_db()
    repo = HistoryRepository()
    ids: list[int] = []
    try:
        draft = _draft("MID")
        output = _output()
        history_id = await repo.save(draft, output, model_used="deepseek-reasoner")
        ids.append(history_id)

        async with AsyncSessionLocal() as session:
            row = await session.get(HistoryEntry, history_id)
            assert row is not None
            assert DraftState.model_validate_json(row.draft_state_json) == draft
            assert SuggestionOutput.model_validate_json(row.output_json) == output
    finally:
        await _delete(ids)


@pytest.mark.asyncio
async def test_update_feedback_changes_row() -> None:
    """DoD T54 repository: update feedback to good/bad on an existing row."""
    await init_db()
    repo = HistoryRepository()
    ids: list[int] = []
    try:
        history_id = await repo.save(_draft("SUPPORT"), _output(), model_used="t54-model")
        ids.append(history_id)

        assert await repo.update_feedback(history_id, "good") is True
        async with AsyncSessionLocal() as session:
            row = await session.get(HistoryEntry, history_id)
            assert row is not None
            assert row.feedback == "good"

        assert await repo.update_feedback(history_id, "bad") is True
        async with AsyncSessionLocal() as session:
            row = await session.get(HistoryEntry, history_id)
            assert row is not None
            assert row.feedback == "bad"
    finally:
        await _delete(ids)


@pytest.mark.asyncio
async def test_update_feedback_missing_or_invalid() -> None:
    """Missing row returns False; invalid values are rejected defensively."""
    await init_db()
    repo = HistoryRepository()

    assert await repo.update_feedback(999_999_999, "good") is False

    with pytest.raises(ValueError):
        await repo.update_feedback(999_999_999, "unrated")
