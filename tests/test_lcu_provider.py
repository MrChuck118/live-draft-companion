"""Tests for app.lcu_provider lockfile parser and discovery (M5/T36)."""

import asyncio
from pathlib import Path

import pytest

from app import lcu_provider
from app.lcu_provider import (
    GameflowMonitor,
    LCUProvider,
    LockfileError,
    find_lockfile,
    parse_champ_select_session,
    parse_lockfile,
)
from app.models import DraftState

_VALID_LOCKFILE = "LeagueClient:13245:54321:S3cr3tPassw0rd:https"


def test_parse_lockfile_valid(tmp_path) -> None:
    lockfile = tmp_path / "lockfile"
    lockfile.write_text(_VALID_LOCKFILE, encoding="utf-8")

    result = parse_lockfile(lockfile)

    assert result == {
        "process_name": "LeagueClient",
        "pid": "13245",
        "port": "54321",
        "password": "S3cr3tPassw0rd",
        "protocol": "https",
    }


def test_parse_lockfile_accepts_str_path_and_trailing_whitespace(tmp_path) -> None:
    lockfile = tmp_path / "lockfile"
    lockfile.write_text(_VALID_LOCKFILE + "\n", encoding="utf-8")

    result = parse_lockfile(str(lockfile))

    assert result["port"] == "54321"
    assert result["protocol"] == "https"


def test_parse_lockfile_missing_file_raises(tmp_path) -> None:
    with pytest.raises(LockfileError, match="not found"):
        parse_lockfile(tmp_path / "does_not_exist")


def test_parse_lockfile_malformed_raises(tmp_path) -> None:
    lockfile = tmp_path / "lockfile"
    lockfile.write_text("LeagueClient:13245:54321", encoding="utf-8")

    with pytest.raises(LockfileError, match="unexpected lockfile format"):
        parse_lockfile(lockfile)


def test_find_lockfile_not_running_raises(monkeypatch) -> None:
    monkeypatch.setattr(lcu_provider, "_STANDARD_LOCKFILE", Path("Z:/nope/lockfile"))
    monkeypatch.setattr(lcu_provider.psutil, "process_iter", lambda attrs=None: iter([]))

    with pytest.raises(LockfileError, match="not running or not installed"):
        find_lockfile()


def test_find_lockfile_via_process_discovery(tmp_path, monkeypatch) -> None:
    """Non-standard install path (e.g. E:\\Riot Games) discovered via psutil."""
    (tmp_path / "lockfile").write_text(_VALID_LOCKFILE, encoding="utf-8")

    class _FakeProc:
        def __init__(self, info: dict) -> None:
            self.info = info

    fake = _FakeProc({"name": "LeagueClientUx.exe", "exe": str(tmp_path / "LeagueClientUx.exe")})
    monkeypatch.setattr(lcu_provider, "_STANDARD_LOCKFILE", Path("Z:/nope/lockfile"))
    monkeypatch.setattr(
        lcu_provider.psutil, "process_iter", lambda attrs=None: iter([fake])
    )

    result = find_lockfile()

    assert result == tmp_path / "lockfile"
    assert parse_lockfile(result)["port"] == "54321"


class _FakeResponse:
    status_code = 200


class _FakeAsyncClient:
    last_init: dict = {}
    last_request: dict = {}

    def __init__(self, **kwargs) -> None:
        _FakeAsyncClient.last_init = kwargs

    async def __aenter__(self) -> "_FakeAsyncClient":
        return self

    async def __aexit__(self, *exc) -> bool:
        return False

    async def request(self, method, url, **kwargs) -> _FakeResponse:
        _FakeAsyncClient.last_request = {"method": method, "url": url, **kwargs}
        return _FakeResponse()


