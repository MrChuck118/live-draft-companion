"""FastAPI application + lifecycle (M6a/T41).

Startup: init the SQLite schema and refresh the Data Dragon cache when the
patch changed. Network failure on Data Dragon is non-fatal (spec Â§12: "Data
Dragon CDN non risponde -> uso cache locale"): the app must still start so
the user sees the UI (RF-001). The HTTP port is NOT bound here; the launcher
(T42) owns port selection (spec Â§7.1 "porta libera auto-rilevata").

Endpoints (GET /, /api/draft-state, ...) are out of scope for T41 and added
in T43/T44.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.data_dragon import check_patch_and_refresh
from app.db import init_db
from app.models import DraftState
from app.providers import get_draft_state_provider

# Path is relative to the process CWD (repo root in dev / via launcher).
# PyInstaller sys._MEIPASS resolution is deferred to T66 per breakdown.
templates = Jinja2Templates(directory="templates")

logger = logging.getLogger("live_draft_companion")


def _configure_logging(level_name: str) -> None:
    level = logging.getLevelName(level_name.upper())
    if not isinstance(level, int):
        level = logging.INFO
    logging.basicConfig(level=level)
    logger.setLevel(level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: prepare local caches on startup, clean up on shutdown."""
    settings = get_settings()
    _configure_logging(settings.log_level)

    await init_db()
    try:
        patch = await check_patch_and_refresh()
        logger.info("Data Dragon cache ready (patch %s)", patch)
    except (httpx.HTTPError, RuntimeError) as exc:
        # Non-fatal: fall back to whatever local cache exists (spec Â§12).
        logger.warning(
            "Data Dragon refresh skipped (%s); using local cache if present", exc
        )

    logger.info("App ready")
    yield
    logger.info("App shutting down")


app = FastAPI(
    title="Live Draft Companion",
    description="Assistente AI per il draft di League of Legends (MVP).",
    version="0.1.0",
    lifespan=lifespan,
)

# Serve Vanilla JS / static assets (ERRATA-002). Path relative to CWD;
# PyInstaller sys._MEIPASS resolution deferred to T66 per breakdown.
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the base UI shell (initial state: waiting for the LoL client).

    Minimal page only (T43); full Tailwind UI + sections is T46, the polling
    JS is T47.
    """
    return templates.TemplateResponse(request, "index.html")


@app.get("/api/draft-state")
async def draft_state() -> DraftState:
    """Return the current DraftState from the active provider (sim or live).

    Provider is chosen from `.env` (MVP-004). On a provider failure return a
    controlled 503 (no stack trace); the full error-code/user-message
    mapping is T49b, not anticipated here.
    """
    provider = get_draft_state_provider(get_settings())
    try:
        return await provider.get_current_state()
    except (OSError, ValueError, RuntimeError) as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Stato draft non disponibile: {type(exc).__name__}",
        ) from exc
