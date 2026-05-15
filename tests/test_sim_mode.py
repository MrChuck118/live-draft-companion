"""Tests for scripts/test_sim_mode.py sim-mode flow logic (M4/T35).

Verifica la parte 1 della DoD T35 (5/5 esito controllato, no crash) con mock.
La parte 2 (>=3/5 SuggestionOutput valido reale) e rinviata a OPEN-001 batch.
"""

import asyncio
import importlib.util
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.models import SuggestionItem, SuggestionOutput

_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "test_sim_mode.py"


def _load_sim_mode():
    spec = importlib.util.spec_from_file_location("test_sim_mode_mod", _SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _valid_response() -> MagicMock:
    payload = SuggestionOutput(
        patch="16.10.1",
        suggestions=[
            SuggestionItem(
                rank=i,
                champion=champ,
                build_path=["Liandry's Torment", "Sundered Sky", "Trinity Force"],
                keystone="Conqueror",
                explanation="Buona scelta per la lane in questo draft",
            )
            for i, champ in enumerate(["Garen", "Darius", "Sett"], start=1)
        ],
    ).model_dump_json()
    resp = MagicMock()
    resp.choices = [MagicMock()]
    resp.choices[0].message.content = payload
    return resp


def test_sim_mode_all_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    sim_mode = _load_sim_mode()
    fake = _valid_response()
    monkeypatch.setattr(sim_mode, "get_suggestions_with_fallback", lambda system, user: fake)

    results = asyncio.run(sim_mode.run_all())

    assert len(results) == 5
    assert all(outcome == "VALID" for _, outcome in results)


def test_sim_mode_chain_exhausted_is_controlled(monkeypatch: pytest.MonkeyPatch) -> None:
    sim_mode = _load_sim_mode()

    def _raise_exhausted(system: str, user: str):
        raise RuntimeError("AI chain exhausted after trying 4 models")

    monkeypatch.setattr(sim_mode, "get_suggestions_with_fallback", _raise_exhausted)

    results = asyncio.run(sim_mode.run_all())

    assert len(results) == 5
    assert all(outcome.startswith("CONTROLLED_FAILURE") for _, outcome in results)
    unhandled = sum(1 for _, outcome in results if outcome.startswith("UNHANDLED"))
    assert unhandled == 0
