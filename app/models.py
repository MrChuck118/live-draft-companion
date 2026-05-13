"""Pydantic models for the draft state captured from LCU or sim files (M2/T13)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChampionPick(BaseModel):
    """A pick slot in a team during champion select."""

    role: str
    champion: str | None = None


class Action(BaseModel):
    """An LCU champion-select action (ban or pick)."""

    action_id: int
    actor_cell_id: int
    type: str
    completed: bool


class DraftState(BaseModel):
    """Normalized champion-select state used by prompt builder and validators."""

    patch: str
    user_role: str
    bans: list[str]
    enemy_team: list[ChampionPick]
    ally_team: list[ChampionPick]
    actions: list[Action]
    local_player_cell_id: int


class SuggestionItem(BaseModel):
    """A single AI pick suggestion (M2/T14)."""

    rank: int
    champion: str
    build_path: list[str] = Field(min_length=3, max_length=4)
    keystone: str
    explanation: str = Field(max_length=150)


class SuggestionOutput(BaseModel):
    """Top-3 AI pick suggestions for a draft state (M2/T14)."""

    patch: str
    suggestions: list[SuggestionItem] = Field(min_length=3, max_length=3)
