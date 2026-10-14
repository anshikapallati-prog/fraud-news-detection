"""
TruthLens AI — Analysis Route
POST /api/analyze endpoint.
"""

from fastapi import APIRouter
from schemas import AnalysisRequest, AnalysisResponse, ErrorResponse
from groq_service import analyze_news

router = APIRouter()


@router.post(
    "/api/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        429: {"model": ErrorResponse, "description": "Rate limited"},
        500: {"model": ErrorResponse, "description": "Server error"},
        502: {"model": ErrorResponse, "description": "AI service error"},
        503: {"model": ErrorResponse, "description": "AI service unavailable"},
        504: {"model": ErrorResponse, "description": "AI service timeout"},
    },
    summary="Analyze news text for misinformation signals",
    description=(
        "Submit a news headline, article, or social media post. "
        "The text is sent to the configured Groq-hosted language model for analysis. "
        "Returns a structured assessment including classification, suspicious signals, "
        "claims to verify, and recommended fact-checking steps."
    ),
)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze submitted news text and return structured findings."""
    result = await analyze_news(request.text)
    return result
