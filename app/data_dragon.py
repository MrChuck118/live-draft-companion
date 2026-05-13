"""Data Dragon helpers for League static data."""

from __future__ import annotations

from typing import Any

import httpx
from sqlalchemy import delete, func, select

from app.db import AsyncSessionLocal, Champion, Item, Meta, Rune, init_db


DATA_DRAGON_VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
DATA_DRAGON_CHAMPION_URL = (
    "https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json"
)
DATA_DRAGON_CHAMPION_IMAGE_URL = (
    "https://ddragon.leagueoflegends.com/cdn/{patch}/img/champion/{image}"
)
DATA_DRAGON_ITEM_URL = "https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/item.json"
DATA_DRAGON_RUNES_URL = (
    "https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/runesReforged.json"
)
DATA_DRAGON_RUNE_ICON_URL = "https://ddragon.leagueoflegends.com/cdn/img/{icon}"


async def fetch_versions() -> str:
    """Return the current League patch from Data Dragon."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(DATA_DRAGON_VERSIONS_URL)
        response.raise_for_status()

    versions: Any = response.json()
    if not isinstance(versions, list) or not versions or not isinstance(versions[0], str):
        raise RuntimeError("Unexpected Data Dragon versions response")

    return versions[0]


async def fetch_champions(patch: str) -> dict[str, dict[str, Any]]:
    """Return champion static data for a Data Dragon patch."""
    url = DATA_DRAGON_CHAMPION_URL.format(patch=patch)
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    payload: Any = response.json()
    champion_data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(champion_data, dict):
        raise RuntimeError("Unexpected Data Dragon champion response")

    champions: dict[str, dict[str, Any]] = {}
    for champion_id, champion in champion_data.items():
        if not isinstance(champion_id, str) or not isinstance(champion, dict):
            raise RuntimeError("Unexpected Data Dragon champion entry")

        name = champion.get("name")
        key = champion.get("key")
        tags = champion.get("tags")
        image = champion.get("image")
        image_name = image.get("full") if isinstance(image, dict) else None
        if not isinstance(name, str) or not isinstance(key, str) or not isinstance(tags, list):
            raise RuntimeError("Unexpected Data Dragon champion fields")
        if not all(isinstance(tag, str) for tag in tags):
            raise RuntimeError("Unexpected Data Dragon champion tags")
        if not isinstance(image_name, str):
            raise RuntimeError("Unexpected Data Dragon champion image")

        champions[champion_id] = {
            "name": name,
            "key": key,
            "tags": tags,
            "image_url": DATA_DRAGON_CHAMPION_IMAGE_URL.format(
                patch=patch,
                image=image_name,
            ),
        }

    return champions


async def fetch_items(patch: str) -> dict[str, dict[str, Any]]:
    """Return item static data for a Data Dragon patch."""
    url = DATA_DRAGON_ITEM_URL.format(patch=patch)
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    payload: Any = response.json()
    item_data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(item_data, dict):
        raise RuntimeError("Unexpected Data Dragon item response")

    items: dict[str, dict[str, Any]] = {}
    for item_id, item in item_data.items():
        if not isinstance(item_id, str) or not isinstance(item, dict):
            raise RuntimeError("Unexpected Data Dragon item entry")

        name = item.get("name")
        stats = item.get("stats")
        if not isinstance(name, str) or not isinstance(stats, dict):
            raise RuntimeError("Unexpected Data Dragon item fields")

        items[item_id] = {
            "name": name,
            "stats": stats,
        }

    return items


async def fetch_runes(patch: str) -> dict[str, dict[str, Any]]:
    """Return keystone rune static data for a Data Dragon patch."""
    url = DATA_DRAGON_RUNES_URL.format(patch=patch)
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    payload: Any = response.json()
    if not isinstance(payload, list):
        raise RuntimeError("Unexpected Data Dragon runes response")

    runes: dict[str, dict[str, Any]] = {}
    for tree in payload:
        if not isinstance(tree, dict):
            raise RuntimeError("Unexpected Data Dragon rune tree")

        tree_name = tree.get("name")
        tree_key = tree.get("key")
        slots = tree.get("slots")
        if not isinstance(tree_name, str) or not isinstance(tree_key, str):
            raise RuntimeError("Unexpected Data Dragon rune tree fields")
        if not isinstance(slots, list) or not slots or not isinstance(slots[0], dict):
            raise RuntimeError("Unexpected Data Dragon rune slots")

        keystone_slot = slots[0].get("runes")
        if not isinstance(keystone_slot, list):
            raise RuntimeError("Unexpected Data Dragon keystone slot")

        for rune in keystone_slot:
            if not isinstance(rune, dict):
                raise RuntimeError("Unexpected Data Dragon rune entry")

            rune_id = rune.get("id")
            key = rune.get("key")
            name = rune.get("name")
            icon = rune.get("icon")
            if not isinstance(rune_id, int):
                raise RuntimeError("Unexpected Data Dragon rune id")
            if not isinstance(key, str) or not isinstance(name, str) or not isinstance(icon, str):
                raise RuntimeError("Unexpected Data Dragon rune fields")

            runes[str(rune_id)] = {
                "name": name,
                "key": key,
                "tree": tree_name,
                "tree_key": tree_key,
                "icon_url": DATA_DRAGON_RUNE_ICON_URL.format(icon=icon),
            }

    return runes


async def populate_cache(patch: str | None = None) -> str:
    """Populate the local Data Dragon SQLite cache for a patch."""
    await init_db()
    cache_patch = patch or await fetch_versions()

    champions = await fetch_champions(cache_patch)
    items = await fetch_items(cache_patch)
    runes = await fetch_runes(cache_patch)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Champion))
            await session.execute(delete(Item))
            await session.execute(delete(Rune))

            session.add_all(
                Champion(
                    id=champion_id,
                    name=champion["name"],
                    key=champion["key"],
                    tags=champion["tags"],
                    image_url=champion["image_url"],
                )
                for champion_id, champion in champions.items()
            )
            session.add_all(
                Item(
                    id=item_id,
                    name=item["name"],
                    stats=item["stats"],
                )
                for item_id, item in items.items()
            )
            session.add_all(
                Rune(
                    id=rune_id,
                    name=rune["name"],
                    key=rune["key"],
                    tree=rune["tree"],
                    tree_key=rune["tree_key"],
                    icon_url=rune["icon_url"],
                )
                for rune_id, rune in runes.items()
            )
            await session.merge(Meta(key="patch", value=cache_patch))

    return cache_patch


async def check_patch_and_refresh(current_patch: str | None = None) -> str:
    """Refresh the local cache when the Data Dragon patch changed."""
    await init_db()
    patch = current_patch or await fetch_versions()

    async with AsyncSessionLocal() as session:
        cached_patch = await _get_cached_patch(session)
        cache_ready = await _has_static_cache(session)

    if cached_patch == patch and cache_ready:
        return patch

    return await populate_cache(patch)


async def _get_cached_patch(session: Any) -> str | None:
    meta = await session.get(Meta, "patch")
    if meta is None:
        return None
    return meta.value


async def _has_static_cache(session: Any) -> bool:
    champion_count = await session.scalar(select(func.count()).select_from(Champion))
    item_count = await session.scalar(select(func.count()).select_from(Item))
    rune_count = await session.scalar(select(func.count()).select_from(Rune))
    return bool(champion_count and item_count and rune_count)
