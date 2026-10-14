#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TruthLens AI — Synthetic Demo Dataset Generator
================================================

Builds `truthlens_news_dataset.csv` and `truthlens_news_dataset.json`:
a 500-row, three-class news-text dataset used to demonstrate and evaluate
the TruthLens AI classifier.

!!! IMPORTANT — WHAT THIS DATASET IS *NOT* !!!
------------------------------------------------
Every row is SYNTHETIC (hand-curated templates + programmatic variation).
None of the text is real reporting, and no statement in it is true.
* All organisations, people, places, agencies and statistics are FICTIONAL.
* The "label" column encodes the *characteristic pattern* of the text
  (attributed + measured reporting vs. sensational virality vs. an
  unverifiable circulating claim) — it is NOT a fact-check verdict.
* Do NOT use this to train or benchmark a real-world fact-checking model
  and do NOT cite it as evidence about any real person or organisation.

For genuine ML research, use a real, licensed corpus instead — see
`data/README.md` for a list (LIAR, FakeNewsNet, ISOT, WELFake, …).

Usage
-----
    python generate_dataset.py              # writes CSV + JSON (500 rows)
    python generate_dataset.py --rows 1000  # choose the target size

Requires only the Python standard library (works on Python 3.7+).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 20260101
DEFAULT_ROWS = 500

LABEL_REAL = "Likely Real"
LABEL_FAKE = "Likely Fake"
LABEL_UNVERIFIED = "Unverified / Insufficient Evidence"

CATEGORIES = [
    "Politics",
    "Health",
    "Science",
    "Technology",
    "Finance",
    "Climate",
    "Sports",
    "Entertainment",
    "Crime",
    "Disaster",
]

SOURCE_TYPES = ["headline", "social_post", "full_article"]

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "truthlens_news_dataset.csv")
JSON_PATH = os.path.join(HERE, "truthlens_news_dataset.json")

SYNTHETIC_NOTE = "SYNTHETIC DEMO DATA — fictional entities, not real news"

# ---------------------------------------------------------------------------
# 1. Curated seeds — hand-written, high-quality examples
# ---------------------------------------------------------------------------

