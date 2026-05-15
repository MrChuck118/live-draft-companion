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
