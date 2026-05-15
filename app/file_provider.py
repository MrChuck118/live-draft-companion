"""FileProvider: load a pre-recorded DraftState from a JSON file for sim mode (M4/T33)."""

from pathlib import Path

from app.draft_state_provider import DraftStateProvider
from app.models import DraftState


class FileProvider(DraftStateProvider):
    """Load a pre-recorded DraftState from a JSON file (sim/replay mode, MVP-015, RF-018)."""

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)

    async def get_current_state(self) -> DraftState:
        """Read the JSON file and validate it into a DraftState."""
        raw = self._file_path.read_text(encoding="utf-8")
        return DraftState.model_validate_json(raw)
