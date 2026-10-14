"""
TruthLens AI — Offline Heuristic Analyzer (fallback)
=====================================================

Used ONLY when the Groq AI service cannot be reached (missing key,
invalid key, network failure, timeout, rate limit, or bad AI response).

This is a transparent, deterministic, rule-based text-pattern check. It is
NOT a language-model assessment and must never be presented as one: every
result carries mode="offline", the explanation says so up front, and the
limitations repeat it. No scores are fabricated; every listed signal names
the exact pattern that was matched in the text.
"""

import re

from schemas import AnalysisResponse

LABEL_REAL = "Likely Real"
LABEL_FAKE = "Likely Fake"
LABEL_UNVERIFIED = "Unverified / Insufficient Evidence"

# --- Pattern pools (all matched case-insensitively, reported by name) --------

LOADED_WORDS = [
    "shocking",
    "miracle",
    "cure",
    "secret",
    "exposed",
    "hoax",
    "scandal",
    "banned",
    "cover-up",
    "coverup",
]

URGENCY_PHRASES = [
    "breaking",
    "urgent",
    "share before",
    "before it gets deleted",
    "before they delete",
    "forward this",
    "share this",
    "act now",
    "click here",
    "limited time",
    "must share",
]

VAGUE_SOURCE_WORDS = [
    "anonymous",
    "unnamed",
    "insider",
    "sources say",
    "source says",
    "leaked",
    "someone",
    "everyone knows",
    "they don't want you to know",
    "they dont want you to know",
]

ABSOLUTE_WORDS = [
    "always",
    "never",
    " proven",
    "guaranteed",
    "100%",
    "every single",
    "no one doubts",
]

ATTRIBUTION_MARKERS = [
    "according to",
    "said",
    "says",
    "announced",
    "confirmed",
    "reported",
    "stated",
    "published",
    "survey",
    "study",
    "figures",
    "release",
    "methodology",
    "findings",
    "data shows",
    "records show",
]

# Superlatives / exclusivity markers. Counted ONLY in short texts
# (headlines, posts, single-claim statements) where they function as
# punchy overclaims; in long-form reporting they are ordinary vocabulary.
OVERCLAIM_WORDS = [
    "most",
    "least",
    "best",
    "worst",
    "biggest",
    "largest",
    "smallest",
    "only",
]

# Pejorative / accusation vocabulary. A mild signal on its own (disaster and
# crime reporting legitimately uses words like "destroyed"), so it is capped
# and only decisive together with an absence of attribution.
ACCUSATION_WORDS = [
    "lie",
    "lies",
    "lying",
    "liar",
    "corrupt",
    "crooked",
    "destroy",
    "stupid",
    "idiot",
    "moron",
    "shameful",
    "disgrace",
    "cheat",
    "cheating",
]

HEDGE_WORDS = [
    "allegedly",
    "reportedly",
    "unconfirmed",
    "rumor",
    "rumour",
    "appears to",
    "claims",
    "supposedly",
]

REASONS = {
    "no_key": "no Groq API key is configured",
    "bad_key": "the configured key was rejected by the AI service",
    "unreachable": "the AI service could not be reached",
    "rate_limited": "the AI service is rate-limited right now",
    "bad_response": "the AI service returned an unusable response",
}


def _contains_any(text: str, phrases: list[str]) -> list[str]:
    """Return the phrases (lowercased) found in the text."""
    lowered = text.lower()
    return [p for p in phrases if p in lowered]


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 3]


def _caps_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    caps = sum(1 for c in letters if c.isupper())
    return caps / len(letters)