CURATED = [
    # ---------------------------- Likely Real ------------------------------
    {
        "text": (
            "The National Statistics Directorate said Tuesday that consumer prices rose "
            "2.4 percent over the twelve months to September, down from 2.9 percent in "
            "August. In a briefing, chief economist Marta Delgado attributed the slowdown "
            "to lower energy costs and easing food prices. The full methodology and "
            "regional breakdowns were published on the directorate's website."
        ),
        "label": LABEL_REAL,
        "category": "Finance",
        "source_type": "full_article",
        "signals": "",
        "notes": "Named agency, named official, precise figure, published methodology.",
    },
    {
        "text": "Health authority reports 3.1% fall in seasonal respiratory cases",
        "label": LABEL_REAL,
        "category": "Health",
        "source_type": "headline",
        "signals": "",
        "notes": "Measured, attributable, non-sensational headline.",
    },
    {
        "text": (
            "A regional transit authority confirmed on Thursday that repairs to the "
            "northern line will extend the average commute by roughly eight minutes until "
            "late November. A spokesperson said replacement buses would run every six "
            "minutes during peak periods and that timetables had been posted at every "
            "affected station."
        ),
        "label": LABEL_REAL,
        "category": "Technology",
        "source_type": "full_article",
        "signals": "",
        "notes": "Specific, verifiable operational details; attributed to a spokesperson.",
    },
    {
        "text": (
            "The Coastal Weather Service issued a flood watch for low-lying districts "
            "along the eastern estuary, effective from Friday evening. Forecasters expect "
            "between 40 and 60 millimetres of rain over 24 hours. Residents were advised "
            "to avoid underpasses and to monitor updates on the service's official feed."
        ),
        "label": LABEL_REAL,
        "category": "Disaster",
        "source_type": "full_article",
        "signals": "",
        "notes": "Official advisory with ranges, timing and actionable guidance.",
    },
    {
        "text": "University team publishes peer-reviewed study on soil carbon retention",
        "label": LABEL_REAL,
        "category": "Science",
        "source_type": "headline",
        "signals": "",
        "notes": "Peer-review status stated; no overclaiming.",
    },
    {
        "text": (
            "The National Space Research Council said its second lunar mapping satellite "
            "completed its commissioning phase and began returning images last week. "
            "Mission director Ilan Petrov said the first calibrated scans matched "
            "pre-launch simulations. Raw data will be released to researchers on a rolling "
            "basis, the council added."
        ),
        "label": LABEL_REAL,
        "category": "Science",
        "source_type": "full_article",
        "signals": "",
        "notes": "Attributed, specific, includes how the claim can be checked.",
    },
    {
        "text": (
            "Quarterly filings show the manufacturer's operating margin narrowed to "
            "6.8 percent from 8.1 percent a year earlier. Executives told analysts on a "
            "conference call that higher component costs accounted for most of the "
            "difference. The figures are audited and appear in the company's published "
            "statutory accounts."
        ),
        "label": LABEL_REAL,
        "category": "Finance",
        "source_type": "full_article",
        "signals": "",
        "notes": "Numbers traced to audited filings; balanced framing.",
    },
    {
        "text": "Ministry confirms rescheduled vaccination drive for two districts",
        "label": LABEL_REAL,
        "category": "Health",
        "source_type": "headline",
        "signals": "",
        "notes": "Plain, specific, official.",
    },
    {
        "text": (
            "Election officials said turnout in Sunday's municipal ballot reached "
            "58.3 percent, with 94 percent of precincts reporting. Observers from three "
            "accredited monitoring bodies described the process as orderly, while noting "
            "long queues at two central polling stations. Final certified results are due "
            "within five days."
        ),
        "label": LABEL_REAL,
        "category": "Politics",
        "source_type": "full_article",
        "signals": "",
        "notes": "Provisional figures flagged as provisional; independent observers named.",
    },
    {
        "text": (
            "Researchers at a public university reported that a 12-week walking programme "
            "was associated with modest improvements in self-reported sleep quality among "
            "142 participants. The authors cautioned that the sample was small, that "
            "results were observational, and that the study had not yet been replicated."
        ),
        "label": LABEL_REAL,
        "category": "Health",
        "source_type": "full_article",
        "signals": "",
        "notes": "Explicit limitations — a hallmark of careful reporting.",
    },
    {
        "text": "Grid operator says peak demand fell after efficiency subsidy began",
        "label": LABEL_REAL,
        "category": "Climate",
        "source_type": "headline",
        "signals": "",
        "notes": "Measurable claim tied to a named operator.",
    },
    {
        "text": (
            "The athletics federation confirmed that the national trials will be held in "
            "the capital from 4 to 6 August. A federation statement said qualifying times "
            "would follow the published continental standard and that anti-doping testing "
            "would be conducted by an independent agency."
        ),
        "label": LABEL_REAL,
        "category": "Sports",
        "source_type": "full_article",
        "signals": "",
        "notes": "Verifiable logistics; governance details included.",
    },
    # ---------------------------- Likely Fake ------------------------------
    {
        "text": (
            "SHOCKING!!! The government has been SECRETLY putting mind-control chemicals "
            "in the water supply for 20 YEARS and the mainstream media REFUSES to report "
            "it! A whistleblower who cannot be named confirms EVERYTHING. Share this "
            "before it gets DELETED — they are trying to silence us!"
        ),
        "label": LABEL_FAKE,
        "category": "Health",
        "source_type": "social_post",
        "signals": (
            "All-caps sensationalism; unnamed whistleblower; claim of media cover-up; "
            "urgency and share-before-deleted framing; no verifiable evidence"
        ),
        "notes": "Classic virality pattern; every entity is fictional.",
    },
    {
        "text": (
            "Doctors are BANNING this one kitchen ingredient that CURES every known "
            "disease — and Big Pharma is spending BILLIONS to keep it off the shelves! "
            "Thousands already healed. Click the link NOW before this is taken down!"
        ),
        "label": LABEL_FAKE,
        "category": "Health",
        "source_type": "social_post",
        "signals": (
            "Miracle-cure framing; conspiracy about a suppressed industry; absolute "
            "medical claim; click-urgency; no study, author or institution cited"
        ),
        "notes": "Health-misinformation template.",
    },
    {
        "text": (
            "BREAKING: A leaked document PROVES the national election was stolen by "
            "a secret cabal. Officials refuse to comment, which everyone knows means "
            "it is true. Patriot sources say the real results will be revealed any day "
            "now. Forward this to everyone you know!"
        ),
        "label": LABEL_FAKE,
        "category": "Politics",
        "source_type": "social_post",
        "signals": (
            "Unsubstantiated 'leaked document'; absence of denial treated as proof; "
            "vague 'patriot sources'; no document, court or official cited"
        ),
        "notes": "Political-misinformation template.",
    },
    {
        "text": (
            "This fruit found ONLY in one remote valley makes you lose 10 kg in 3 DAYS "
            "without diet or exercise. Scientists are FURIOUS because it will destroy "
            "the weight-loss industry. Limited supply — order in the next 10 minutes!"
        ),
        "label": LABEL_FAKE,
        "category": "Health",
        "source_type": "social_post",
        "signals": (
            "Impossible efficacy claim; artificial scarcity and countdown urgency; "
            "no named expert; commercial sales funnel"
        ),
        "notes": "Commercial-misinformation template.",
    },
    {
        "text": "EXPOSED: The entire 'energy crisis' is a hoax invented to raise your bills",
        "label": LABEL_FAKE,
        "category": "Climate",
        "source_type": "headline",
        "signals": "Blanket denial without evidence; emotionally loaded framing",
        "notes": "Sensational headline with no supporting substance.",
    },
    {
        "text": (
            "A 'former NASA insider' says the space agency has been faking every launch "
            "since the 1970s and that the footage you see is computer-generated. Major "
            "newsrooms are covering it up. The insider is now in hiding from the "
            "authorities, which proves the story is real."
        ),
        "label": LABEL_FAKE,
        "category": "Science",
        "source_type": "full_article",
        "signals": (
            "Anonymous 'insider'; unfalsifiable cover-up claim; circular reasoning "
            "(hiding proves truth); no documentation"
        ),
        "notes": "Conspiracy-reasoning template.",
    },
    {
        "text": (
            "A celebrity 'doctor' reveals the medical establishment has been lying to you "
            "for 100 years. His breakthrough formula is BANNED in 14 countries — that's "
            "how you know it works! Only 57 bottles left. Comment 'YES' to claim yours!"
        ),
        "label": LABEL_FAKE,
        "category": "Health",
        "source_type": "social_post",
        "signals": (
            "Vague authority ('doctor'); conspiracy framing; 'banned = effective' "
            "fallacy; artificial scarcity; engagement-bait call to action"
        ),
        "notes": "Influencer-misinformation template.",
    },
    {
        "text": (
            "URGENT: The banks will freeze ALL savings accounts this Friday at midnight. "
            "An anonymous employee leaked the plan. Transfer everything to gold NOW. "
            "They will erase this message, so screenshot it immediately."
        ),
        "label": LABEL_FAKE,
        "category": "Finance",
        "source_type": "social_post",
        "signals": (
            "Deadline panic; anonymous leak; financial action demand; "
            "'message will be erased' framing"
        ),
        "notes": "Financial-panic template.",
    },
    {
        "text": "PROOF that the airport construction is a secret military bunker",
        "label": LABEL_FAKE,
        "category": "Politics",
        "source_type": "headline",
        "signals": "Assertion of 'proof' with none given; hidden-agenda framing",
        "notes": "Clickbait headline; no verifiable claim inside.",
    },
    {
        "text": (
            "They don't want you to know that a single vitamin makes the flu DISAPPEAR "
            "overnight. The pharmaceutical companies have paid to keep this QUIET. "
            "I tried it myself and I'm cured — that's all the proof anyone needs. "
            "Share before the censors delete it!"
        ),
        "label": LABEL_FAKE,
        "category": "Health",
        "source_type": "social_post",
        "signals": (
            "Anecdote presented as proof; suppression narrative; absolute medical "
            "claim; no trial, author or regulator cited"
        ),
        "notes": "Anecdote-as-proof template.",
    },
    {
        "text": (
            "Sports officials have been secretly fixing championships for decades, says a "
            "tipster nobody can identify. Every result you have ever watched is fake. "
            "The evidence was destroyed by the league, which proves it existed."
        ),
        "label": LABEL_FAKE,
        "category": "Sports",
        "source_type": "full_article",
        "signals": (
            "Unidentified tipster; sweeping unevidenced claim; destroyed-evidence "
            "circularity"
        ),
        "notes": "Conspiracy template applied to sport.",
    },
    # ------------------ Unverified / Insufficient Evidence ------------------
    {
        "text": (
            "A video circulating on social media appears to show flooding in a regional "
            "town centre. The clip has been shared more than 40,000 times, but the "
            "location and date cannot be confirmed from the footage, and it does not "
            "match official flood reports for the period. No source for the original "
            "upload has been identified."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Disaster",
        "source_type": "full_article",
        "signals": (
            "Unverified footage; unknown provenance; conflicts with official reports; "
            "original uploader unidentified"
        ),
        "notes": "Describes an unverified claim rather than asserting it.",
    },
    {
        "text": "Unconfirmed reports of an explosion near a northern industrial zone",
        "label": LABEL_UNVERIFIED,
        "category": "Disaster",
        "source_type": "headline",
        "signals": "Explicitly flagged as unconfirmed; no official statement yet",
        "notes": "Appropriately hedged headline.",
    },
    {
        "text": (
            "A widely shared post claims that a major grocery chain will close all its "
            "stores next month. The post does not name a source and no company statement "
            "or regulatory filing could be located. The chain has not responded to "
            "requests for comment."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Finance",
        "source_type": "full_article",
        "signals": (
            "No source named; no company statement or filing found; "
            "company has not responded"
        ),
        "notes": "Shows what 'insufficient evidence' looks like in practice.",
    },
    {
        "text": (
            "An account with a large following says a new disease outbreak has been "
            "detected in three cities. The account provides no laboratory reference, no "
            "official bulletin and no named authority. Public health agencies have not "
            "issued any alert matching the description."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Health",
        "source_type": "full_article",
        "signals": (
            "No laboratory or official reference; no named authority; "
            "no matching public alert"
        ),
        "notes": "Health claim with no verifiable anchor.",
    },
    {
        "text": "Screenshot claims a new tax will start next month; not yet confirmed",
        "label": LABEL_UNVERIFIED,
        "category": "Politics",
        "source_type": "social_post",
        "signals": "Screenshot without provenance; flagged as not yet confirmed",
        "notes": "Hedged claim; needs checking against the revenue authority.",
    },
    {
        "text": (
            "A photograph described as showing a rare astronomical event has been shared "
            "thousands of times. Reverse-image searches return several older, unrelated "
            "postings. The observatory that supposedly captured it has not published it, "
            "and its caption does not include a date or location."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Science",
        "source_type": "full_article",
        "signals": (
            "Image likely recycled; no date or location; supposed source has not "
            "published it"
        ),
        "notes": "Out-of-context media description.",
    },
    {
        "text": (
            "A post claims that a well-known athlete has signed with a new club. Neither "
            "club has announced a transfer, and no accredited reporter has confirmed it. "
            "The claim appears to originate from an anonymous fan account."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Sports",
        "source_type": "full_article",
        "signals": (
            "No official announcement from either club; anonymous fan account origin"
        ),
        "notes": "Transfer-rumour template.",
    },
    {
        "text": "Claims that a coastal highway will be permanently closed remain unverified",
        "label": LABEL_UNVERIFIED,
        "category": "Politics",
        "source_type": "headline",
        "signals": "Hedged; no official confirmation cited",
        "notes": "Neutral, appropriately cautious headline.",
    },
    {
        "text": (
            "An audio clip said to be a private conversation between two executives is "
            "spreading online. Audio analysts have not examined it, no transcript has been "
            "authenticated, and the companies involved have declined to comment on "
            "whether the recording is genuine."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Technology",
        "source_type": "full_article",
        "signals": (
            "Unverified audio; no forensic analysis; no authenticated transcript; "
            "no on-record response"
        ),
        "notes": "Media-authenticity uncertainty.",
    },
    {
        "text": (
            "Several posts say a new weather warning covers the whole country. The "
            "national weather service has issued a warning for two provinces only, and "
            "the posts do not link to the bulletin. The discrepancy has not been explained "
            "by the accounts sharing it."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Disaster",
        "source_type": "full_article",
        "signals": (
            "Viral version broadens an official warning; no link to the bulletin; "
            "internal inconsistency with the official scope"
        ),
        "notes": "Exaggerated-scope claim.",
    },
    {
        "text": "Viral chart about rent prices has no visible source or methodology",
        "label": LABEL_UNVERIFIED,
        "category": "Finance",
        "source_type": "social_post",
        "signals": "Chart without source or methodology; unverifiable as presented",
        "notes": "Data-without-provenance template.",
    },
    {
        "text": (
            "A rumour that a popular streaming series will be cancelled mid-season is "
            "spreading in fan communities. The platform has made no announcement, and the "
            "production company has not commented. The original post cites an unnamed "
            "'industry contact'."
        ),
        "label": LABEL_UNVERIFIED,
        "category": "Entertainment",
        "source_type": "full_article",
        "signals": (
            "No official announcement; unnamed 'industry contact'; "
            "rumour-only sourcing"
        ),
        "notes": "Entertainment-rumour template.",
    },
]

# ---------------------------------------------------------------------------
# 2. Generative pools — all fictional and deliberately generic
# ---------------------------------------------------------------------------

ORGS = [
    "the National Statistics Directorate",
    "the Global Economic Monitor",
    "the Federal Statistics Agency",
    "the Regional Health Authority",
    "the National Health Directorate",
    "the Coastal Weather Service",
    "the National Space Research Council",
    "the Public Transport Authority",
    "the Energy Market Regulator",
    "the Central Planning Office",
    "the National Audit Bureau",
    "the Water Safety Commission",
    "the National Rail Board",
    "the Environmental Standards Agency",
    "the Utilities Oversight Panel",
    "the National Sports Federation",
    "the Housing and Land Registry",
    "the Maritime Safety Inspectorate",
    "the Food Standards Directorate",
    "the Employment Policy Institute",
    "the Road and Bridge Agency",
    "the National Meteorological Office",
    "the Consumer Protection Bureau",
    "the Regional Development Council",
    "the Public Health Monitoring Unit",
    "the National Grid Balancing Centre",
    "the Fisheries and Coastal Authority",
    "the Building Safety Regulator",
    "the National Records Office",
    "the Agricultural Support Board",
]

# Sector organisations report "notice"-style news, not statistics.
# This mapping keeps the category column coherent.
ORG_CATEGORY = {
    "the National Statistics Directorate": "Finance",
    "the Global Economic Monitor": "Finance",
    "the Federal Statistics Agency": "Finance",
    "the Central Planning Office": "Finance",
    "the National Audit Bureau": "Finance",
    "the Employment Policy Institute": "Finance",
    "the Consumer Protection Bureau": "Finance",
    "the Regional Development Council": "Politics",
    "the Regional Health Authority": "Health",
    "the National Health Directorate": "Health",
    "the Public Health Monitoring Unit": "Health",
    "the Food Standards Directorate": "Health",
    "the Coastal Weather Service": "Disaster",
    "the National Meteorological Office": "Disaster",
    "the National Space Research Council": "Science",
    "the Public Transport Authority": "Technology",
    "the National Rail Board": "Technology",
    "the Road and Bridge Agency": "Technology",
    "the Building Safety Regulator": "Technology",
    "the Maritime Safety Inspectorate": "Technology",
    "the Energy Market Regulator": "Climate",
    "the National Grid Balancing Centre": "Climate",
    "the Water Safety Commission": "Climate",
    "the Environmental Standards Agency": "Climate",
    "the Utilities Oversight Panel": "Climate",
    "the Fisheries and Coastal Authority": "Climate",
    "the National Sports Federation": "Sports",
    "the Housing and Land Registry": "Finance",
    "the Agricultural Support Board": "Finance",
    "the National Records Office": "Politics",
}

# Pools for the "official notice / advisory" family of realistic rows.
NOTICE_EVENTS = [
    "expected heavy rain",
    "a forecast cold snap",
    "seasonal high tides",
    "strong coastal winds",
    "a heatwave expected later in the week",
    "the first frost of the season",
]

NOTICE_WORKS = [
    "a scheduled maintenance window",
    "a planned safety inspection",
    "routine track replacement",
    "an upgrade to the signalling system",
    "a full safety audit",
    "essential repairs to a pumping station",
]

NOTICE_EFFECTS = [
    "take effect from Monday",
    "begin next week",
    "last approximately four hours",
    "affect two routes only",
    "apply to the northern half of the network",
    "be phased in over two weekends",
]

# Only weather and coastal bodies issue weather advisories.
WEATHER_ORGS = [
    "the Coastal Weather Service",
    "the National Meteorological Office",
    "the Fisheries and Coastal Authority",
    "the Water Safety Commission",
]

LOCATIONS = [
    "the Northern Province",
    "the capital district",
    "the eastern estuary",
    "the coastal towns",
    "the central highlands",
    "the western valley",
    "the southern districts",
    "the port area",
    "the industrial belt",
    "the border region",
    "the lake basin",
    "the metropolitan area",
]

ROLES = [
    "a spokesperson",
    "the chief economist",
    "the director of operations",
    "a senior researcher",
    "the regional coordinator",
    "the head of communications",
    "the chief medical adviser",
    "the lead analyst",
    "the deputy commissioner",
    "the head of data",
]

# Organisations that plausibly publish economic and social statistics.
# Used with INDICATORS so that "who reports what" always makes sense.
STAT_ORGS = [
    "the National Statistics Directorate",
    "the Global Economic Monitor",
    "the Federal Statistics Agency",
    "the National Audit Bureau",
    "the Central Planning Office",
    "the Employment Policy Institute",
    "the Regional Development Council",
    "the Consumer Protection Bureau",
]

STAT_ROLES = [
    "the chief economist",
    "the lead analyst",
    "the head of data",
    "the director of operations",
    "a spokesperson",
    "the head of communications",
]

INDICATORS = [
    "consumer prices",
    "unemployment",
    "quarterly output",
    "new home registrations",
    "industrial production",
    "retail sales",
    "average weekly earnings",
    "electricity demand",
    "hospital admissions",
    "public transport ridership",
    "export volumes",
    "construction starts",
    "rental vacancy rates",
    "rail freight volumes",
    "water reservoir levels",
    "small-business lending",
]

MOVEMENTS = [
    "rose",
    "fell",
    "increased",
    "declined",
    "was broadly unchanged",
    "climbed",
    "dropped",
    "edged higher",
    "eased",
    "recovered",
]

PERIODS = [
    "the second quarter",
    "September",
    "the first half of the year",
    "the previous month",
    "the last fiscal year",
    "the twelve months to June",
    "the third quarter",
    "the first quarter",
    "the most recent reporting period",
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

REASONS = [
    "lower energy costs",
    "weaker demand from overseas markets",
    "seasonal effects",
    "a one-off change in the reporting calendar",
    "broadly stable prices across most categories",
    "reduced maintenance downtime",
    "cooler-than-average weather",
    "a temporary correction after an unusual quarter",
    "higher borrowing costs",
    "delayed infrastructure works",
    "an unusually mild start to the season",
    "the ending of a temporary support scheme",
]

DAYS_LATER = [
    "within five working days",
    "later this month",
    "at the next scheduled briefing",
    "by the end of the quarter",
    "in the following release",
]

FAKE_TARGETS = [
    "the government",
    "the health ministry",
    "the central bank",
    "the national broadcaster",
    "the food regulator",
    "the school board",
    "the energy authority",
    "the water utility",
    "the airport operator",
    "the pension agency",
    "the transport ministry",
    "the election commission",
    "the national library",
    "the housing department",
    "the tax office",
    "the weather service",
]

FAKE_SECRETS = [
    "putting mind-control chemicals in the water supply",
    "replacing all banknotes with trackable versions",
    "hiding a permanent ban on private car ownership",
    "paying journalists to bury the truth",
    "planning to outlaw cash by the end of the month",
    "placing silent tracking chips in supermarket food",
    "running a covert programme to control the weather",
    "draining the reservoirs on purpose",
    "selling public land to unnamed buyers",
    "switching the water supply to an unlabelled source",
    "rewriting school textbooks overnight",
    "stockpiling food for officials only",
    "installing listening devices in buses",
    "deleting land records to seize private property",
    "replacing hospital staff with untrained volunteers",
]

FAKE_CURES = [
    "a single household spice",
    "a root grown only in one remote valley",
    "a 10-minute breathing exercise",
    "a banned herbal tea",
    "a magnetic wristband",
    "a moon-phase diet",
    "a cold-water shock routine",
    "a secret blend of three seeds",
    "a blue LED lamp",
    "a special type of salt",
    "two minutes of humming",
    "a copper bracelet",
]

FAKE_CLAIMS = [
    "that all swimming pools will be closed permanently from Friday",
    "that every school will switch to a four-day week next term",
    "that the national grid will be shut down for three days",
    "that a new law will confiscate unused savings",
    "that aeroplanes will be grounded for a whole month",
    "that the city will ban all private vehicles",
    "that drinking water will be rationed to two litres a day",
    "that every library will be closed for a year",
    "that all fuel stations will close at weekends",
    "that a national curfew will begin without notice",
    "that all mobile networks will be switched off for a week",
    "that property taxes will be tripled next month",
    "that hospitals will stop treating non-residents",
    "that the currency will be replaced overnight",
    "that all parks will be sold to private developers",
]

FAKE_HOOKS = [
    "You will not believe what {target} is hiding in {loc}.",
    "People in {loc} are furious after a 'leaked memo' about {target}.",
    "A message spreading through {loc} claims {target} has been {secret}.",
    "Nobody in {loc} is talking about this, and that is the real scandal.",
    "An insider in {loc} says the whole thing was decided years ago.",
]

UNVERIFIED_SUBJECTS = [
    "A widely shared post",
    "An account with a large following",
    "A video circulating online",
    "A screenshot posted to a community forum",
    "An audio clip shared in a group chat",
    "A photograph described as recent",
    "A forwarded message",
    "A viral chart",
    "A short clip reposted across several platforms",
    "A comment thread under a news page",
    "A newsletter forwarded by email",
    "A post in a neighbourhood group",
]

UNVERIFIED_CLAIMS = [
    "claims that a major employer will close its largest site next month",
    "says a new restriction will take effect with no notice",
    "claims that a well-known figure has been hospitalised",
    "suggests that tap water in three districts is unsafe to drink",
    "says a bridge on the main route has been declared unsafe and closed",
    "claims that a scheduled sporting event has been cancelled",
    "reports that a large sum of public money has been misallocated",
    "claims that a popular product has been recalled nationwide",
    "says that bus fares will double from the start of the month",
    "claims that a hospital unit will be closed to save money",
    "says that a local factory has been sold to an unnamed buyer",
    "claims that a tax on second homes starts immediately",
    "reports that a reservoir has been declared unsafe",
    "says that all trains to the coast have been suspended",
    "claims that a supermarket chain will stop accepting cash",
    "suggests that a vaccine programme has been paused",
]

UNVERIFIED_ABSENCES = [
    "does not name a source, document or authority",
    "provides no link to an official statement or notice",
    "cites no named official, filing or public record",
    "includes no date, location or verifiable reference",
    "contains no original document, photograph metadata or recording",
    "gives no contactable author or organisation behind it",
    "offers no methodology for the figures it shows",
]

UNVERIFIED_CLOSERS = [
    "No independent outlet has confirmed the claim, and the original author could not be reached for comment.",
    "The relevant authority has not issued any notice matching the description.",
    "No company statement or regulatory filing matching the claim could be located.",
    "The claim remains unverified and should not be treated as established.",
    "Requests for comment sent to the accounts sharing it were not answered.",
    "Until a primary source is produced, the claim cannot be assessed.",
]

REAL_SIGNALS_CLEAN = ""
REAL_SIGNALS_MILD = "Attributed to a named organisation; figures presented with scope and timing"

FAKE_SIGNALS = [
    "Sensationalised wording in capital letters",
    "Urgency and share-before-deleted framing",
    "Claim of a deliberate media or industry cover-up",
    "No verifiable evidence, study or official record provided",
    "Emotional manipulation and absolute language",
    "Unnamed or unidentifiable source described as an insider",
    "Conspiracy reasoning that treats hiding as proof",
    "Artificial scarcity and countdown pressure",
    "Circular reasoning presented as confirmation",
    "Broad, sweeping claim with no scope or limitation",
]

UNVERIFIED_SIGNALS = [
    "No named source, document or authority referenced",
    "Claim has not been independently confirmed",
    "Viral sharing without corroboration",
    "Original author or uploader could not be identified",
    "Possible misattributed or recycled media",
    "Official statements do not match the claim",
    "Figures presented without methodology",
]


INDICATOR_CATEGORY = {
    "consumer prices": "Finance",
    "unemployment": "Finance",
    "quarterly output": "Finance",
    "new home registrations": "Finance",
    "industrial production": "Finance",
    "retail sales": "Finance",
    "average weekly earnings": "Finance",
    "electricity demand": "Climate",
    "hospital admissions": "Health",
    "public transport ridership": "Technology",
    "export volumes": "Finance",
    "construction starts": "Finance",
    "rental vacancy rates": "Finance",
    "rail freight volumes": "Technology",
    "water reservoir levels": "Climate",
    "small-business lending": "Finance",
}

NON_DIRECTIONAL_MOVEMENT = "was broadly unchanged"


def pick(rng, pool):
    return rng.choice(pool)


def pct(rng, low=0.1, high=9.9):
    """A plausible one-decimal percentage that is clearly illustrative."""
    return round(rng.uniform(low, high), 1)


def infer_category(text, fallback):
    """Give real-style rows a category that matches what they are about."""
    lowered = text.lower()
    for org, org_category in ORG_CATEGORY.items():
        if org.lower() in lowered:
            return org_category
    for indicator, indicator_category in INDICATOR_CATEGORY.items():
        if indicator in lowered:
            return indicator_category
    return fallback


# ---------------------------------------------------------------------------
# 3. Template builders — one per (label, source_type)
# ---------------------------------------------------------------------------


def build_real(rng, category, source_type):
    """Dispatch between two realistic families: statistics and public notices."""
    if rng.random() < 0.5:
        return _build_real_statistics(rng, source_type)
    return _build_real_notice(rng, source_type)


def _build_real_statistics(rng, source_type):
    org = pick(rng, STAT_ORGS)
    org_cap = org[0].upper() + org[1:]
    role = pick(rng, STAT_ROLES)
    indicator = pick(rng, INDICATORS)
    movement = pick(rng, MOVEMENTS)
    period = pick(rng, PERIODS)
    day = pick(rng, DAYS)
    reason = pick(rng, REASONS)
    later = pick(rng, DAYS_LATER)
    value = pct(rng)

    if source_type == "headline":
        if movement == NON_DIRECTIONAL_MOVEMENT:
            return "%s: %s was broadly unchanged in %s" % (org_cap, indicator, period)
        return "%s: %s %s %s%% in %s" % (org_cap, indicator, movement, value, period)

    if source_type == "social_post":
        if movement == NON_DIRECTIONAL_MOVEMENT:
            return (
                "New figures from %s today: %s was broadly unchanged in %s. "
                "The full release, including methodology, is on their public site."
                % (org, indicator, period)
            )
        return (
            "New figures from %s today: %s %s by %s%% in %s. "
            "The full release, including methodology, is on their public site."
            % (org, indicator, movement, value, period)
        )

    if movement == NON_DIRECTIONAL_MOVEMENT:
        return (
            "%s said that, in %s, %s was broadly unchanged compared with the same "
            "period a year earlier. In a briefing on %s, %s said the figures "
            "reflected %s. The release included the underlying tables and a "
            "description of how the figures were compiled. A revised estimate is "
            "expected %s."
            % (org_cap, period, indicator, day, role, reason, later)
        )

    return (
        "%s said that, in %s, %s %s by %s percent compared with the same period a "
        "year earlier. In a briefing on %s, %s said the change reflected %s. The "
        "release included the underlying tables and a description of how the "
        "figures were compiled. A revised estimate is expected %s."
        % (org_cap, period, indicator, movement, value, day, role, reason, later)
    )


def _build_real_notice(rng, source_type):
    org = pick(rng, ORGS)
    org_cap = org[0].upper() + org[1:]
    loc = pick(rng, LOCATIONS)
    role = pick(rng, ROLES)
    day = pick(rng, DAYS)
    later = pick(rng, DAYS_LATER)
    event = pick(rng, NOTICE_EVENTS)
    works = pick(rng, NOTICE_WORKS)
    effect = pick(rng, NOTICE_EFFECTS)

    if org in WEATHER_ORGS:
        if source_type == "headline":
            return "%s issues advisory for %s ahead of %s" % (org_cap, loc, event)
        if source_type == "social_post":
            return (
                "%s has issued an advisory for %s ahead of %s. Residents can read "
                "the full notice and safety guidance on the official site."
                % (org_cap, loc, event)
            )
        return (
            "%s issued an advisory on %s for %s ahead of %s. The notice sets out "
            "recommended precautions and will remain in force until conditions "
            "change. %s said the situation would be reassessed %s and that updates "
            "would be published on the official channels."
            % (org_cap, day, loc, event, role.capitalize(), later)
        )

    if source_type == "headline":
        return "%s announces %s affecting %s" % (org_cap, works, loc)
    if source_type == "social_post":
        return (
            "%s has published details of %s affecting %s. Timetables and "
            "alternative arrangements are listed in the official notice."
            % (org_cap, works, loc)
        )
    return (
        "%s announced on %s that %s will affect %s. The works are expected to %s. "
        "%s said the full programme, including maps and timetables, had been posted "
        "in advance and would be updated %s."
        % (org_cap, day, works, loc, effect, role.capitalize(), later)
    )


def build_fake(rng, category, source_type):
    target = pick(rng, FAKE_TARGETS)
    target_cap = target[0].upper() + target[1:]
    secret = pick(rng, FAKE_SECRETS)
    cure = pick(rng, FAKE_CURES)
    claim = pick(rng, FAKE_CLAIMS)
    loc = pick(rng, LOCATIONS)

    if source_type == "headline":
        return "EXPOSED: %s has been secretly %s for years — and nobody is allowed to say it" % (
            target_cap,
            secret,
        )

    if source_type == "social_post":
        form = rng.randint(0, 3)
        if form == 0:
            return (
                "SHOCKING!!! %s has been %s for YEARS and the mainstream media "
                "REFUSES to report it! An insider who cannot be named confirms "
                "EVERYTHING. Share this before it gets DELETED!"
                % (target_cap, secret)
            )
        if form == 1:
            return (
                "They don't want you to know that %s CURES almost everything — and "
                "they are spending BILLIONS to keep it quiet! Doctors are FURIOUS. "
                "Only a few left, claim yours in the next 10 minutes!"
                % cure
            )
        if form == 2:
            return (
                "BREAKING: A leaked document proves %s. Officials refuse to comment, "
                "which everyone knows means it is true. Forward this to everyone you "
                "know before it disappears!"
                % claim
            )
        return (
            "URGENT: A leaked plan says %s. An anonymous employee revealed it and "
            "the newsrooms are silent. Take action NOW — they will delete this "
            "within hours!"
            % claim
        )

    hook = pick(rng, FAKE_HOOKS).format(target=target, loc=loc, secret=secret)
    return (
        "%s Several accounts say the plan has been in place for years and that every "
        "newsroom has agreed to stay silent about it. Supporters of the story claim the "
        "evidence was destroyed, which they say proves it existed. No document, court "
        "filing or named official has been produced. The message ends by urging readers "
        "to share it everywhere before the 'censors' remove it."
        % hook
    )


def build_unverified(rng, category, source_type):
    subject = pick(rng, UNVERIFIED_SUBJECTS)
    subject_cap = subject[0].upper() + subject[1:]
    claim = pick(rng, UNVERIFIED_CLAIMS)
    absence = pick(rng, UNVERIFIED_ABSENCES)
    closer = pick(rng, UNVERIFIED_CLOSERS)

    if source_type == "headline":
        return "%s: %s — not yet confirmed by any official source" % (
            subject_cap,
            claim[0].upper() + claim[1:],
        )

    if source_type == "social_post":
        return (
            "%s %s. It %s, and it has been shared thousands of times. Treat it "
            "with caution until an official source confirms it."
            % (subject_cap, claim, absence)
        )

    return "%s %s. The item %s. It has been shared widely. %s" % (
        subject_cap,
        claim,
        absence,
        closer,
    )


BUILDERS = {
    LABEL_REAL: build_real,
    LABEL_FAKE: build_fake,
    LABEL_UNVERIFIED: build_unverified,
}


# ---------------------------------------------------------------------------
# 4. Assembly
# ---------------------------------------------------------------------------


def generate_rows(target_rows):
    """Return (rows, columns). Curated rows first, then generated rows."""
    rows = []
    seen_text = set()

    # 4a. Curated rows
    for seed in CURATED:
        key = seed["text"].strip().lower()
        if key in seen_text:
            continue
        seen_text.add(key)
        rows.append(
            {
                "text": seed["text"],
                "label": seed["label"],
                "category": seed["category"],
                "source_type": seed["source_type"],
                "signals": seed["signals"],
                "origin": "curated",
                "notes": seed["notes"],
            }
        )

    # 4b. Generated rows — always extend the currently smallest label so the
    #     three classes stay balanced even when a template family runs dry.
    rng = random.Random(SEED)
    labels = [LABEL_REAL, LABEL_FAKE, LABEL_UNVERIFIED]
    counts = {label: 0 for label in labels}
    for row in rows:
        counts[row["label"]] += 1

    attempts = 0
    max_attempts = max(target_rows, 1) * 400
    while len(rows) < target_rows and attempts < max_attempts:
        attempts += 1
        label = min(labels, key=lambda name: counts[name])
        category = pick(rng, CATEGORIES)
        source_type = pick(rng, SOURCE_TYPES)

        text = BUILDERS[label](rng, category, source_type).strip()
        key = text.lower()
        if key in seen_text:
            continue
        seen_text.add(key)
        counts[label] += 1

        if label == LABEL_REAL:
            category = infer_category(text, category)

        if label == LABEL_REAL:
            signals = REAL_SIGNALS_CLEAN if rng.random() < 0.85 else REAL_SIGNALS_MILD
            notes = "Attributed reporting with scope, timing and a named source."
        elif label == LABEL_FAKE:
            signals = "; ".join(rng.sample(FAKE_SIGNALS, rng.randint(2, 4)))
            notes = "Multiple sensationalism / manipulation signals present."
        else:
            signals = "; ".join(rng.sample(UNVERIFIED_SIGNALS, rng.randint(2, 3)))
            notes = "Insufficient verifiable evidence to classify the claim."

        rows.append(
            {
                "text": text,
                "label": label,
                "category": category,
                "source_type": source_type,
                "signals": signals,
                "origin": "generated",
                "notes": notes,
            }
        )

    # 4c. Shuffle so labels/categories are interleaved, then assign ids
    rng.shuffle(rows)
    for index, row in enumerate(rows, start=1):
        row["id"] = "TL-%04d" % index
        row["is_synthetic"] = "true"
        row["dataset_note"] = SYNTHETIC_NOTE

    columns = [
        "id",
        "text",
        "label",
        "category",
        "source_type",
        "signals",
        "origin",
        "is_synthetic",
        "dataset_note",
        "notes",
    ]
    return rows, columns


def write_outputs(rows, columns):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in columns})

    with open(JSON_PATH, "w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def summarise(rows):
    groups = {
        "label": {},
        "category": {},
        "source_type": {},
        "origin": {},
    }
    keys = {
        "label": "label",
        "category": "category",
        "source_type": "source_type",
        "origin": "origin",
    }
    for row in rows:
        for name, field in keys.items():
            groups[name][row[field]] = groups[name].get(row[field], 0) + 1

    unique_texts = len(set(row["text"] for row in rows))

    print("Generated %d rows (%d unique texts)" % (len(rows), unique_texts))
    for name in ["label", "source_type", "origin", "category"]:
        print("\nBy %s:" % name)
        for key in sorted(groups[name]):
            print("  %-38s %d" % (key, groups[name][key]))
    print("\nWrote:")
    print("  %s" % CSV_PATH)
    print("  %s" % JSON_PATH)


def main():
    parser = argparse.ArgumentParser(description="Generate the TruthLens AI demo dataset.")
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help="target number of rows (default: %d)" % DEFAULT_ROWS,
    )
    args = parser.parse_args()

    rows, columns = generate_rows(max(args.rows, len(CURATED)))
    write_outputs(rows, columns)
    summarise(rows)


if __name__ == "__main__":
    main()
