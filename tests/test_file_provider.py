"""Tests for app.file_provider FileProvider (M4/T33, M8/T57)."""

from collections import Counter
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.file_provider import FileProvider
from app.models import ChampionPick, DraftState

MOCK_DRAFT_DIR = Path("tests/mock_drafts")
MOCK_DRAFT_FILES = sorted(MOCK_DRAFT_DIR.glob("*.json"))


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


@pytest.mark.parametrize("json_file", MOCK_DRAFT_FILES, ids=lambda path: path.stem)
@pytest.mark.asyncio
async def test_mock_draft_loads_with_fileprovider(json_file: Path) -> None:
    """DoD T34/T57: each mock draft JSON loads into a valid DraftState."""
    result = await FileProvider(json_file).get_current_state()

    assert isinstance(result, DraftState)
    assert result.patch == "16.10.1"
    assert result.user_role in {"TOP", "JUNGLE", "MID", "ADC", "SUPPORT"}


@pytest.mark.asyncio
async def test_t57_mock_draft_set_has_15_scenarios_and_3_per_role() -> None:
    """DoD T57: 15 scenarios, covering every role exactly 3 times."""
    assert len(MOCK_DRAFT_FILES) == 15

    roles: Counter[str] = Counter()
    for json_file in MOCK_DRAFT_FILES:
        draft = await FileProvider(json_file).get_current_state()
        roles[draft.user_role] += 1

    assert roles == {
        "TOP": 3,
        "JUNGLE": 3,
        "MID": 3,
        "ADC": 3,
        "SUPPORT": 3,
    }


def test_t57_mock_draft_filenames_cover_required_patterns() -> None:
    """Scenario names document the required comp/edge coverage."""
    names = {path.stem for path in MOCK_DRAFT_FILES}

    assert any("ad_heavy" in name for name in names)
    assert any("ap_heavy" in name for name in names)
    assert any("balanced" in name for name in names)
    assert any("first_pick" in name for name in names)
    assert any("last_pick" in name for name in names)
    assert any("aggressive_bans" in name for name in names)
    assert any("meta_picks_out" in name for name in names)
