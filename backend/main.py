"""
TruthLens AI — FastAPI Application Entry Point
"""

import logging
import sys

# Fail fast with a clear message on unsupported Python versions instead of
# surfacing confusing import errors from FastAPI / Pydantic.
if sys.version_info < (3, 10):
    raise RuntimeError(
        "TruthLens AI requires Python 3.10 or higher. "
        f"You are running Python {sys.version.split()[0]}. "
        "Install a newer Python from https://www.python.org/downloads/ "
        "and recreate the virtual environment."
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from schemas import HealthResponse
from routes.analyze import router as analyze_router
from routes.auth import router as auth_router
from exceptions import (
    GroqAPIError,
    AnalysisParsingError,
    groq_api_error_handler,
    analysis_parsing_error_handler,
    generic_error_handler,
)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("truthlens")

# ── Application ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="TruthLens AI API",
    description="AI-powered news analysis and misinformation detection API.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
# NOTE: "Authorization" must be allowed — the frontend sends the session
# Bearer token with every request once signed in. Without it, logged-in
# users get CORS preflight failures on ALL endpoints (the analyze page
# then misleadingly reports "could not connect to the server").
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# ── Exception Handlers ────────────────────────────────────────────────────────
app.add_exception_handler(GroqAPIError, groq_api_error_handler)
app.add_exception_handler(AnalysisParsingError, analysis_parsing_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# ── Routes ─────────────────────────────────────────────────────────────────────
app.include_router(analyze_router)
app.include_router(auth_router)


@app.get(
    "/api/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the API and the configured model name.",
)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        service="TruthLens AI API",
        model_configured=settings.GROQ_MODEL,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
