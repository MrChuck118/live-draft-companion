"""T59 cache-hit integration check.

Run the same sim scenario twice. The first run should call the AI and populate
the cache; the second run should be served from cache and add zero new
`logs/ai_calls_YYYY-MM-DD.jsonl` lines. SuggestionService logs "cache hit" on
the second run.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import delete

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ai_client import _LOGS_DIR  # noqa: E402
from app.data_dragon import check_patch_and_refresh  # noqa: E402
from app.db import AsyncSessionLocal, CacheEntry, init_db  # noqa: E402
from app.file_provider import FileProvider  # noqa: E402
from app.suggestion_service import SuggestionError, SuggestionService, draft_state_hash  # noqa: E402

MOCK_DRAFTS_DIR = ROOT / "tests" / "mock_drafts"


def _daily_ai_log_path() -> Path:
    return _LOGS_DIR / f"ai_calls_{datetime.now().strftime('%Y-%m-%d')}.jsonl"


def _line_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8").splitlines())


async def _clear_cache_for_hash(state_hash: str) -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                delete(CacheEntry).where(CacheEntry.draft_state_hash == state_hash)
            )


async def run_check(scenario: str) -> dict[str, object]:
    load_dotenv(ROOT / ".env")
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("DEEPSEEK_API_KEY not configured; cannot run T59")
    if not os.environ.get("LLM_MODEL_PRIMARY"):
        raise RuntimeError("LLM_MODEL_PRIMARY not configured; cannot run T59")

    await init_db()
    await check_patch_and_refresh("16.10.1")

    scenario_path = MOCK_DRAFTS_DIR / f"{scenario}.json"
    draft = await FileProvider(scenario_path).get_current_state()
    state_hash = draft_state_hash(draft)
    await _clear_cache_for_hash(state_hash)

    log_path = _daily_ai_log_path()
    before = _line_count(log_path)
    service = SuggestionService()

    error: str | None = None
    try:
        await service.suggest(draft)
    except SuggestionError as exc:
        error = f"{exc.error_code}: {exc}"
    after_first = _line_count(log_path)

    if error is not None:
        return {
            "scenario": scenario,
            "draft_state_hash": state_hash,
            "ai_log_path": str(log_path),
            "ai_calls_first_run": after_first - before,
            "ai_calls_second_run": None,
            "ok": False,
            "error": error,
        }

    await service.suggest(draft)
    after_second = _line_count(log_path)

    first_delta = after_first - before
    second_delta = after_second - after_first
    ok = first_delta >= 1 and second_delta == 0
    return {
        "scenario": scenario,
        "draft_state_hash": state_hash,
        "ai_log_path": str(log_path),
        "ai_calls_first_run": first_delta,
        "ai_calls_second_run": second_delta,
        "ok": ok,
        "error": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run T59 cache-hit integration check.")
    parser.add_argument("--scenario", default="last_pick_support")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    report = asyncio.run(run_check(args.scenario))
    print(f"[cache_hit] scenario={report['scenario']}")
    print(f"[cache_hit] draft_state_hash={report['draft_state_hash']}")
    print(f"[cache_hit] ai_calls_first_run={report['ai_calls_first_run']}")
    print(f"[cache_hit] ai_calls_second_run={report['ai_calls_second_run']}")
    if report.get("error"):
        print(f"[cache_hit] error={report['error']}")
    print(f"[cache_hit] ok={report['ok']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
