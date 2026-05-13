"""Test cache integrita Data Dragon (M1/T12)."""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import func, select

from app.data_dragon import check_patch_and_refresh
from app.db import AsyncSessionLocal, Champion, Item, Rune


MIN_CHAMPIONS = 160
MIN_ITEMS = 200
MIN_KEYSTONES = 8

ITALIAN_ACCENT_RE = re.compile(r"[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]")


async def main() -> int:
    patch = await check_patch_and_refresh()

    async with AsyncSessionLocal() as session:
        champion_count = await session.scalar(select(func.count()).select_from(Champion))
        item_count = await session.scalar(select(func.count()).select_from(Item))
        rune_count = await session.scalar(select(func.count()).select_from(Rune))

        champions = (await session.execute(select(Champion))).scalars().all()
        items = (await session.execute(select(Item))).scalars().all()
        runes = (await session.execute(select(Rune))).scalars().all()

    print(f"patch: {patch}")
    print(f"champions: {champion_count}")
    print(f"items: {item_count}")
    print(f"keystones: {rune_count}")

    failures: list[str] = []

    if champion_count is None or champion_count < MIN_CHAMPIONS:
        failures.append(f"champions {champion_count} < {MIN_CHAMPIONS}")
    if item_count is None or item_count < MIN_ITEMS:
        failures.append(f"items {item_count} < {MIN_ITEMS}")
    if rune_count is None or rune_count < MIN_KEYSTONES:
        failures.append(f"keystones {rune_count} < {MIN_KEYSTONES}")

    accent_offenders: list[str] = []
    for champion in champions:
        if ITALIAN_ACCENT_RE.search(champion.name):
            accent_offenders.append(f"champion:{champion.name}")
    for item in items:
        if ITALIAN_ACCENT_RE.search(item.name):
            accent_offenders.append(f"item:{item.name}")
    for rune in runes:
        if ITALIAN_ACCENT_RE.search(rune.name):
            accent_offenders.append(f"rune:{rune.name}")
    if accent_offenders:
        failures.append("accented names found: " + ", ".join(accent_offenders[:5]))

    tags_offenders: list[str] = []
    for champion in champions:
        if not isinstance(champion.tags, list) or not champion.tags:
            tags_offenders.append(champion.name)
    if tags_offenders:
        failures.append("champions without tags: " + ", ".join(tags_offenders[:5]))

    column_names = {column.key for column in Champion.__table__.columns}
    if "roles" in column_names:
        failures.append("Champion model exposes forbidden 'roles' column")

    print("accent_check_ok:", not accent_offenders)
    print("tags_check_ok:", not tags_offenders)
    print("no_roles_column:", "roles" not in column_names)

    if failures:
        print("FAIL")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
