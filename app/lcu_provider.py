"""LCU lockfile parser and discovery for live draft capture (M5/T36).

Scope T36: pure lockfile parsing + path discovery only. No authenticated HTTP
calls and no summoner-name reads (privacy by design, spec 10.1); those belong
to T37 and later.
"""

import asyncio
from pathlib import Path

import httpx
import psutil
from sqlalchemy import select

from app.db import AsyncSessionLocal, Champion, Meta
from app.draft_state_provider import DraftStateProvider
from app.models import Action, ChampionPick, DraftState

_LCU_USERNAME = "riot"

_CHAMP_SELECT_PATH = "/lol-champ-select/v1/session"

# LCU assignedPosition -> internal role label.
_ROLE_MAP = {
    "top": "TOP",
    "jungle": "JUNGLE",
    "middle": "MID",
    "bottom": "ADC",
    "utility": "SUPPORT",
}

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


async def lcu_request(
    method: str,
    path: str,
    *,
    lockfile_path: str | Path | None = None,
    timeout: float = 10.0,
) -> httpx.Response:
    """Issue an authenticated request to the local LCU endpoint.

    Resolves the lockfile (given path, else find_lockfile()), builds the
    loopback base URL from it, and sends an HTTP Basic request with
    verify=False: the LCU uses a local self-signed certificate and traffic is
    loopback-only (127.0.0.1), so disabling verification here is expected per
    spec RF-003. Privacy by design (spec 10.1): callers must not target
    summoner endpoints; this wrapper adds no such path itself.
    """
    source = lockfile_path if lockfile_path is not None else find_lockfile()
    creds = parse_lockfile(source)
    normalized_path = path if path.startswith("/") else f"/{path}"
    url = f"{creds['protocol']}://127.0.0.1:{creds['port']}{normalized_path}"
    async with httpx.AsyncClient(verify=False, timeout=timeout) as client:
        return await client.request(
            method,
            url,
            auth=(_LCU_USERNAME, creds["password"]),
        )


class GameflowMonitor:
    """Poll the LCU gameflow session and keep the current phase (M5/T38).

    Scope T38: gameflow phase only (RF-004/RF-005). Champ-select session
    parsing is T39. The client being closed or not started is a normal state,
    not a fatal error: on any LCU/transport error the phase becomes None and
    polling continues without crashing (RF-022).
    """

    _GAMEFLOW_PATH = "/lol-gameflow/v1/session"

    def __init__(self) -> None:
        self.current_phase: str | None = None

    async def poll_once(self) -> str | None:
        """Read the gameflow session once and update current_phase."""
        try:
            response = await lcu_request("GET", self._GAMEFLOW_PATH)
        except (LockfileError, httpx.HTTPError):
            self.current_phase = None
            return None

        if response.status_code != 200:
            self.current_phase = None
            return None

        try:
            phase = response.json().get("phase")
        except (ValueError, AttributeError):
            self.current_phase = None
            return None

        self.current_phase = phase
        return phase

    async def run(self, *, stop_event: asyncio.Event, interval: float = 2.0) -> None:
        """Poll every `interval` seconds until `stop_event` is set."""
        while not stop_event.is_set():
            await self.poll_once()
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=interval)
            except asyncio.TimeoutError:
                continue


def _normalize_role(assigned: str | None) -> str:
    """Map an LCU assignedPosition to an internal role label ('' if unknown)."""
    if not assigned:
        return ""
    return _ROLE_MAP.get(assigned.lower(), assigned.upper())


def _champion_name(champion_id, champion_names: dict[int, str]) -> str | None:
    """Resolve an LCU championId to a Data Dragon name (None if unpicked/unknown)."""
    if not champion_id:
        return None
    try:
        return champion_names.get(int(champion_id))
    except (TypeError, ValueError):
        return None


async def _load_champion_id_to_name() -> dict[int, str]:
    """Build {numeric championId: name} from the Data Dragon cache."""
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(Champion.key, Champion.name))).all()
    mapping: dict[int, str] = {}
    for key, name in rows:
        try:
            mapping[int(key)] = name
        except (TypeError, ValueError):
            continue
    return mapping


async def _load_cached_patch() -> str:
    """Read the cached patch from the Data Dragon meta table ('' if absent)."""
    async with AsyncSessionLocal() as session:
        meta = await session.get(Meta, "patch")
    return meta.value if meta is not None else ""


def parse_champ_select_session(
    session: dict,
    patch: str,
    champion_names: dict[int, str],
) -> DraftState:
    """Parse an LCU champ-select session into a DraftState.

    Privacy by design (spec 10.1): only cellId, championId, assignedPosition
    and action fields are read. Summoner identity fields (summonerId,
    gameName, displayName, ...) are never accessed. Defensive against the
    reduced custom-vs-bot actions schema (INC-001).
    """
    local_cell = session.get("localPlayerCellId", -1)
    if not isinstance(local_cell, int):
        local_cell = -1
    my_team_raw = session.get("myTeam") or []
    their_team_raw = session.get("theirTeam") or []

    ally_team = [
        ChampionPick(
            role=_normalize_role(member.get("assignedPosition")),
            champion=_champion_name(member.get("championId"), champion_names),
        )
        for member in my_team_raw
        if isinstance(member, dict)
    ]
    enemy_team = [
        ChampionPick(
            role=_normalize_role(member.get("assignedPosition")),
            champion=_champion_name(member.get("championId"), champion_names),
        )
        for member in their_team_raw
        if isinstance(member, dict)
    ]

    actions: list[Action] = []
    bans: list[str] = []
    for group in session.get("actions") or []:
        for action in group or []:
            if not isinstance(action, dict):
                continue
            actions.append(
                Action(
                    action_id=action.get("id", 0),
                    actor_cell_id=action.get("actorCellId", -1),
                    type=action.get("type", ""),
                    completed=bool(action.get("completed", False)),
                )
            )
            if action.get("type") == "ban" and action.get("completed"):
                name = _champion_name(action.get("championId"), champion_names)
                if name:
                    bans.append(name)

    user_role = ""
    for member in my_team_raw:
        if isinstance(member, dict) and member.get("cellId") == local_cell:
            user_role = _normalize_role(member.get("assignedPosition"))
            break

    return DraftState(
        patch=patch,
        user_role=user_role,
        bans=bans,
        enemy_team=enemy_team,
        ally_team=ally_team,
        actions=actions,
        local_player_cell_id=local_cell,
    )


class LCUProvider(DraftStateProvider):
    """Live DraftStateProvider backed by the LCU champ-select session (M5/T39)."""

    async def get_current_state(self) -> DraftState:
        """Fetch and parse the current champ-select session into a DraftState."""
        response = await lcu_request("GET", _CHAMP_SELECT_PATH)
        if response.status_code != 200:
            raise LockfileError(
                f"champ-select session unavailable (HTTP {response.status_code})"
            )
        session = response.json()
        patch = await _load_cached_patch()
        champion_names = await _load_champion_id_to_name()
        return parse_champ_select_session(session, patch, champion_names)
