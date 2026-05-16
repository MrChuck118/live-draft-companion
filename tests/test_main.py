"""Tests for app.main FastAPI app + lifecycle and app.config (M6a/T41)."""

import logging

from fastapi.testclient import TestClient

import app.main as main
from app.config import Settings
from app.suggestion_service import SuggestionError


def test_settings_defaults_without_env(monkeypatch) -> None:
    """Settings import with safe defaults; sim mode is the default path.

    Other tests call load_dotenv(), polluting os.environ; clear the relevant
    vars so this asserts the in-code defaults, not the local .env values.
    """
    for var in (
        "DEEPSEEK_API_KEY",
        "LLM_MODEL_PRIMARY",
        "LLM_MODEL_FALLBACK_1",
        "DRAFT_PROVIDER_MODE",
        "DRAFT_PROVIDER_FILE",
        "LOG_LEVEL",
    ):
        monkeypatch.delenv(var, raising=False)

    settings = Settings(_env_file=None)

    assert settings.draft_provider_mode == "sim"
    assert settings.draft_provider_file == "tests/mock_drafts/balanced_mid.json"
    assert settings.llm_model_primary == "deepseek-chat"
    assert settings.llm_model_fallback_1 == "deepseek-reasoner"
    assert settings.log_level == "INFO"
    assert settings.deepseek_api_key == ""


def test_app_metadata() -> None:
    assert main.app.title == "Live Draft Companion"


def test_index_serves_base_html(monkeypatch) -> None:
    """GET / returns the base UI shell with the initial waiting state (DoD T43)."""

    async def fake_init_db() -> None:
        return None

    async def fake_check_patch_and_refresh() -> str:
        return "16.10.1"

    monkeypatch.setattr(main, "init_db", fake_init_db)
    monkeypatch.setattr(main, "check_patch_and_refresh", fake_check_patch_and_refresh)

    with TestClient(main.app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "In attesa del client LoL" in response.text


def test_index_shell_has_all_containers(monkeypatch) -> None:
    """DoD T46: full Tailwind shell with all section containers in the DOM."""
    _mock_lifecycle(monkeypatch)

    with TestClient(main.app) as client:
        html = client.get("/").text

    assert "https://cdn.tailwindcss.com" in html
    for marker in (
        'id="status"',
        'id="bans-list"',
        'id="ally-team"',
        'id="enemy-team"',
        'id="suggestions"',
        'id="suggest-button"',
        'id="history-list"',
    ):
        assert marker in html, f"missing container {marker}"
    # Error banner present but initially hidden (logic in T49b).
    assert 'id="error-banner"' in html
    assert "hidden" in html.split('id="error-banner"')[1].split(">")[0]
    # JS wired into the shell (T47).
    assert '/static/app.js' in html


def test_static_app_js_served(monkeypatch) -> None:
    """DoD T47: static mount serves app.js with the 2s draft-state polling."""
    _mock_lifecycle(monkeypatch)

    with TestClient(main.app) as client:
        response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]
    body = response.text
    assert "/api/draft-state" in body
    assert "2000" in body


def _mock_lifecycle(monkeypatch) -> None:
    async def fake_init_db() -> None:
        return None

    async def fake_check_patch_and_refresh() -> str:
        return "16.10.1"

    monkeypatch.setattr(main, "init_db", fake_init_db)
    monkeypatch.setattr(main, "check_patch_and_refresh", fake_check_patch_and_refresh)


def test_draft_state_sim_returns_draftstate(monkeypatch) -> None:
    """GET /api/draft-state in sim mode returns the DraftState JSON (DoD T44)."""
    _mock_lifecycle(monkeypatch)
    monkeypatch.setattr(
        main,
        "get_settings",
        lambda: Settings(
            _env_file=None,
            draft_provider_mode="sim",
            draft_provider_file="tests/mock_drafts/balanced_mid.json",
        ),
    )

    with TestClient(main.app) as client:
        response = client.get("/api/draft-state")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    body = response.json()
    assert body["patch"] == "16.10.1"
    assert body["user_role"] in {"TOP", "JUNGLE", "MID", "ADC", "SUPPORT"}
    assert isinstance(body["bans"], list)


