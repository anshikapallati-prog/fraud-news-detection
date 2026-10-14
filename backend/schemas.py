"""
TruthLens AI — Pydantic Schemas
Request and response models for the analysis API.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from enum import Enum


class Classification(str, Enum):
    """Possible classification outcomes."""
    LIKELY_REAL = "Likely Real"
    LIKELY_FAKE = "Likely Fake"
    UNVERIFIED = "Unverified / Insufficient Evidence"


class AnalysisRequest(BaseModel):
    """Request body for the /api/analyze endpoint."""
    text: str = Field(
        ...,
        min_length=20,
        max_length=15000,
        description="The news headline, article, or social media post to analyze.",
        examples=["Breaking: Scientists discover new planet in habitable zone of nearby star system."],
    )


class AnalysisResponse(BaseModel):
    """Structured analysis result returned by the AI."""
    classification: str = Field(
        ...,
        description="One of: 'Likely Real', 'Likely Fake', or 'Unverified / Insufficient Evidence'.",
    )
    explanation: str = Field(
        ...,
        description="A short explanation of why this classification was given.",
    )
    summary: str = Field(
        ...,
        description="A brief, easy-to-understand summary of the submitted text.",
    )
    suspicious_signals: list[str] = Field(
        default_factory=list,
        description="Potentially suspicious or misleading language patterns found in the text.",
    )
    claims_to_verify: list[str] = Field(
        default_factory=list,
        description="Key factual claims in the text that should be independently verified.",
    )
    verification_steps: list[str] = Field(
        default_factory=list,
        description="Suggested steps the reader can take to fact-check the claims.",
    )
    evidence_limitations: list[str] = Field(
        default_factory=list,
        description="Limitations of this analysis (e.g., no external source verification performed).",
    )
    mode: str = Field(
        default="ai",
        description="'ai' for a language-model assessment, 'offline' for the local heuristic fallback.",
    )


class HealthResponse(BaseModel):
    """Response for the health check endpoint."""
    model_config = ConfigDict(protected_namespaces=())

    status: str = "ok"
    service: str = "TruthLens AI API"
    model_configured: str = ""


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Optional[str] = None
