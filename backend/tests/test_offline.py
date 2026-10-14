"""
TruthLens AI — Offline Fallback Tests
Verifies the labeled local heuristic used when the AI service is unavailable.
"""

import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport
from main import app
from offline_analysis import analyze_offline


SENSATIONAL = (
    "SHOCKING!!! The government has been SECRETLY putting mind-control chemicals "
    "in the water supply for 20 YEARS and the mainstream media REFUSES to report "
    "it! An insider who cannot be named confirms EVERYTHING. Share this before it "
    "gets DELETED!"
)

MEASURED = (
    "The National Statistics Directorate said Tuesday that consumer prices rose "
    "2.4 percent over the twelve months to September, down from 2.9 percent in "
    "August. The full methodology and regional breakdowns were published on the "
    "directorate's website."
)


def _assert_shape(result) -> None:
    """Every offline result must be complete and honestly labeled."""
    assert result.mode == "offline"
    assert result.classification in {
        "Likely Real",
        "Likely Fake",
        "Unverified / Insufficient Evidence",
    }
    assert "offline" in result.explanation.lower()
    assert "no language model" in result.explanation.lower()
    assert result.summary
    assert len(result.verification_steps) >= 1
    assert len(result.evidence_limitations) >= 1
    assert any("offline" in limit.lower() for limit in result.evidence_limitations)


def test_offline_flags_sensational_text():
    result = analyze_offline(SENSATIONAL, reason="unreachable")
    _assert_shape(result)
    assert result.classification == "Likely Fake"
    assert len(result.suspicious_signals) >= 2


def test_offline_rates_measured_text():
    result = analyze_offline(MEASURED, reason="unreachable")
    _assert_shape(result)
    assert result.classification == "Likely Real"


def test_offline_reasons_surface_in_explanation():
    assert "no groq api key" in analyze_offline(MEASURED, "no_key").explanation.lower()
    assert "rejected" in analyze_offline(MEASURED, "bad_key").explanation.lower()
    assert "rate-limit" in analyze_offline(MEASURED, "rate_limited").explanation.lower()


@pytest.mark.asyncio
async def test_no_key_returns_offline_without_calling_groq(monkeypatch):
    """Missing key → 200 offline result, Groq SDK never touched."""
    import groq_service

    monkeypatch.setattr(groq_service.settings, "GROQ_API_KEY", "")
    with patch("groq_service.Groq") as MockGroq:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/analyze",
                json={"text": MEASURED},
            )
    MockGroq.assert_not_called()
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "offline"
    assert data["classification"] == "Likely Real"


@pytest.mark.asyncio
async def test_bad_key_format_returns_offline_without_calling_groq(monkeypatch):
    """Clearly non-Groq key → 200 offline result, no doomed network call."""
    import groq_service

    monkeypatch.setattr(
        groq_service.settings, "GROQ_API_KEY", "AQ.definitely-not-a-groq-key"
    )
    with patch("groq_service.Groq") as MockGroq:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/analyze",
                json={"text": SENSATIONAL},
            )
    MockGroq.assert_not_called()
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "offline"
    assert data["classification"] == "Likely Fake"
    assert "rejected" in data["explanation"].lower()
