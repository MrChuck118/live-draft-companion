"""Prompt builder loading system.md and user_template.md and returning (system, user) (M3/T25)."""

from pathlib import Path

from app.models import ChampionPick, DraftState

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _format_bans(bans: list[str]) -> str:
    """Format the 5 ban slots as a numbered list with placeholder for empty slots."""
    lines = []
    for index, ban in enumerate(bans, start=1):
        name = ban if ban else "(non bannato)"
        lines.append(f"{index}. {name}")
    return "\n".join(lines)


def _format_picks(picks: list[ChampionPick]) -> str:
    """Format team picks as 'role: champion' lines with placeholder for empty slots."""
    lines = []
    for pick in picks:
        champion = pick.champion if pick.champion else "(non pickato)"
        lines.append(f"{pick.role}: {champion}")
    return "\n".join(lines)


def build_prompt(draft_state: DraftState, champion_data: dict) -> tuple[str, str]:
    """Build (system_prompt, user_prompt) by loading prompt files and substituting placeholders."""
    system_prompt = (_PROMPTS_DIR / "system.md").read_text(encoding="utf-8")
    template = (_PROMPTS_DIR / "user_template.md").read_text(encoding="utf-8")

    bans_list = _format_bans(draft_state.bans)
    enemy_picks = _format_picks(draft_state.enemy_team)
    ally_picks = _format_picks(draft_state.ally_team)

    user_prompt = (
        template
        .replace("{patch}", draft_state.patch)
        .replace("{user_role}", draft_state.user_role)
        .replace("{bans_list}", bans_list)
        .replace("{enemy_picks_with_roles}", enemy_picks)
        .replace("{ally_picks_with_roles}", ally_picks)
    )

    return system_prompt, user_prompt
