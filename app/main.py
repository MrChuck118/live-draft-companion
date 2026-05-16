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
from pathlib import Path
from typing import Literal

import httpx
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.data_dragon import check_patch_and_refresh
from app.db import init_db
from app.lcu_provider import LockfileError
from app.models import DraftState
from app.providers import get_draft_state_provider
from app.suggestion_service import (
    HistoryRepository,
    SuggestionError,
    SuggestionService,
)

# HTTP status per error_code (4xx user input, 5xx external services). T49b.
_ERROR_STATUS = {
    "invalid_input": 422,
    "ai_unavailable": 503,
    "ai_output_invalid": 502,
    "draft_unavailable": 503,
    "history_not_found": 404,
    "history_unavailable": 503,
}
_ERRORS_LOG = Path("logs") / "errors.log"

# Path is relative to the process CWD (repo root in dev / via launcher).
# PyInstaller sys._MEIPASS resolution is deferred to T66 per breakdown.
templates = Jinja2Templates(directory="templates")

logger = logging.getLogger("live_draft_companion")


class HistoryFeedbackRequest(BaseModel):
    """Body for POST /api/history/feedback (T54)."""

    history_id: int = Field(gt=0)
    feedback: Literal["good", "bad"]


def _configure_logging(level_name: str) -> None:
    level = logging.getLevelName(level_name.upper())
    if not isinstance(level, int):
        level = logging.INFO
    logging.basicConfig(level=level)
    logger.setLevel(level)

    # Dedicated ERROR file log (T49b / spec Â§12). Guard against duplicate
    # handlers when the lifespan runs multiple times (e.g. in tests).
    if not any(
        getattr(handler, "_ldc_errors_file", False) for handler in logger.handlers
    ):
        _ERRORS_LOG.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(_ERRORS_LOG, encoding="utf-8")
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        file_handler._ldc_errors_file = True  # type: ignore[attr-defined]
        logger.addHandler(file_handler)


def _error_response(
    error_code: str, user_message: str, log_detail: str
) -> JSONResponse:
    """Uniform error contract: log ERROR + JSON {error_code, user_message}.

    Never leak stack traces or secrets: log_detail stays server-side.
    """
    status = _ERROR_STATUS.get(error_code, 500)
    logger.error("api error [%s] %s", error_code, log_detail)
    return JSONResponse(
        status_code=status,
        content={"error_code": error_code, "user_message": user_message},
    )


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


@app.exception_handler(RequestValidationError)
async def _validation_handler(request: Request, exc: RequestValidationError):
    """Malformed request body -> uniform error contract (T49b)."""
    return _error_response(
        "invalid_input",
        "Dati di input non validi.",
        f"validation error on {request.url.path}: {exc.errors()}",
    )


@app.get("/api/draft-state")
async def draft_state():
    """Return the current DraftState from the active provider (sim or live).

    On a provider failure return the uniform error contract (T49b):
    {"error_code", "user_message"} with a coherent 5xx, no stack trace.
    """
    try:
        provider = get_draft_state_provider(get_settings())
        return await provider.get_current_state()
    except LockfileError as exc:
        return _error_response(
            "draft_unavailable",
            "Client League of Legends non rilevato. Avvia il client e riprova.",
            f"LCU lockfile error: {exc}",
        )
    except (OSError, ValueError, RuntimeError) as exc:
        return _error_response(
            "draft_unavailable",
            "Stato del draft non disponibile, riprova.",
            f"{type(exc).__name__}: {exc}",
        )


@app.post("/api/suggest")
async def suggest(draft_state: DraftState):
    """Thin endpoint: delegate the whole flow to SuggestionService (T45/T45b).

    Body is a DraftState (malformed -> 422 via the validation handler). On a
    controlled SuggestionError return the uniform error contract (T49b) with a
    coherent status, no stack trace or API key.
    """
    try:
        return await SuggestionService().suggest(draft_state)
    except SuggestionError as exc:
        error_code = getattr(exc, "error_code", "ai_unavailable")
        user_message = (
            "I suggerimenti AI non sono validi al momento, riprova."
            if error_code == "ai_output_invalid"
            else "Servizio AI non disponibile, riprova tra poco."
        )
        return _error_response(error_code, user_message, f"SuggestionError: {exc}")


@app.post("/api/history/feedback")
async def history_feedback(request: HistoryFeedbackRequest):
    """Update feedback for one history row (M7b/T54)."""
    try:
        updated = await HistoryRepository().update_feedback(
            request.history_id, request.feedback
        )
    except ValueError as exc:
        return _error_response("invalid_input", "Feedback non valido.", str(exc))
    except SQLAlchemyError as exc:
        return _error_response(
            "history_unavailable",
            "Storico non disponibile, riprova.",
            f"{type(exc).__name__}: {exc}",
        )

    if not updated:
        return _error_response(
            "history_not_found",
            "Voce dello storico non trovata.",
            f"history_id not found: {request.history_id}",
        )

    return {
        "status": "ok",
        "history_id": request.history_id,
        "feedback": request.feedback,
    }
