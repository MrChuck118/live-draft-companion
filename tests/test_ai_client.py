"""Tests for app.ai_client fallback chain + validation retry logic (M3/T28-T29)."""

import json
from unittest.mock import MagicMock, patch

import pytest
from openai import APIError, APITimeoutError, RateLimitError

from app.ai_client import get_suggestions_with_fallback

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
