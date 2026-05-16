"""Tests for app.lcu_provider lockfile parser and discovery (M5/T36)."""

from pathlib import Path

import pytest

from app import lcu_provider
from app.lcu_provider import LockfileError, find_lockfile, parse_lockfile

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
