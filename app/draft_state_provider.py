"""Abstract DraftStateProvider interface for live (LCU) and sim (File) sources (M4/T32)."""

from abc import ABC, abstractmethod

from app.models import DraftState


class DraftStateProvider(ABC):
    """Contract for any draft-state source; consumers do not know if it is LCU or file-based."""

    @abstractmethod
    async def get_current_state(self) -> DraftState:
        """Return the current normalized draft state."""
        ...