def test_draft_state_provider_error_returns_503(monkeypatch) -> None:
    """A provider failure is surfaced as a controlled 503, not a stack trace."""
    _mock_lifecycle(monkeypatch)

    class FailingProvider:
        async def get_current_state(self):
            raise RuntimeError("client LoL non attivo")

    monkeypatch.setattr(main, "get_draft_state_provider", lambda settings: FailingProvider())

    with TestClient(main.app) as client:
        response = client.get("/api/draft-state")

    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/json")
    assert "Stato draft non disponibile" in response.json()["detail"]


def test_lifespan_startup_ok(monkeypatch, caplog) -> None:
    """Startup runs init_db + Data Dragon refresh and logs 'App ready' (DoD T41)."""
    calls: list[str] = []

    async def fake_init_db() -> None:
        calls.append("init_db")

    async def fake_check_patch_and_refresh() -> str:
        calls.append("check_patch")
        return "16.10.1"

    monkeypatch.setattr(main, "init_db", fake_init_db)
    monkeypatch.setattr(main, "check_patch_and_refresh", fake_check_patch_and_refresh)

    with caplog.at_level(logging.INFO, logger="live_draft_companion"):
        with TestClient(main.app):
            pass

    assert calls == ["init_db", "check_patch"]
    assert "App ready" in caplog.text
    assert "App shutting down" in caplog.text


def test_lifespan_datadragon_failure_non_fatal(monkeypatch, caplog) -> None:
    """Data Dragon network failure must NOT crash startup (spec Â§12, RF-001)."""
    import httpx

    async def fake_init_db() -> None:
        return None

    async def failing_refresh() -> str:
        raise httpx.ConnectError("Data Dragon unreachable")

    monkeypatch.setattr(main, "init_db", fake_init_db)
    monkeypatch.setattr(main, "check_patch_and_refresh", failing_refresh)

    with caplog.at_level(logging.INFO, logger="live_draft_companion"):
        with TestClient(main.app):
            pass

    messages = [record.getMessage() for record in caplog.records]
    assert any("Data Dragon refresh skipped" in message for message in messages)
    assert any(message == "App ready" for message in messages)


# --- T45: thin POST /api/suggest ---

_VALID_DRAFT_BODY = {
    "patch": "16.10.1",
    "user_role": "MID",
    "bans": ["Yasuo", "Zed", "Yone", "Akali", "Sylas"],
    "enemy_team": [{"role": "TOP", "champion": None}],
    "ally_team": [{"role": "MID", "champion": None}],
    "actions": [],
    "local_player_cell_id": 2,
}


def _sample_suggestion_output():
    from app.models import SuggestionItem, SuggestionOutput

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


def test_suggest_valid_body_delegates_to_service(monkeypatch) -> None:
    """DoD T45: valid body -> 200 with 3 suggestions (service delegated)."""
    _mock_lifecycle(monkeypatch)
    output = _sample_suggestion_output()
    captured = {}

    class FakeService:
        async def suggest(self, draft_state):
            captured["draft"] = draft_state
            return output

    monkeypatch.setattr(main, "SuggestionService", lambda: FakeService())

    with TestClient(main.app) as client:
        response = client.post("/api/suggest", json=_VALID_DRAFT_BODY)

    assert response.status_code == 200
    body = response.json()
    assert len(body["suggestions"]) == 3
    assert captured["draft"].user_role == "MID"


def test_suggest_malformed_body_returns_422(monkeypatch) -> None:
    _mock_lifecycle(monkeypatch)

    with TestClient(main.app) as client:
        response = client.post("/api/suggest", json={"patch": "16.10.1"})

    assert response.status_code == 422


def test_suggest_service_error_returns_controlled_503(monkeypatch) -> None:
    """SuggestionError -> 503 without stack trace or API key in the body."""
    _mock_lifecycle(monkeypatch)

    class FailingService:
        async def suggest(self, draft_state):
            raise SuggestionError("AI chain exhausted; key sk-secret-xyz")

    monkeypatch.setattr(main, "SuggestionService", lambda: FailingService())

    with TestClient(main.app) as client:
        response = client.post("/api/suggest", json=_VALID_DRAFT_BODY)

    assert response.status_code == 503
    text = response.text
    assert "sk-secret-xyz" not in text
    assert "Traceback" not in text
    assert response.json()["detail"]
