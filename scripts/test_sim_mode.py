"""Sim-mode end-to-end smoke: FileProvider -> PromptBuilder -> AIClient chain -> output (M4/T35).

Esegue il flusso sim per i 5 scenari mock. La parte AI reale e impattata da
OPEN-001 (chain rate-limited): eseguito da CLI ora ogni scenario terminera in
CONTROLLED_FAILURE. La verifica ">=3/5 SuggestionOutput valido" e rinviata a
OPEN-001 batch. La logica del flusso e verificata via tests/test_sim_mode.py.
"""

import asyncio
import sys
from pathlib import Path

from app.ai_client import get_suggestions_with_fallback
from app.file_provider import FileProvider
from app.models import SuggestionOutput
from app.prompt_builder import build_prompt

_SCENARIOS = [
    "balanced_mid",
    "ad_heavy_top",
    "mid_meta_banned",
    "first_pick_top",
    "last_pick_support",
]
_MOCK_DRAFTS_DIR = Path(__file__).resolve().parent.parent / "tests" / "mock_drafts"


async def run_scenario(name: str) -> tuple[str, str]:
    """Run one scenario end-to-end and return (name, outcome) with a controlled outcome."""
    try:
        draft = await FileProvider(_MOCK_DRAFTS_DIR / f"{name}.json").get_current_state()
        system, user = build_prompt(draft, {})
        response = get_suggestions_with_fallback(system, user)
        content = response.choices[0].message.content or ""
        SuggestionOutput.model_validate_json(content)
        return name, "VALID"
    except RuntimeError as exc:
        return name, f"CONTROLLED_FAILURE: {exc}"
    except Exception as exc:  # noqa: BLE001
        return name, f"UNHANDLED: {type(exc).__name__}: {exc}"


async def run_all() -> list[tuple[str, str]]:
    """Run all 5 scenarios sequentially and return their outcomes."""
    return [await run_scenario(name) for name in _SCENARIOS]


def main() -> int:
    results = asyncio.run(run_all())
    valid = sum(1 for _, outcome in results if outcome == "VALID")
    unhandled = sum(1 for _, outcome in results if outcome.startswith("UNHANDLED"))
    for name, outcome in results:
        print(f"[sim_mode] {name}: {outcome}")
    print(f"[sim_mode] summary: {valid}/5 VALID, {unhandled}/5 UNHANDLED")
    return 1 if unhandled > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
