"""Cache, history and the SuggestionService orchestrator (M7a).

T51 CacheService, T53 HistoryRepository, T45b SuggestionService all live here.
CacheService/SuggestionService live here (NOT in ai_client.py) on purpose:
ai_client must not know the DraftState domain (SoC, breakdown v2.1).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone

from app.ai_client import get_suggestions_with_fallback
from app.db import AsyncSessionLocal, CacheEntry, HistoryEntry
from app.models import DraftState, SuggestionOutput
from app.prompt_builder import build_prompt
from app.validators import (
    validator_champion_legality,
    validator_explanation_length,
    validator_format,
    validator_items_legality,
    validator_keystone_legality,
    validator_language,
    validator_utf8_encoding,
)


class SuggestionError(RuntimeError):
    """Controlled failure of the suggestion flow (no stack trace to the user).

    `error_code` drives the HTTP mapping in app.main (T49b):
    - "ai_unavailable": AI chain exhausted / service unreachable
    - "ai_output_invalid": AI output invalid/mojibake/illegal after retries
    """

    def __init__(self, message: str, error_code: str = "ai_unavailable") -> None:
        super().__init__(message)
        self.error_code = error_code


def draft_state_hash(draft_state: DraftState) -> str:
    """Deterministic hash of the semantically relevant draft content.

    Spec: "hash su ban+pick+role". `actions` and `local_player_cell_id` are
    intentionally excluded (volatile, not part of the suggestion input).
    """
    payload = {
        "patch": draft_state.patch,
        "user_role": draft_state.user_role,
        "bans": draft_state.bans,
        "enemy_team": [pick.model_dump() for pick in draft_state.enemy_team],
        "ally_team": [pick.model_dump() for pick in draft_state.ally_team],
    }
    canonical = json.dumps(
        payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

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

    async def get_with_model(
        self, draft_state_hash: str
    ) -> tuple[SuggestionOutput, str] | None:
        """Like get(), but also returns the cached model_used (T45b needs it
        to record history on a cache hit). Additive: does not change get()."""
        async with self._session_factory() as session:
            entry = await session.get(CacheEntry, draft_state_hash)
            if entry is None:
                return None
            if entry.expires_at <= _utcnow_naive():
                return None
            output = SuggestionOutput.model_validate_json(entry.output_json)
            return output, entry.model_used

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


class SuggestionService:
    """Orchestrates the full suggestion flow (M7a/T45b).

    DraftState -> hash -> cache lookup -> (miss) prompt -> AI chain ->
    validate -> save cache + history -> SuggestionOutput. Keeps /api/suggest
    thin (T45) and ai_client free of the DraftState domain (SoC).
    """

    def __init__(
        self,
        cache: CacheService | None = None,
        history: HistoryRepository | None = None,
        ai_call=get_suggestions_with_fallback,
    ) -> None:
        self._cache = cache or CacheService()
        self._history = history or HistoryRepository()
        self._ai_call = ai_call

    async def suggest(self, draft_state: DraftState) -> SuggestionOutput:
        """Return Top-3 suggestions for the draft, using cache when possible."""
        state_hash = draft_state_hash(draft_state)

        cached = await self._cache.get_with_model(state_hash)
        if cached is not None:
            output, model_used = cached
            await self._history.save(draft_state, output, model_used)
            return output

        system, user = build_prompt(draft_state, {})
        try:
            response = self._ai_call(system, user)
        except RuntimeError as exc:
            raise SuggestionError(
                f"Servizio AI non disponibile: {exc}", error_code="ai_unavailable"
            ) from exc

        content = response.choices[0].message.content
        ok, parsed = validator_format(content)
        if not ok:
            raise SuggestionError(
                f"Output AI non valido: {parsed}", error_code="ai_output_invalid"
            )
        output = parsed  # SuggestionOutput
        model_used = getattr(response, "model", "") or ""

        await self._run_legality_gate(output, draft_state)

        await self._cache.set(state_hash, output, model_used)
        await self._history.save(draft_state, output, model_used)
        return output

    async def _run_legality_gate(
        self, output: SuggestionOutput, draft_state: DraftState
    ) -> None:
        """Legality/quality gate. On failure raise a controlled SuggestionError.

        Scope T45b: gate only. Graceful remediation (default-item
        substitution, explanation truncation) is intentionally NOT here
        (not in T45b DoD; spec assigns it to the validators layer).
        """
        results = [
            await validator_champion_legality(output, draft_state),
            await validator_items_legality(output),
            await validator_keystone_legality(output),
            validator_explanation_length(output),
            validator_utf8_encoding(output),
            validator_language(output),
        ]
        for ok, error in results:
            if not ok:
                raise SuggestionError(
                    f"Validazione output fallita: {error}",
                    error_code="ai_output_invalid",
                )
