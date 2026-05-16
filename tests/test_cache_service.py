"""Tests for CacheService get/set (M7a/T51) + persistence/TTL (M7a/T52)."""

import sqlite3
from datetime import timedelta

import pytest

from app.db import AsyncSessionLocal, CacheEntry, init_db
from app.models import SuggestionItem, SuggestionOutput
from app.suggestion_service import DEFAULT_TTL, CacheService

_TEST_HASH = "t51-test-hash-do-not-collide"


def _sample_output() -> SuggestionOutput:
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


async def _cleanup() -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            entry = await session.get(CacheEntry, _TEST_HASH)
            if entry is not None:
                await session.delete(entry)


@pytest.mark.asyncio
async def test_get_absent_returns_none() -> None:
    await init_db()
    await _cleanup()
    try:
        assert await CacheService().get(_TEST_HASH) is None
    finally:
        await _cleanup()


@pytest.mark.asyncio
async def test_set_then_get_roundtrip() -> None:
    await init_db()
    await _cleanup()
    try:
        service = CacheService()
        output = _sample_output()
        await service.set(_TEST_HASH, output, model_used="deepseek-chat")

        cached = await service.get(_TEST_HASH)
        assert cached is not None
        assert cached.model_dump() == output.model_dump()
    finally:
        await _cleanup()


@pytest.mark.asyncio
async def test_expired_entry_returns_none() -> None:
    await init_db()
    await _cleanup()
    try:
        service = CacheService()
        await service.set(
            _TEST_HASH,
            _sample_output(),
            model_used="deepseek-chat",
            ttl=timedelta(seconds=-1),
        )
        assert await service.get(_TEST_HASH) is None
    finally:
        await _cleanup()


# --- T52: cache save post-call (persistence + 30d TTL) ---


@pytest.mark.asyncio
async def test_set_default_ttl_is_30_days() -> None:
    """DoD T52: set() without ttl writes a row with a ~30-day TTL (spec §8.3)."""
    await init_db()
    await _cleanup()
    try:
        await CacheService().set(_TEST_HASH, _sample_output(), model_used="deepseek-chat")

        async with AsyncSessionLocal() as session:
            entry = await session.get(CacheEntry, _TEST_HASH)
            assert entry is not None
            assert entry.model_used == "deepseek-chat"
            assert entry.expires_at - entry.created_at == DEFAULT_TTL
            assert DEFAULT_TTL == timedelta(days=30)
    finally:
        await _cleanup()


@pytest.mark.asyncio
async def test_cache_persists_on_disk() -> None:
    """DoD T52: the cache row survives a 'restart' (it is on disk, not in-memory)."""
    await init_db()
    await _cleanup()
    try:
        output = _sample_output()
        await CacheService().set(_TEST_HASH, output, model_used="deepseek-chat")

        # Raw read via a fresh sqlite3 connection: proves it is persisted to
        # data_dragon.db, independent of the SQLAlchemy session/engine.
        connection = sqlite3.connect("data_dragon.db")
        try:
            row = connection.execute(
                "SELECT output_json, model_used FROM cache WHERE draft_state_hash = ?",
                (_TEST_HASH,),
            ).fetchone()
        finally:
            connection.close()

        assert row is not None
        assert row[1] == "deepseek-chat"

        # A brand-new CacheService instance (simulated restart) still reads it.
        cached = await CacheService().get(_TEST_HASH)
        assert cached is not None
        assert cached.model_dump() == output.model_dump()
    finally:
        await _cleanup()
