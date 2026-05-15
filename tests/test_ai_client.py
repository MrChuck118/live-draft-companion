"""Tests for app.ai_client fallback chain + validation retry logic (M3/T28-T29)."""

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from openai import APIError, APITimeoutError, RateLimitError

from app.ai_client import get_suggestions_with_fallback
from app.models import ChampionPick, DraftState, SuggestionOutput
from app.prompt_builder import build_prompt

_VALID_SUGGESTION_JSON = json.dumps(
    {
        "patch": "16.10.1",
        "suggestions": [
            {
                "rank": 1,
                "champion": "Garen",
                "build_path": ["Liandry's Torment", "Sundered Sky", "Trinity Force"],
                "keystone": "Conqueror",
                "explanation": "Counter forte e molto utile per la lane",
            },
            {
                "rank": 2,
                "champion": "Darius",
                "build_path": ["Stridebreaker", "Sundered Sky", "Trinity Force"],
                "keystone": "Conqueror",
                "explanation": "Buona scelta nel meta del momento",
            },
            {
                "rank": 3,
                "champion": "Sett",
                "build_path": ["Stridebreaker", "Sundered Sky", "Trinity Force"],
                "keystone": "Conqueror",
                "explanation": "Resiste bene e ha utility per il team",
            },
        ],
    }
)


def _fake_response(content: str = _VALID_SUGGESTION_JSON) -> MagicMock:
    """Build a fake ChatCompletion-like object; default content is a valid SuggestionOutput JSON."""
    resp = MagicMock()
    resp.choices = [MagicMock()]
    resp.choices[0].message.content = content
    resp.model = "fake-model"
    resp.usage.prompt_tokens = 120
    resp.usage.completion_tokens = 85
    return resp


def _fake_429() -> RateLimitError:
    """Build a minimal RateLimitError instance for tests."""
    response = MagicMock()
    response.status_code = 429
    response.headers = {}
    response.request = MagicMock()
    return RateLimitError(message="fake 429", response=response, body={"error": "rate_limited"})


def _fake_timeout() -> APITimeoutError:
    """Build a minimal APITimeoutError instance for tests."""
    return APITimeoutError(request=MagicMock())


def _fake_api_error() -> APIError:
    """Build a minimal generic APIError instance for tests."""
    return APIError(message="fake api error", request=MagicMock(), body=None)


