"""
TruthLens AI — Analysis Endpoint Tests
Uses mocked Groq responses so no real API calls are made.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport
from main import app


VALID_TEST_KEY = "gsk_test_key_for_pytest_only_1234567890"


@pytest.fixture
def groq_key(monkeypatch):
    """Give the service a well-formed (but fake) key so the Groq path runs mocked."""
    import groq_service

    monkeypatch.setattr(groq_service.settings, "GROQ_API_KEY", VALID_TEST_KEY)
    monkeypatch.setattr(groq_service.settings, "GROQ_MODEL", "pytest-mock-model")


MOCK_GROQ_RESPONSE = {
    "classification": "Unverified / Insufficient Evidence",
    "explanation": "The text makes claims that cannot be independently verified from the provided content alone.",
    "summary": "The text presents a claim about a recent event without citing specific sources.",
    "suspicious_signals": ["No source attribution for the main claim"],
    "claims_to_verify": ["The central factual claim in the article"],
    "verification_steps": [
        "Search for the original announcement from official sources",
        "Check reputable independent news outlets for corroboration",
    ],
    "evidence_limitations": [
        "No independent external source verification was performed by this tool"
    ],
}


def _make_mock_completion(response_data: dict) -> MagicMock:
    """Create a mock Groq chat completion object."""
    mock_message = MagicMock()
    mock_message.content = json.dumps(response_data)
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    return mock_completion


@pytest.mark.asyncio
async def test_analyze_empty_input():
    """Empty text should return 422 validation error."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/analyze", json={"text": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_too_short():
    """Text shorter than minimum should return 422."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/analyze", json={"text": "Too short"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_missing_text():
    """Missing text field should return 422."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/analyze", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_valid_input(groq_key):
    """Valid input with mocked Groq response should return 200 with structured data."""
    mock_completion = _make_mock_completion(MOCK_GROQ_RESPONSE)

    with patch("groq_service.Groq") as MockGroq:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_completion
        MockGroq.return_value = mock_client

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/analyze",
                json={
                    "text": "Breaking news: Scientists have discovered a new planet in the habitable zone of a nearby star system, according to unnamed sources."
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "ai"
    assert "classification" in data
    assert "explanation" in data
    assert "summary" in data
    assert "suspicious_signals" in data
    assert "claims_to_verify" in data
    assert "verification_steps" in data
    assert "evidence_limitations" in data


@pytest.mark.asyncio
async def test_analyze_malformed_groq_response(groq_key):
    """Malformed AI response should fall back to a labeled offline result (200)."""
    mock_message = MagicMock()
    mock_message.content = "This is not valid JSON at all"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    with patch("groq_service.Groq") as MockGroq:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_completion
        MockGroq.return_value = mock_client

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/analyze",
                json={
                    "text": "This is a valid input text that is long enough to pass validation for the analysis endpoint."
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "offline"
    assert "offline" in data["explanation"].lower()


@pytest.mark.asyncio
async def test_analyze_groq_rate_limit(groq_key):
    """Groq rate limit should fall back to a labeled offline result (200)."""
    from groq import RateLimitError

    with patch("groq_service.Groq") as MockGroq:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {}
        mock_client.chat.completions.create.side_effect = RateLimitError(
            message="Rate limit exceeded",
            response=mock_response,
            body=None,
        )
        MockGroq.return_value = mock_client

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/analyze",
                json={
                    "text": "This is a valid input text that is long enough to pass validation for the analysis endpoint."
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "offline"
    assert "rate-limit" in data["explanation"]
