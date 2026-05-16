"""Run the T58 sim-mode benchmark: 15 mock drafts x 2 rounds = 30 calls.

The benchmark exercises the backend/sim flow (FileProvider -> SuggestionService
-> AI chain -> validators -> history) and intentionally bypasses the cache so
the second round still performs real AI calls. It does not depend on the UI.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ai_client import _LOGS_DIR  # noqa: E402
from app.data_dragon import check_patch_and_refresh  # noqa: E402
from app.db import init_db  # noqa: E402
from app.file_provider import FileProvider  # noqa: E402
from app.suggestion_service import (  # noqa: E402
    HistoryRepository,
    SuggestionError,
    SuggestionService,
)

MOCK_DRAFTS_DIR = ROOT / "tests" / "mock_drafts"
REPORTS_DIR = ROOT / "logs"
TARGET_P95_MS = 30_000


class BenchmarkNoCache:
    """Cache bypass for T58: every scenario call must hit the AI chain."""

    async def get(self, draft_state_hash: str):  # noqa: ARG002
        return None

    async def get_with_model(self, draft_state_hash: str):  # noqa: ARG002
        return None

    async def set(  # noqa: ANN001, ARG002
        self, draft_state_hash: str, output, model_used: str, ttl=None
    ):
        return None


@dataclass
class CallResult:
    scenario: str
    round_index: int
    ok: bool
    latency_ms: int
    model_used: str | None
    fallback_used: bool
    error_code: str | None
    error: str | None
    ai_log_records: int
    rate_limit_events: int
    timeout_events: int
    validation_failures: int
    prompt_tokens: int
    completion_tokens: int
    reported_cost: float | None


def _scenario_files() -> list[Path]:
    return sorted(MOCK_DRAFTS_DIR.glob("*.json"))


def _daily_ai_log_path() -> Path:
    date_str = datetime.now().strftime("%Y-%m-%d")
    return _LOGS_DIR / f"ai_calls_{date_str}.jsonl"


def _line_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8").splitlines())


def _read_new_ai_records(start_line_count: int) -> list[dict[str, Any]]:
    path = _daily_ai_log_path()
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()[start_line_count:]
    records: list[dict[str, Any]] = []
    for line in lines:
        if line.strip():
            records.append(json.loads(line))
    return records


def _sum_usage(records: list[dict[str, Any]], key: str) -> int:
    total = 0
    for record in records:
        usage = record.get("usage")
        if isinstance(usage, dict) and isinstance(usage.get(key), int):
            total += usage[key]
    return total


def _reported_cost(records: list[dict[str, Any]]) -> float | None:
    values = [
        record.get("cost")
        for record in records
        if isinstance(record.get("cost"), (int, float))
    ]
    if not values:
        return None
    return float(sum(values))


def _percentile(values: list[int], percentile: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, math.ceil((percentile / 100) * len(ordered)) - 1)
    return ordered[index]


def _summarize(
    results: list[CallResult], started_at: str, report_path: Path, rounds: int
) -> dict[str, Any]:
    latencies = [result.latency_ms for result in results]
    success_latencies = [result.latency_ms for result in results if result.ok]
    reported_costs = [
        result.reported_cost for result in results if result.reported_cost is not None
    ]
    primary_model = os.environ.get("LLM_MODEL_PRIMARY")
    fallback_count = sum(1 for result in results if result.fallback_used)
    success_count = sum(1 for result in results if result.ok)
    rate_limit_events = sum(result.rate_limit_events for result in results)
    timeout_events = sum(result.timeout_events for result in results)
    validation_failures = sum(result.validation_failures for result in results)
    p95_all = _percentile(latencies, 95)

    return {
        "task": "T58",
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "scenario_count": len(_scenario_files()),
        "rounds": rounds,
        "attempted_calls": len(results),
        "successful_calls": success_count,
        "error_calls": len(results) - success_count,
        "primary_model": primary_model,
        "fallback_call_count": fallback_count,
        "fallback_call_percent": round((fallback_count / len(results)) * 100, 2)
        if results
        else 0.0,
        "rate_limit_events": rate_limit_events,
        "timeout_events": timeout_events,
        "validation_failures": validation_failures,
        "latency_ms": {
            "p50_all": _percentile(latencies, 50),
            "p95_all": p95_all,
            "p50_success": _percentile(success_latencies, 50),
            "p95_success": _percentile(success_latencies, 95),
            "target_p95": TARGET_P95_MS,
            "target_met_all": p95_all is not None and p95_all <= TARGET_P95_MS,
        },
        "usage": {
            "prompt_tokens": sum(result.prompt_tokens for result in results),
            "completion_tokens": sum(result.completion_tokens for result in results),
        },
        "reported_cost_total": float(sum(reported_costs)) if reported_costs else None,
        "reported_cost_note": (
            "AI client logs cost=null because the DeepSeek/OpenAI-compatible "
            "ChatCompletion response used here does not expose billed cost."
        ),
        "report_path": str(report_path),
        "results": [asdict(result) for result in results],
    }


async def _run_one(
    scenario_path: Path,
    round_index: int,
    primary_model: str | None,
) -> CallResult:
    draft = await FileProvider(scenario_path).get_current_state()
    service = SuggestionService(cache=BenchmarkNoCache(), history=HistoryRepository())
    start_line_count = _line_count(_daily_ai_log_path())
    start = time.perf_counter()
    ok = False
    error_code: str | None = None
    error: str | None = None
    try:
        await service.suggest(draft)
        ok = True
    except SuggestionError as exc:
        error_code = exc.error_code
        error = str(exc)
    except Exception as exc:  # noqa: BLE001
        error_code = "unhandled"
        error = f"{type(exc).__name__}: {exc}"

    latency_ms = int((time.perf_counter() - start) * 1000)
    records = _read_new_ai_records(start_line_count)
    success_records = [record for record in records if record.get("outcome") == "success"]
    model_used = success_records[-1].get("model_used") if success_records else None
    fallback_used = bool(primary_model and model_used and model_used != primary_model)

    return CallResult(
        scenario=scenario_path.stem,
        round_index=round_index,
        ok=ok,
        latency_ms=latency_ms,
        model_used=model_used,
        fallback_used=fallback_used,
        error_code=error_code,
        error=error,
        ai_log_records=len(records),
        rate_limit_events=sum(1 for record in records if record.get("outcome") == "rate_limited"),
        timeout_events=sum(1 for record in records if record.get("outcome") == "timeout"),
        validation_failures=sum(
            1 for record in records if record.get("outcome") == "validation_failed"
        ),
        prompt_tokens=_sum_usage(records, "prompt_tokens"),
        completion_tokens=_sum_usage(records, "completion_tokens"),
        reported_cost=_reported_cost(records),
    )


async def run_benchmark(rounds: int = 2) -> dict[str, Any]:
    load_dotenv(ROOT / ".env")
    scenarios = _scenario_files()
    if len(scenarios) != 15:
        raise RuntimeError(f"Expected 15 mock drafts for T58, found {len(scenarios)}")
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("DEEPSEEK_API_KEY not configured; cannot run real T58 benchmark")
    if not os.environ.get("LLM_MODEL_PRIMARY"):
        raise RuntimeError("LLM_MODEL_PRIMARY not configured; cannot run real T58 benchmark")

    await init_db()
    await check_patch_and_refresh("16.10.1")

    started_at = datetime.now().isoformat(timespec="seconds")
    report_path = REPORTS_DIR / f"benchmark_30_calls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    primary_model = os.environ.get("LLM_MODEL_PRIMARY")
    results: list[CallResult] = []
    for round_index in range(1, rounds + 1):
        for scenario_path in scenarios:
            result = await _run_one(scenario_path, round_index, primary_model)
            results.append(result)
            status = "OK" if result.ok else f"ERR:{result.error_code}"
            print(
                f"[benchmark] round={round_index} scenario={scenario_path.stem} "
                f"status={status} latency_ms={result.latency_ms} model={result.model_used}"
            )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report = _summarize(results, started_at, report_path, rounds)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run T58 benchmark (15 scenarios x 2 rounds).")
    parser.add_argument("--rounds", type=int, default=2)
    args = parser.parse_args()

    report = asyncio.run(run_benchmark(rounds=args.rounds))
    latency = report["latency_ms"]
    print("[benchmark] summary")
    print(f"  attempted_calls: {report['attempted_calls']}")
    print(f"  successful_calls: {report['successful_calls']}")
    print(f"  error_calls: {report['error_calls']}")
    print(f"  p95_all_ms: {latency['p95_all']}")
    print(f"  p95_success_ms: {latency['p95_success']}")
    print(f"  fallback_call_percent: {report['fallback_call_percent']}")
    print(f"  rate_limit_events: {report['rate_limit_events']}")
    print(f"  reported_cost_total: {report['reported_cost_total']}")
    print(f"  report_path: {report['report_path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
