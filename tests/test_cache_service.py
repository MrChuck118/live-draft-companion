"""Tests for CacheService get/set (M7a/T51)."""

from datetime import timedelta

import pytest

from app.db import AsyncSessionLocal, CacheEntry, init_db
from app.models import SuggestionItem, SuggestionOutput
from app.suggestion_service import CacheService

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
