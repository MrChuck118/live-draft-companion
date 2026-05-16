"""Live LCU verification utility for M5/T40 (run from repo root with PYTHONPATH set).

NOT a pytest test (filename intentionally without test_ prefix to avoid the
scripts/ vs tests/ collection collision, PLOG-2026-05-15-032).

Idempotent and re-runnable. Steps 1-3 work as soon as the client is up.
Step 4 (champ-select -> DraftState) only runs when phase == ChampSelect;
otherwise it tells you to re-run once in champion select.

Privacy by design (spec 10.1): only /lol-gameflow/v1/session and
/lol-champ-select/v1/session are queried. No summoner endpoint, no writes,
no in-client automation (spec 10.3).
"""

import asyncio
import json

from app.lcu_provider import (
    GameflowMonitor,
    LCUProvider,
    LockfileError,
    find_lockfile,
    lcu_request,
    parse_lockfile,
)


def _mask(secret: str) -> str:
    if not secret:
        return "<empty>"
    return secret[:3] + "***" if len(secret) > 3 else "***"


async def main() -> int:
    print("=== T40 step 1: find_lockfile + parse_lockfile ===")
    try:
        path = find_lockfile()
    except LockfileError as exc:
        print(f"[FAIL] find_lockfile: {exc}")
        return 1
    creds = parse_lockfile(path)
    print(f"[OK] lockfile path: {path}")
    print(
        f"[OK] protocol={creds['protocol']} port={creds['port']} "
        f"pid={creds['pid']} password={_mask(creds['password'])}"
    )

    print("\n=== T40 step 2: lcu_request GET /lol-gameflow/v1/session ===")
    try:
        resp = await lcu_request("GET", "/lol-gameflow/v1/session")
    except (LockfileError, Exception) as exc:  # noqa: BLE001
        print(f"[FAIL] lcu_request gameflow: {type(exc).__name__}: {exc}")
        return 1
    print(f"[OK] HTTP {resp.status_code}")
    phase = None
    if resp.status_code == 200:
        try:
            phase = resp.json().get("phase")
        except ValueError:
            phase = None
    print(f"[OK] gameflow phase: {phase!r}")

    print("\n=== T40 step 3: GameflowMonitor.poll_once ===")
    monitor = GameflowMonitor()
    monitor_phase = await monitor.poll_once()
    print(f"[OK] monitor.current_phase: {monitor_phase!r}")

    print("\n=== T40 step 4: LCUProvider.get_current_state (needs ChampSelect) ===")
    if monitor_phase != "ChampSelect":
        print(
            f"[SKIP] phase is {monitor_phase!r}, not 'ChampSelect'. Enter a Custom "
            "Tournament Draft champion select (>=5 bans + picks), then re-run."
        )
        return 0

    draft = await LCUProvider().get_current_state()
    dumped = draft.model_dump_json()
    summoner_tokens = ("summonerId", "gameName", "displayName", "nameVisibilityType")
    leaked = [t for t in summoner_tokens if t in dumped]
    print(f"[OK] user_role={draft.user_role!r} cell={draft.local_player_cell_id}")
    print(f"[OK] bans ({len(draft.bans)}): {draft.bans}")
    print(
        f"[OK] ally_picks="
        f"{[(p.role, p.champion) for p in draft.ally_team]}"
    )
    print(
        f"[OK] enemy_picks="
        f"{[(p.role, p.champion) for p in draft.enemy_team]}"
    )
    print(f"[OK] actions count: {len(draft.actions)} (gating 09/05 era 3)")
    print(f"[{'FAIL' if leaked else 'OK'}] summoner tokens leaked: {leaked or 'none'}")
    print("\n--- DraftState JSON ---")
    print(json.dumps(json.loads(dumped), indent=2, ensure_ascii=False))

    bans_ok = len(draft.bans) >= 5
    actions_ok = len(draft.actions) >= 10
    print(
        f"\nDoD: bans>=5 {'OK' if bans_ok else 'NO'} | "
        f"actions>=10 {'OK' if actions_ok else 'NO (vedi INC-001/14.2)'} | "
        f"no summoner {'OK' if not leaked else 'FAIL'}"
    )
    return 0 if (bans_ok and not leaked) else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
