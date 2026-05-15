"""LCU lockfile parser and discovery for live draft capture (M5/T36).

Scope T36: pure lockfile parsing + path discovery only. No authenticated HTTP
calls and no summoner-name reads (privacy by design, spec 10.1); those belong
to T37 and later.
"""

from pathlib import Path

import psutil

_STANDARD_LOCKFILE = Path(r"C:\Riot Games\League of Legends\lockfile")
_PROCESS_NAMES = {
    "LeagueClientUx.exe",
    "LeagueClient.exe",
    "LeagueClientUx",
    "LeagueClient",
}


class LockfileError(RuntimeError):
    """Raised when the LCU lockfile cannot be located or parsed."""


def parse_lockfile(path: str | Path) -> dict[str, str]:
    """Parse an LCU lockfile into its components.

    Lockfile format: ``<processName>:<pid>:<port>:<password>:<protocol>``.
    Returns keys: process_name, pid, port, password, protocol.
    Raises LockfileError on a missing, unreadable or malformed file.
    """
    lockfile = Path(path)
    try:
        raw = lockfile.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise LockfileError(f"lockfile not found: {lockfile}") from exc
    except OSError as exc:
        raise LockfileError(f"lockfile not readable: {lockfile} ({exc})") from exc

    parts = raw.split(":")
    if len(parts) != 5:
        raise LockfileError(
            f"unexpected lockfile format: expected 5 colon-separated fields, "
            f"got {len(parts)}"
        )

    process_name, pid, port, password, protocol = parts
    return {
        "process_name": process_name,
        "pid": pid,
        "port": port,
        "password": password,
        "protocol": protocol,
    }


def _lockfile_from_process() -> Path | None:
    """Locate the lockfile via the running LeagueClient process.

    Covers non-standard install paths (e.g. ``E:\\Riot Games\\...``) where the
    standard path does not exist.
    """
    for proc in psutil.process_iter(["name", "exe"]):
        try:
            if proc.info.get("name") not in _PROCESS_NAMES:
                continue
            exe = proc.info.get("exe")
            if not exe:
                continue
            candidate = Path(exe).parent / "lockfile"
            if candidate.is_file():
                return candidate
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def find_lockfile() -> Path:
    """Return the LCU lockfile path: standard path first, then process discovery.

    Raises LockfileError when the client is not running or not installed.
    """
    if _STANDARD_LOCKFILE.is_file():
        return _STANDARD_LOCKFILE
    discovered = _lockfile_from_process()
    if discovered is not None:
        return discovered
    raise LockfileError(
        "LCU lockfile not found: League of Legends client not running "
        "or not installed"
    )
