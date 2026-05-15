"""Tests for app.file_provider FileProvider (M4/T33)."""

import pytest
from pydantic import ValidationError

from app.file_provider import FileProvider
from app.models import ChampionPick, DraftState


def _balanced_mid_draft() -> DraftState:
    return DraftState(
        patch="16.10.1",
        user_role="MID",
        bans=["Yasuo", "Zed", "Yone", "Akali", "Sylas"],
        enemy_team=[
            ChampionPick(role="TOP", champion="Ornn"),
            ChampionPick(role="MID", champion="Orianna"),
        ],
        ally_team=[
            ChampionPick(role="MID", champion=None),
            ChampionPick(role="ADC", champion="Kai'Sa"),
        ],
        actions=[],
        local_player_cell_id=2,
    )


@pytest.mark.asyncio
async def test_file_provider_loads_valid_draft(tmp_path) -> None:
    draft = _balanced_mid_draft()
    json_file = tmp_path / "balanced_mid.json"
    json_file.write_text(draft.model_dump_json(), encoding="utf-8")

    result = await FileProvider(json_file).get_current_state()

    assert isinstance(result, DraftState)
    assert result.user_role == "MID"
    assert result.patch == "16.10.1"
    assert result.bans == ["Yasuo", "Zed", "Yone", "Akali", "Sylas"]
    assert result.enemy_team[1].champion == "Orianna"
    assert result.ally_team[0].champion is None


@pytest.mark.asyncio
async def test_file_provider_accepts_str_path(tmp_path) -> None:
    draft = _balanced_mid_draft()
    json_file = tmp_path / "balanced_mid.json"
    json_file.write_text(draft.model_dump_json(), encoding="utf-8")

    result = await FileProvider(str(json_file)).get_current_state()

    assert isinstance(result, DraftState)
    assert result.user_role == "MID"


@pytest.mark.asyncio
async def test_file_provider_invalid_schema_raises(tmp_path) -> None:
    bad_file = tmp_path / "bad.json"
    bad_file.write_text('{"patch": "16.10.1"}', encoding="utf-8")

    with pytest.raises(ValidationError):
        await FileProvider(bad_file).get_current_state()


@pytest.mark.parametrize(
    "name",
    [
        "balanced_mid",
        "ad_heavy_top",
        "mid_meta_banned",
        "first_pick_top",
        "last_pick_support",
    ],
)
@pytest.mark.asyncio
async def test_mock_draft_loads_with_fileprovider(name: str) -> None:
    """DoD T34: each of the 5 mock draft JSON files loads via FileProvider into a valid DraftState."""
    result = await FileProvider(f"tests/mock_drafts/{name}.json").get_current_state()

    assert isinstance(result, DraftState)
    assert result.patch == "16.10.1"
    assert result.user_role in {"TOP", "JUNGLE", "MID", "ADC", "SUPPORT"}