@pytest.mark.asyncio
async def test_lcu_request_builds_authenticated_loopback_request(tmp_path, monkeypatch) -> None:
    lockfile = tmp_path / "lockfile"
    lockfile.write_text(_VALID_LOCKFILE, encoding="utf-8")
    monkeypatch.setattr(lcu_provider.httpx, "AsyncClient", _FakeAsyncClient)

    response = await lcu_provider.lcu_request(
        "GET", "/lol-gameflow/v1/session", lockfile_path=lockfile
    )

    assert response.status_code == 200
    assert _FakeAsyncClient.last_init.get("verify") is False
    assert _FakeAsyncClient.last_request["method"] == "GET"
    assert (
        _FakeAsyncClient.last_request["url"]
        == "https://127.0.0.1:54321/lol-gameflow/v1/session"
    )
    assert _FakeAsyncClient.last_request["auth"] == ("riot", "S3cr3tPassw0rd")


@pytest.mark.asyncio
async def test_lcu_request_uses_find_lockfile_when_no_path(tmp_path, monkeypatch) -> None:
    lockfile = tmp_path / "lockfile"
    lockfile.write_text(_VALID_LOCKFILE, encoding="utf-8")
    monkeypatch.setattr(lcu_provider, "find_lockfile", lambda: lockfile)
    monkeypatch.setattr(lcu_provider.httpx, "AsyncClient", _FakeAsyncClient)

    await lcu_provider.lcu_request("GET", "lol-gameflow/v1/session")

    assert (
        _FakeAsyncClient.last_request["url"]
        == "https://127.0.0.1:54321/lol-gameflow/v1/session"
    )


def test_no_summoner_endpoint_in_python_sources() -> None:
    """DoD T37 / spec 10.1: no summoner endpoint referenced in any .py source.

    The forbidden token is assembled at runtime so this assertion itself does
    not contain the literal (keeps `git grep` clean too).
    """
    forbidden = "lol-" + "summoner"
    root = Path(__file__).resolve().parent.parent
    offenders = []
    for py_file in root.rglob("*.py"):
        if ".venv" in py_file.parts:
            continue
        if forbidden in py_file.read_text(encoding="utf-8"):
            offenders.append(str(py_file.relative_to(root)))
    assert offenders == [], f"summoner endpoint referenced in: {offenders}"


class _PhaseResponse:
    def __init__(self, status_code: int, payload) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


@pytest.mark.asyncio
async def test_poll_once_updates_phase(monkeypatch) -> None:
    async def fake_request(method, path, **kwargs):
        return _PhaseResponse(200, {"phase": "ChampSelect"})

    monkeypatch.setattr(lcu_provider, "lcu_request", fake_request)
    monitor = GameflowMonitor()

    result = await monitor.poll_once()

    assert result == "ChampSelect"
    assert monitor.current_phase == "ChampSelect"


@pytest.mark.asyncio
async def test_poll_once_non_200_sets_none(monkeypatch) -> None:
    async def fake_request(method, path, **kwargs):
        return _PhaseResponse(404, {})

    monkeypatch.setattr(lcu_provider, "lcu_request", fake_request)
    monitor = GameflowMonitor()
    monitor.current_phase = "Lobby"

    result = await monitor.poll_once()

    assert result is None
    assert monitor.current_phase is None


@pytest.mark.asyncio
async def test_poll_once_handles_lcu_error_without_crash(monkeypatch) -> None:
    async def fake_request(method, path, **kwargs):
        raise LockfileError("client not running")

    monkeypatch.setattr(lcu_provider, "lcu_request", fake_request)
    monitor = GameflowMonitor()
    monitor.current_phase = "ChampSelect"

    result = await monitor.poll_once()

    assert result is None
    assert monitor.current_phase is None


@pytest.mark.asyncio
async def test_run_polls_then_stops(monkeypatch) -> None:
    stop_event = asyncio.Event()
    monitor = GameflowMonitor()
    calls = {"n": 0}

    async def fake_poll_once():
        calls["n"] += 1
        if calls["n"] >= 3:
            stop_event.set()
        return "ChampSelect"

    monkeypatch.setattr(monitor, "poll_once", fake_poll_once)

    await asyncio.wait_for(
        monitor.run(stop_event=stop_event, interval=0.0), timeout=2.0
    )

    assert calls["n"] >= 3


