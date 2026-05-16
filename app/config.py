"""Application configuration loaded from .env (M6a/T41).

Spec v2.3 Â§7.1 mandates `pydantic-settings` for env config. This module
centralizes reading of the `.env` keys that were previously read ad-hoc
(e.g. `app/ai_client.py` via `load_dotenv()` + `os.environ`). The AI client
keeps its own direct reads for backward compatibility; this Settings object
is the single source of truth for the FastAPI app lifecycle and providers.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for Live Draft Companion.

    All fields have safe defaults so the app and the test suite can import
    Settings without a populated `.env` (sim mode without AI key is valid;
    AI calls fail later with a controlled error, not at startup).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # DeepSeek direct API (ERRATA-006). Empty is allowed: AI calls surface a
    # controlled error downstream, the app must still start (RF-001).
    deepseek_api_key: str = ""
    llm_model_primary: str = "deepseek-chat"
    llm_model_fallback_1: str = "deepseek-reasoner"

    # Draft provider selection (Demo Mode First: `sim` is the default path).
    draft_provider_mode: str = "sim"
    draft_provider_file: str = "tests/mock_drafts/balanced_mid.json"

    # Runtime logging.
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (read .env once per process)."""
    return Settings()