def analyze_offline(text: str, reason: str = "unreachable") -> AnalysisResponse:
    """
    Run the deterministic local check and return a validated response.

    `reason` is one of REASONS keys and is reflected in the explanation so
    the reader always knows WHY they received a heuristic result.
    """
    lowered = text.lower()
    sentences = _split_sentences(text)
    signals: list[str] = []
    fake_points = 0
    real_points = 0

    # 1. Capitalisation shouting
    caps = _caps_ratio(text)
    if caps > 0.25 and len(text) > 60:
        signals.append(
            f"Heavy use of capital letters ({caps:.0%} of letters are uppercase), "
            "a common sensationalism marker"
        )
        fake_points += 2

    # 2. Exclamation spam
    exclamations = text.count("!")
    if exclamations >= 3:
        signals.append(
            f"{exclamations} exclamation marks — emphatic punctuation often used "
            "to manufacture urgency"
        )
        fake_points += 1

    # 3. Loaded / sensational vocabulary
    loaded = _contains_any(lowered, LOADED_WORDS)
    if loaded:
        shown = ", ".join(f"'{w}'" for w in loaded[:5])
        signals.append(f"Loaded or sensational words detected: {shown}")
        fake_points += min(len(loaded), 4)

    # 4. Virality / urgency pressure
    urgency = _contains_any(lowered, URGENCY_PHRASES)
    if urgency:
        shown = ", ".join(f"'{p}'" for p in urgency[:4])
        signals.append(f"Share-pressure / urgency phrasing detected: {shown}")
        fake_points += 2

    # 5. Vague sourcing
    vague = _contains_any(lowered, VAGUE_SOURCE_WORDS)
    if vague:
        shown = ", ".join(f"'{p}'" for p in vague[:4])
        signals.append(
            f"Claims lean on unnamed or vague sourcing ({shown}) instead of "
            "named, checkable sources"
        )
        fake_points += 2

    # 6. Absolutist language
    absolutes = _contains_any(lowered, ABSOLUTE_WORDS)
    if absolutes:
        signals.append("Absolutist language ('always/never/proven'-style claims)")
        fake_points += 1

    # 7. Attribution markers (positive — checkable anchors)
    attribution = _contains_any(lowered, ATTRIBUTION_MARKERS)
    if attribution:
        real_points += 2

    # 8. Concrete numbers (positive — independently checkable)
    has_numbers = bool(re.search(r"\d", text))
    if has_numbers:
        real_points += 1

    # 9. Hedging / unconfirmed-status language (neutral — needs verification)
    hedges = _contains_any(lowered, HEDGE_WORDS)

    # 10. No attribution at all
    if not attribution and not has_numbers and '"' not in text and "'" not in text:
        signals.append(
            "No named official, document, figure, or quotation to verify against"
        )
        fake_points += 1

    # 11. Overclaim superlatives in short texts (headline/claim style)
    short_text = len(text) < 300
    if short_text:
        overclaims = _contains_any(lowered, OVERCLAIM_WORDS)
        if overclaims:
            shown = ", ".join(f"'{w}'" for w in overclaims[:4])
            signals.append(
                f"Superlative/exclusive framing typical of overclaims: {shown}"
            )
            fake_points += min(len(overclaims), 2)

    # 12. Pejorative / accusation vocabulary (capped — also occurs in
    # legitimate crime/disaster reporting)
    accusations = _contains_any(lowered, ACCUSATION_WORDS)
    if accusations:
        shown = ", ".join(f"'{w}'" for w in accusations[:4])
        signals.append(f"Pejorative or accusatory language detected: {shown}")
        fake_points += min(len(accusations), 2)
        if short_text and not attribution:
            signals.append(
                "Accusatory claim presented with no attributable source"
            )
            fake_points += 2

    # --- Classification (transparent thresholds) ---
    if fake_points >= 4:
        classification = LABEL_FAKE
        verdict = (
            f"matched {fake_points} misinformation-style pattern(s): "
            + "; ".join(s.lower() for s in signals[:3])
        )
    elif real_points >= 3 and fake_points <= 2:
        classification = LABEL_REAL
        verdict = (
            "uses attributed language and checkable details, with "
            + ("no sensational patterns detected" if not signals else "only minor warning signs")
        )
    else:
        classification = LABEL_UNVERIFIED
        verdict = (
            "does not contain enough verifiable anchors (named sources, figures, "
            "documents) to support a stronger reading"
        )

    # --- Claims worth verifying: longest factual-looking sentences ---
    candidates = [
        s for s in sentences
        if re.search(r"\d", s) or len(s.split()) >= 12
    ]
    claims = [s[:220] for s in candidates[:4]]
    if not claims and sentences:
        claims = [sentences[0][:220]]
    if hedges:
        claims.append(
            "Whether the hedged/rumoured elements (" + ", ".join(f"'{h}'" for h in hedges[:3]) + ") describe real events"
        )

    # --- Summary: lead sentences ---
    summary = " ".join(sentences[:2])[:300]
    if len(" ".join(sentences[:2])) > 300:
        summary = summary.rsplit(" ", 1)[0] + "…"

    reason_text = REASONS.get(reason, REASONS["unreachable"])
    explanation = (
        f"Offline heuristic check ({reason_text}): this text {verdict}. "
        "This judgment comes from local text-pattern rules only — "
        "no language model assessed it."
    )

    return AnalysisResponse(
        classification=classification,
        explanation=explanation,
        summary=summary or "No summary could be produced from the supplied text.",
        suspicious_signals=signals,
        claims_to_verify=claims,
        verification_steps=[
            "Search for the core claim on the official channels of any named organisation",
            "Check whether reputable independent outlets corroborate it",
            "Look for the original document, footage, or dataset behind the claim",
        ],
        evidence_limitations=[
            "Offline heuristic check only — the AI service was unreachable, so no language-model assessment was performed",
            "No independent external source verification was performed by this tool",
        ],
        mode="offline",
    )
