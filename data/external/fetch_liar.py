#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TruthLens AI — External dataset fetcher (LIAR)
===============================================

Downloads the public LIAR benchmark (Wang, EMNLP 2017: ~12.8k short
PolitiFact statements with 6-way truth labels) and normalizes it into the
TruthLens schema so it can be evaluated and demonstrated like the synthetic
dataset.

Source : https://www.cs.ucsb.edu/~william/data/liar_dataset.zip
License: free for research use. If you publish results, cite:
         William Yang Wang. "Liar, Liar Pants on Fire" (EMNLP 2017).

Label mapping (documented, debatable — see data/external/README.md):
    true / mostly-true          -> Likely Real
    half-true / barely-true     -> Unverified / Insufficient Evidence
    false / pants-fire          -> Likely Fake

IMPORTANT: these are REAL statements about REAL people, with PolitiFact's
rulings as labels. Do not republish rows as TruthLens judgments, and do not
present model outputs on them as verdicts about any person.

Usage (stdlib only — no pip install needed):
    python fetch_liar.py                  # writes liar_truthlens.csv
    python fetch_liar.py --out custom.csv --limit 2000
"""

from __future__ import annotations

import argparse
import csv
import os
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "liar_truthlens.csv")

LIAR_URL = "https://www.cs.ucsb.edu/~william/data/liar_dataset.zip"
LIAR_FILES = ["train.tsv", "valid.tsv", "test.tsv"]

LABEL_MAP = {
    "true": "Likely Real",
    "mostly-true": "Likely Real",
    "half-true": "Unverified / Insufficient Evidence",
    "barely-true": "Unverified / Insufficient Evidence",
    "false": "Likely Fake",
    "pants-fire": "Likely Fake",
}

DATASET_NOTE = (
    "EXTERNAL DATA — real PolitiFact statements from LIAR (Wang 2017). "
    "Labels are PolitiFact rulings, not TruthLens judgments."
)


def download(url: str, dest: str) -> None:
    print("Downloading %s ..." % url)
    req = urllib.request.Request(url, headers={"User-Agent": "TruthLensAI-college-project/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response, open(dest, "wb") as handle:
        total = 0
        while True:
            chunk = response.read(256 * 1024)
            if not chunk:
                break
            handle.write(chunk)
            total += len(chunk)
    print("Saved %.1f MB to %s" % (total / 1e6, dest))


def parse_liar(zip_path: str) -> list[dict]:
    """Extract the three TSVs and return normalized row dicts (deduped)."""
    rows: list[dict] = []
    seen_texts = set()
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        for wanted in LIAR_FILES:
            member = next((n for n in names if n.endswith(wanted)), None)
            if member is None:
                print("WARNING: %s not found in archive, skipped" % wanted)
                continue
            with archive.open(member) as handle:
                reader = csv.reader(
                    (line.decode("utf-8", errors="replace") for line in handle),
                    delimiter="\t",
                )
                for cols in reader:
                    if len(cols) < 14:
                        continue
                    original = cols[1].strip().lower()
                    statement = cols[2].strip()
                    if not statement or original not in LABEL_MAP:
                        continue
                    key = statement.lower()
                    if key in seen_texts:
                        continue
                    seen_texts.add(key)
                    subject = (cols[3].split(",")[0].strip() or "Politics").title()
                    rows.append(
                        {
                            "text": statement,
                            "label": LABEL_MAP[original],
                            "category": subject[:40],
                            "source_type": "headline",
                            "signals": "",
                            "origin": "external-liar",
                            "is_synthetic": "false",
                            "dataset_note": DATASET_NOTE,
                            "notes": "PolitiFact ruling: %s; speaker: %s; context: %s"
                            % (original, cols[4].strip() or "unknown", cols[13].strip() or "unknown"),
                            "original_label": original,
                            "speaker": cols[4].strip(),
                        }
                    )
    return rows


def write_csv(rows: list[dict], path: str) -> None:
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
        "original_label",
        "speaker",
    ]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for index, row in enumerate(rows, start=1):
            record = dict(row)
            record["id"] = "LIAR-%05d" % index
            writer.writerow({key: record.get(key, "") for key in columns})


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch + normalize the LIAR dataset.")
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, default=0, help="cap rows (0 = all)")
    parser.add_argument("--zip", default=os.path.join(HERE, ".cache_liar.zip"),
                        help="reuse/refresh the downloaded archive")
    args = parser.parse_args()

    if not os.path.exists(args.zip):
        download(LIAR_URL, args.zip)
    else:
        print("Reusing cached archive: %s" % args.zip)

    rows = parse_liar(args.zip)
    print("Parsed %d unique statements" % len(rows))
    if args.limit and len(rows) > args.limit:
        # Deterministic stride sample so reruns are identical.
        step = len(rows) / args.limit
        rows = [rows[int(i * step)] for i in range(args.limit)]
        print("Sampled down to %d rows" % len(rows))

    write_csv(rows, args.out)

    balance: dict[str, int] = {}
    for row in rows:
        balance[row["label"]] = balance.get(row["label"], 0) + 1
    print("Wrote: %s" % args.out)
    for label in sorted(balance):
        print("  %-38s %d" % (label, balance[label]))


if __name__ == "__main__":
    main()