_CHAMP_NAMES = {266: "Aatrox", 64: "Lee Sin", 103: "Ahri", 22: "Ashe", 412: "Thresh"}


def _ranked_session() -> dict:
    return {
        "localPlayerCellId": 2,
        "myTeam": [
            {"cellId": 1, "championId": 64, "assignedPosition": "jungle", "summonerId": 999},
            {"cellId": 2, "championId": 103, "assignedPosition": "middle", "gameName": "Secret"},
            {"cellId": 3, "championId": 0, "assignedPosition": "bottom", "displayName": "X"},
        ],
        "theirTeam": [
            {"cellId": 4, "championId": 22, "assignedPosition": "bottom", "summonerId": 7},
            {"cellId": 5, "championId": 0, "assignedPosition": "top"},
        ],
        "actions": [
            [{"id": 10, "actorCellId": 1, "championId": 266, "type": "ban", "completed": True}],
            [{"id": 11, "actorCellId": 2, "championId": 103, "type": "pick", "completed": False}],
        ],
    }


def test_parse_champ_select_ranked_builds_draftstate() -> None:
    draft = parse_champ_select_session(_ranked_session(), "16.10.1", _CHAMP_NAMES)

    assert isinstance(draft, DraftState)
    assert draft.patch == "16.10.1"
    assert draft.user_role == "MID"
    assert draft.local_player_cell_id == 2
    assert draft.bans == ["Aatrox"]
    assert draft.ally_team[0].role == "JUNGLE"
    assert draft.ally_team[0].champion == "Lee Sin"
    assert draft.ally_team[2].champion is None  # championId 0 -> unpicked
    assert draft.enemy_team[0].champion == "Ashe"
    assert len(draft.actions) == 2
    assert draft.actions[0].type == "ban" and draft.actions[0].completed is True


def test_parse_champ_select_custom_bot_minimal_no_crash() -> None:
    """INC-001: reduced custom-vs-bot schema (few actions, sparse fields)."""
    session = {
        "localPlayerCellId": 0,
        "myTeam": [{"cellId": 0, "championId": 0, "assignedPosition": ""}],
        "theirTeam": [],
        "actions": [[{"id": 1, "actorCellId": 0, "type": "pick", "completed": False}]],
    }

    draft = parse_champ_select_session(session, "16.10.1", _CHAMP_NAMES)

    assert isinstance(draft, DraftState)
    assert draft.user_role == ""
    assert draft.bans == []
    assert draft.ally_team[0].champion is None
    assert len(draft.actions) == 1


def test_parse_champ_select_ignores_summoner_identity_fields() -> None:
    """Summoner identity fields present in input must not surface in DraftState."""
    draft = parse_champ_select_session(_ranked_session(), "16.10.1", _CHAMP_NAMES)

    dumped = draft.model_dump_json()
    for token in ("summonerId", "gameName", "displayName", "Secret", "999"):
        assert token not in dumped


@pytest.mark.asyncio
async def test_lcu_provider_get_current_state(monkeypatch) -> None:
    async def fake_request(method, path, **kwargs):
        assert path == "/lol-champ-select/v1/session"
        return _PhaseResponse(200, _ranked_session())

    async def fake_patch():
        return "16.10.1"

    async def fake_names():
        return _CHAMP_NAMES

    monkeypatch.setattr(lcu_provider, "lcu_request", fake_request)
    monkeypatch.setattr(lcu_provider, "_load_cached_patch", fake_patch)
    monkeypatch.setattr(lcu_provider, "_load_champion_id_to_name", fake_names)

    draft = await LCUProvider().get_current_state()

    assert isinstance(draft, DraftState)
    assert draft.user_role == "MID"
    assert draft.bans == ["Aatrox"]


@pytest.mark.asyncio
async def test_lcu_provider_non_200_raises(monkeypatch) -> None:
    async def fake_request(method, path, **kwargs):
        return _PhaseResponse(404, {})

    monkeypatch.setattr(lcu_provider, "lcu_request", fake_request)

    with pytest.raises(LockfileError, match="champ-select session unavailable"):
        await LCUProvider().get_current_state()
