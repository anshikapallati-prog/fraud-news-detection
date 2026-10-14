#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TruthLens AI — Offline-analyzer evaluation script
==================================================

Measures how often the deterministic offline heuristic AGREES with the
human (PolitiFact) labels in an external dataset. This is an *agreement*
study, not an accuracy claim about truth detection: a heuristic that spots
sensational wording is a different instrument from a fact-checker, and the
gap between them is itself a report-worthy finding.

Usage (run with the backend venv so `offline_analysis` imports work):
    cd backend
    .\\venv\\Scripts\\python.exe ..\\data\\external\\evaluate_offline.py
    .\\venv\\Scripts\\python.exe ..\\data\\external\\evaluate_offline.py --csv ..\\data\\truthlens_news_dataset.csv --n 300

Options:
    --csv   dataset CSV in TruthLens schema (default: external LIAR file)
    --n     total rows to evaluate, stratified across labels (default: 600)
    --seed  sampling seed for reproducibility (default: 7)
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "backend"))
DEFAULT_CSV = os.path.join(HERE, "liar_truthlens.csv")

sys.path.insert(0, BACKEND_DIR)

from offline_analysis import analyze_offline  # noqa: E402

LABELS = [
    "Likely Real",
    "Likely Fake",
    "Unverified / Insufficient Evidence",
]


def load_rows(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("text")]


def stratified_sample(rows: list[dict], n: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    by_label: dict[str, list[dict]] = {label: [] for label in LABELS}
    for row in rows:
        if row.get("label") in by_label:
            by_label[row["label"]].append(row)
    per_class = max(n // len(LABELS), 1)
    sample: list[dict] = []
    for label in LABELS:
        pool = by_label[label][:]
        rng.shuffle(pool)
        sample.extend(pool[:per_class])
    rng.shuffle(sample)
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the offline heuristic.")
    parser.add_argument("--csv", default=DEFAULT_CSV)
    parser.add_argument("--n", type=int, default=600)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    rows = load_rows(args.csv)
    print("Loaded %d rows from %s" % (len(rows), args.csv))
    sample = stratified_sample(rows, args.n, args.seed)
    print("Evaluating %d rows (stratified, seed=%d) ..." % (len(sample), args.seed))

    confusion: dict[str, dict[str, int]] = {
        gold: {pred: 0 for pred in LABELS} for gold in LABELS
    }
    for row in sample:
        predicted = analyze_offline(row["text"]).classification
        confusion[row["label"]][predicted] += 1

    total = sum(sum(line.values()) for line in confusion.values())
    correct = sum(confusion[label][label] for label in LABELS)

    print("\nConfusion matrix (rows = dataset label, columns = heuristic call):")
    header = "%-34s %12s %12s %12s" % ("", "Real", "Fake", "Unverif.")
    print(header)
    short = {"Likely Real": "Real", "Likely Fake": "Fake",
             "Unverified / Insufficient Evidence": "Unverif."}
    for gold in LABELS:
        print(
            "%-34s %12d %12d %12d"
            % (short[gold], confusion[gold]["Likely Real"],
               confusion[gold]["Likely Fake"],
               confusion[gold]["Unverified / Insufficient Evidence"])
        )

    print("\nAgreement with dataset labels: %d/%d = %.1f%%"
          % (correct, total, 100.0 * correct / total))
    for label in LABELS:
        row_total = sum(confusion[label].values())
        if row_total:
            print("  Recall on %-28s %.1f%% (%d/%d)"
                  % (short[label], 100.0 * confusion[label][label] / row_total,
                     confusion[label][label], row_total))

    print(
        "\nRead this honestly: a heuristic spots *style*; PolitiFact judges "
        "*facts*. Agreement far below 100% is expected — that gap is why the "
        "app routes every important claim to independent verification."
    )


if __name__ == "__main__":
    main()
