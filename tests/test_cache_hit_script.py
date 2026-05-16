"""Tests for scripts/test_cache_hit.py (M8/T59)."""

import importlib.util
from pathlib import Path

_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "test_cache_hit.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("cache_hit_script", _SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cache_hit_script_checks_ai_log_delta() -> None:
    script = _load_script()

    assert hasattr(script, "run_check")
    source = _SCRIPT_PATH.read_text(encoding="utf-8")
    assert "ai_calls_first_run" in source
    assert "ai_calls_second_run" in source
    assert "second_delta == 0" in source
    assert "SuggestionError" in source
    assert "SuggestionService()" in source
    assert "_clear_cache_for_hash" in source
