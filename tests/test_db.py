"""Tests for app.db cache + history tables (M7a/T50)."""

import pytest
from sqlalchemy import inspect

from app.db import engine, init_db


@pytest.mark.asyncio
async def test_init_db_creates_cache_and_history_tables() -> None:
    """DoD T50: init_db() creates the `cache` and `history` tables with the spec columns."""
    await init_db()

    def _columns(connection):
        inspector = inspect(connection)
        return {
            table: {col["name"] for col in inspector.get_columns(table)}
            for table in inspector.get_table_names()
        }

    async with engine.connect() as connection:
        columns = await connection.run_sync(_columns)

    assert "cache" in columns
    assert columns["cache"] == {
        "draft_state_hash",
        "output_json",
        "model_used",
        "created_at",
        "expires_at",
    }

    assert "history" in columns
    assert columns["history"] == {
        "id",
        "timestamp",
        "draft_state_json",
        "output_json",
        "model_used",
        "feedback",
    }


@pytest.mark.asyncio
async def test_history_feedback_defaults_to_unrated() -> None:
    """history.feedback initializes to 'unrated' (MVP-014/RF-016)."""
    from datetime import datetime, timezone

    from app.db import AsyncSessionLocal, HistoryEntry

    await init_db()
    async with AsyncSessionLocal() as session:
        entry = HistoryEntry(
            timestamp=datetime.now(timezone.utc),
            draft_state_json="{}",
            output_json="{}",
            model_used="deepseek-chat",
        )
        session.add(entry)
        await session.commit()
        await session.refresh(entry)
        created_id = entry.id
        assert entry.feedback == "unrated"

        await session.delete(await session.get(HistoryEntry, created_id))
        await session.commit()