@pytest.fixture
def env_chain(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up env with a 2-element chain for tests."""
    monkeypatch.setenv("LLM_MODEL_PRIMARY", "primary-model")
    monkeypatch.setenv("LLM_MODEL_FALLBACK_1", "fallback-model")
    monkeypatch.delenv("LLM_MODEL_FALLBACK_2", raising=False)
    monkeypatch.delenv("LLM_MODEL_FALLBACK_3", raising=False)


@pytest.fixture(autouse=True)
def fast_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip real sleeps in fallback tests so 30s backoff does not slow the suite."""
    monkeypatch.setattr("app.ai_client._sleep", lambda seconds: None)


@pytest.fixture(autouse=True)
def isolate_logs(monkeypatch: pytest.MonkeyPatch, tmp_path) -> object:
    """Redirect AI-call JSONL logs to a temp dir so tests never touch the real logs/ dir."""
    log_dir = tmp_path / "logs"
    monkeypatch.setattr("app.ai_client._LOGS_DIR", log_dir)
    return log_dir


def test_success_on_primary_first_attempt(env_chain: None) -> None:
    fake = _fake_response()
    with patch("app.ai_client.call_model", return_value=fake) as mock_call:
        result = get_suggestions_with_fallback("sys", "user")
    assert result is fake
    assert mock_call.call_count == 1


def test_429_two_retries_then_switch_to_fallback(env_chain: None) -> None:
    fake = _fake_response()
    side_effects = [_fake_429(), _fake_429(), _fake_429(), fake]
    with patch("app.ai_client.call_model", side_effect=side_effects) as mock_call:
        result = get_suggestions_with_fallback("sys", "user")
    assert result is fake
    assert mock_call.call_count == 4


def test_timeout_switches_immediately(env_chain: None) -> None:
    fake = _fake_response()
    side_effects = [_fake_timeout(), fake]
    with patch("app.ai_client.call_model", side_effect=side_effects) as mock_call:
        result = get_suggestions_with_fallback("sys", "user")
    assert result is fake
    assert mock_call.call_count == 2


def test_apierror_switches_immediately(env_chain: None) -> None:
    fake = _fake_response()
    side_effects = [_fake_api_error(), fake]
    with patch("app.ai_client.call_model", side_effect=side_effects) as mock_call:
        result = get_suggestions_with_fallback("sys", "user")
    assert result is fake
    assert mock_call.call_count == 2


def test_chain_exhausted_raises(env_chain: None) -> None:
    side_effects = [_fake_429() for _ in range(6)]
    with patch("app.ai_client.call_model", side_effect=side_effects) as mock_call:
        with pytest.raises(RuntimeError, match="chain exhausted"):
            get_suggestions_with_fallback("sys", "user")
    assert mock_call.call_count == 6


def test_chain_missing_primary_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLM_MODEL_PRIMARY", raising=False)
    monkeypatch.delenv("LLM_MODEL_FALLBACK_1", raising=False)
    monkeypatch.delenv("LLM_MODEL_FALLBACK_2", raising=False)
    monkeypatch.delenv("LLM_MODEL_FALLBACK_3", raising=False)
    with pytest.raises(RuntimeError, match="LLM_MODEL_PRIMARY"):
        get_suggestions_with_fallback("sys", "user")


def test_validation_format_fail_then_retry_succeeds(env_chain: None) -> None:
    """Malformed JSON first attempt -> retry same model -> valid response returned (M3/T29)."""
    invalid = _fake_response("not a valid json string at all")
    valid = _fake_response()
    with patch("app.ai_client.call_model", side_effect=[invalid, valid]) as mock_call:
        result = get_suggestions_with_fallback("sys", "user")
    assert result is valid
    assert mock_call.call_count == 2


def test_validation_format_fail_twice_switches_to_fallback(env_chain: None) -> None:
    """Two malformed JSON on primary (initial + retry) -> switch to fallback -> valid (M3/T29)."""
    invalid_1 = _fake_response("not valid")
    invalid_2 = _fake_response("still not valid")
    valid_on_fallback = _fake_response()
    with patch(
        "app.ai_client.call_model",
        side_effect=[invalid_1, invalid_2, valid_on_fallback],
    ) as mock_call:
        result = get_suggestions_with_fallback("sys", "user")
    assert result is valid_on_fallback
    assert mock_call.call_count == 3


def test_validation_mojibake_then_retry_succeeds(env_chain: None) -> None:
    """Mojibake in explanation first attempt -> retry same model -> clean response (M3/T29)."""
    mojibake_marker = chr(0x00C3) + chr(0x00C2) + chr(0x00A8)
    mojibake_json = _VALID_SUGGESTION_JSON.replace(
        "Counter forte e molto utile per la lane",
        f"Counter {mojibake_marker} forte",
    )
    mojibake_resp = _fake_response(mojibake_json)
    clean = _fake_response()
    with patch("app.ai_client.call_model", side_effect=[mojibake_resp, clean]) as mock_call:
        result = get_suggestions_with_fallback("sys", "user")
    assert result is clean
    assert mock_call.call_count == 2


def test_logging_three_calls_produce_three_jsonl_lines(
    env_chain: None, isolate_logs: object
) -> None:
    """DoD T30: after 3 successful calls the daily JSONL file has 3 parseable lines."""
    fake = _fake_response()
    with patch("app.ai_client.call_model", return_value=fake):
        for _ in range(3):
            get_suggestions_with_fallback("sys", "user")

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = isolate_logs / f"ai_calls_{date_str}.jsonl"
    assert log_file.exists()

    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3

    required = {
        "timestamp",
        "model_used",
        "prompt_hash",
        "latency_ms",
        "usage",
        "cost",
        "json_ok",
        "validation_results",
        "retry_count",
    }
    for line in lines:
        record = json.loads(line)
        assert required.issubset(record.keys())
        assert record["outcome"] == "success"
        assert record["model_used"] == "primary-model"
        assert record["json_ok"] is True
        assert record["cost"] is None
        assert record["validation_results"] == {"format": True, "utf8": True}
        assert record["usage"] == {"prompt_tokens": 120, "completion_tokens": 85}


# --- M3/T31 end-to-end flow tests (3 scenari) ---
# NOTA: questi DraftState sono fixture di PLUMBING per testare il flusso
# prompt -> call -> validate -> log. NON sono i dati reali del benchmark
# 09/05/2026 (non disponibili nel repo). I mock draft reali sono scope
# T34/T57 (tests/mock_drafts/*.json). La DoD chiamata reale di T31 e
# rinviata a OPEN-001 in batch con T27/T35/T58/T62.


def _draft_balanced_mid() -> DraftState:
    return DraftState(
        patch="16.10.1",
        user_role="MID",
        bans=["Yasuo", "Zed", "Yone", "Akali", "Sylas"],
        enemy_team=[
            ChampionPick(role="TOP", champion="Ornn"),
            ChampionPick(role="JUNGLE", champion="Vi"),
            ChampionPick(role="MID", champion="Orianna"),
            ChampionPick(role="ADC", champion="Jinx"),
            ChampionPick(role="SUPPORT", champion="Thresh"),
        ],
        ally_team=[
            ChampionPick(role="TOP", champion="Sett"),
            ChampionPick(role="JUNGLE", champion="Sejuani"),
            ChampionPick(role="MID", champion=None),
            ChampionPick(role="ADC", champion="Kai'Sa"),
            ChampionPick(role="SUPPORT", champion="Nautilus"),
        ],
        actions=[],
        local_player_cell_id=2,
    )


def _draft_mid_meta_banned() -> DraftState:
    return DraftState(
        patch="16.10.1",
        user_role="MID",
        bans=["Ahri", "Orianna", "Syndra", "Viktor", "Azir"],
        enemy_team=[
            ChampionPick(role="TOP", champion="Garen"),
            ChampionPick(role="MID", champion="Vex"),
        ],
        ally_team=[
            ChampionPick(role="JUNGLE", champion="Lee Sin"),
            ChampionPick(role="MID", champion=None),
        ],
        actions=[],
        local_player_cell_id=0,
    )


def _draft_last_pick_support() -> DraftState:
    return DraftState(
        patch="16.10.1",
        user_role="SUPPORT",
        bans=["Blitzcrank", "Thresh", "Pyke", "Nautilus", "Leona"],
        enemy_team=[
            ChampionPick(role="TOP", champion="Aatrox"),
            ChampionPick(role="JUNGLE", champion="Kha'Zix"),
            ChampionPick(role="MID", champion="Ahri"),
            ChampionPick(role="ADC", champion="Caitlyn"),
            ChampionPick(role="SUPPORT", champion="Lux"),
        ],
        ally_team=[
            ChampionPick(role="TOP", champion="Camille"),
            ChampionPick(role="JUNGLE", champion="Elise"),
            ChampionPick(role="MID", champion="Syndra"),
            ChampionPick(role="ADC", champion="Jinx"),
            ChampionPick(role="SUPPORT", champion=None),
        ],
        actions=[],
        local_player_cell_id=9,
    )


def _run_e2e(draft: DraftState, isolate_logs: object) -> SuggestionOutput:
    """Full flow: build_prompt -> get_suggestions_with_fallback (mocked) -> validate -> log."""
    system, user = build_prompt(draft, {})
    assert system != ""
    assert user != ""
    assert draft.user_role in user

    valid = _fake_response()
    with patch("app.ai_client.call_model", return_value=valid):
        response = get_suggestions_with_fallback(system, user)

    parsed = SuggestionOutput.model_validate_json(response.choices[0].message.content)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = isolate_logs / f"ai_calls_{date_str}.jsonl"
    assert log_file.exists()
    last_record = json.loads(log_file.read_text(encoding="utf-8").strip().split("\n")[-1])
    assert last_record["outcome"] == "success"
    return parsed


def test_e2e_balanced_mid(env_chain: None, isolate_logs: object) -> None:
    """DoD T31 (plumbing): scenario balanced_mid -> SuggestionOutput valido + log scritto."""
    parsed = _run_e2e(_draft_balanced_mid(), isolate_logs)
    assert len(parsed.suggestions) == 3
    assert parsed.patch == "16.10.1"


def test_e2e_mid_meta_banned(env_chain: None, isolate_logs: object) -> None:
    """DoD T31 (plumbing): scenario mid_meta_banned -> SuggestionOutput valido + log scritto."""
    parsed = _run_e2e(_draft_mid_meta_banned(), isolate_logs)
    assert len(parsed.suggestions) == 3


def test_e2e_last_pick_support(env_chain: None, isolate_logs: object) -> None:
    """DoD T31 (plumbing): scenario last_pick_support -> SuggestionOutput valido + log scritto."""
    parsed = _run_e2e(_draft_last_pick_support(), isolate_logs)
    assert len(parsed.suggestions) == 3
