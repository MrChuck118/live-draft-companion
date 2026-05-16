"""Cache (and later orchestration) for AI suggestions (M7a).

T51 adds CacheService here. T45b will add the SuggestionService orchestrator
to this same module. CacheService lives here (NOT in ai_client.py) on
purpose: ai_client must not know the DraftState domain (SoC, breakdown v2.1).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db import AsyncSessionLocal, CacheEntry, HistoryEntry
from app.models import DraftState, SuggestionOutput

DEFAULT_TTL = timedelta(days=30)  # spec Â§8.3 "Cache output AI ... 30 giorni"


def _utcnow_naive() -> datetime:
    """Naive UTC. SQLite returns naive datetimes on read; comparing naive vs
    naive avoids the aware/naive TypeError. Used only inside CacheService.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class CacheService:
    """Local AI-output cache keyed by draft-state hash (MVP-010, RF-015)."""

    def __init__(self, session_factory=AsyncSessionLocal) -> None:
        self._session_factory = session_factory

    async def get(self, draft_state_hash: str) -> SuggestionOutput | None:
        """Return the cached SuggestionOutput, or None if absent or expired."""
        async with self._session_factory() as session:
            entry = await session.get(CacheEntry, draft_state_hash)
            if entry is None:
                return None
            if entry.expires_at <= _utcnow_naive():
                return None
            return SuggestionOutput.model_validate_json(entry.output_json)

    async def set(
        self,
        draft_state_hash: str,
        output: SuggestionOutput,
        model_used: str,
        ttl: timedelta = DEFAULT_TTL,
    ) -> None:
        """Upsert the cached output with a TTL (default 30 days)."""
        now = _utcnow_naive()
        async with self._session_factory() as session:
            async with session.begin():
                await session.merge(
                    CacheEntry(
                        draft_state_hash=draft_state_hash,
                        output_json=output.model_dump_json(),
                        model_used=model_used,
                        created_at=now,
                        expires_at=now + ttl,
                    )
                )


class HistoryRepository:
    """Local history of generated suggestions with user feedback (MVP-014, RF-016)."""

    def __init__(self, session_factory=AsyncSessionLocal) -> None:
        self._session_factory = session_factory

    async def save(
        self,
        draft_state: DraftState,
        output: SuggestionOutput,
        model_used: str,
    ) -> int:
        """Persist one generated suggestion with feedback='unrated'. Returns its id."""
        entry = HistoryEntry(
            timestamp=_utcnow_naive(),
            draft_state_json=draft_state.model_dump_json(),
            output_json=output.model_dump_json(),
            model_used=model_used,
            feedback="unrated",
        )
        async with self._session_factory() as session:
            async with session.begin():
                session.add(entry)
            # AsyncSessionLocal uses expire_on_commit=False, so the
            # autoincrement id assigned at flush stays available post-commit.
            return entry.id
