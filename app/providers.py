"""DraftStateProvider factory: select LCU (live) or File (sim) from config (M6a/T44).

Keeps endpoints thin and the LCU-vs-file choice in one place (spec Â§8.1
DraftStateProvider; Demo Mode First: `sim` is the default path).
"""

from __future__ import annotations

from app.config import Settings
from app.draft_state_provider import DraftStateProvider
from app.file_provider import FileProvider
from app.lcu_provider import LCUProvider


def get_draft_state_provider(settings: Settings) -> DraftStateProvider:
    """Return the provider selected by `DRAFT_PROVIDER_MODE` in the environment."""
    mode = settings.draft_provider_mode.strip().lower()
    if mode == "sim":
        return FileProvider(settings.draft_provider_file)
    if mode == "live":
        return LCUProvider()
    raise ValueError(
        f"Unknown DRAFT_PROVIDER_MODE '{settings.draft_provider_mode}' (expected 'sim' or 'live')"
    )
