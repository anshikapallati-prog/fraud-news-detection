# TruthLens AI — External (Real-World) Data

This folder holds **real, published benchmark data** used to *evaluate* the
project — kept strictly separate from the synthetic demo set in `data/`.

| File | Description |
|------|-------------|
| `fetch_liar.py` | Downloader + normalizer (stdlib only, no `pip install`) |
| `liar_truthlens.csv` | **12,763 real PolitiFact statements** in TruthLens schema |
| `evaluate_offline.py` | Agreement benchmark for the offline heuristic |
| `.cache_liar.zip` | Raw download cache (reused on reruns; git-ignored) |

---

## The dataset: LIAR (Wang, EMNLP 2017)

- **What**: 12,763 short political statements fact-checked by PolitiFact,
  with speaker, context, and a 6-way ruling.
- **Source**: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip
- **License**: free for research use. If you publish results, cite:
  *William Yang Wang. "Liar, Liar Pants on Fire: A New Benchmark Dataset for
  Fake News Detection." ACL (EMNLP). 2017.*
- **Our mapping** (documented choice, not gospel):

  | PolitiFact ruling | TruthLens label |
  |---|---|
  | true, mostly-true | Likely Real |
  | half-true, barely-true | Unverified / Insufficient Evidence |
  | false, pants-fire | Likely Fake |

  The middle mapping is deliberate: a half-true claim is precisely one a
  responsible tool should refuse to certify.

- **Columns**: the TruthLens schema (`id, text, label, category, source_type,
  signals, origin, is_synthetic, dataset_note, notes`) **plus**
  `original_label` and `speaker` for traceability. `is_synthetic` is `"false"`
  and every row carries an `EXTERNAL DATA` provenance note.

Balance: 4,502 Likely Real / 3,538 Likely Fake / 4,723 Unverified.

---

## ⚠️ Ethics — read before using real data

The synthetic set is safe to quote; **this one is not**:

1. These are **real statements by real people**. A model output on them is
   pattern analysis, never a verdict about a person. Do not republish rows
   as "TruthLens says X lied".
2. Labels are **PolitiFact's rulings**, frozen in time. Rulings, context, and
   consensus can change; treat labels as one newsroom's judgment.
3. The set skews U.S.-political and English-only. Any metric you quote
   describes *that slice*, not "news" in general.
4. For your report, discuss the label mapping above as a *methodological
   choice* — examiners love that.

---

## Reproduce / extend

```powershell
cd ".\data\external"

# Re-fetch (uses .cache_liar.zip if present; delete it to force re-download)
python fetch_liar.py
python fetch_liar.py --limit 2000 --out liar_sample.csv   # small slice

# Evaluate the offline heuristic (run with the backend venv):
cd ..\..\backend
.\venv\Scripts\python.exe ..\data\external\evaluate_offline.py --n 600
.\venv\Scripts\python.exe ..\data\external\evaluate_offline.py --csv ..\data\truthlens_news_dataset.csv --n 300
```

No third-party packages needed — both scripts are standard library only.

### Adding another dataset

1. Write `fetch_<name>.py` that outputs the TruthLens columns
   (`id, text, label, category, source_type, signals, origin="external-<name>",
   is_synthetic="false", dataset_note, notes`).
2. Keep the three label strings **exactly** as in `backend/schemas.py`.
3. Document source, license, and your label mapping here.
4. Run it through `evaluate_offline.py --csv <file>`.

Good next candidates: ISOT Fake News (~44k full articles), WELFake (~72k),
FakeNewsNet (needs social-context crawling — heavier).

---

## Benchmark results (locked, seed=7)

| Dataset | Rows tested | Agreement | Real recall | Fake recall | Unverif. recall |
|---|---|---|---|---|---|
| Synthetic (`truthlens_news_dataset.csv`) | 300 | **57.7%** | 37% | 36% | 100% |
| LIAR (real claims) | 600 | **33.3%** | 7.5% | 3.5% | 89% |

**How to read this (put this paragraph in your report):**

> A style heuristic and a fact-checker are different instruments. On
> template-written text it agrees with the intended labels about half the
> time; on real one-sentence political claims it falls back to
> "Unverified" almost always (89%) — which is the *correct conservative
> behavior* for a bare claim with no checkable anchor. When it does cry
> "Fake", it is right roughly half the time, and only on blatant style
> abuse (caps, urgency pressure, unnamed sources). The gap between 57.7%
> and 33.3% is the generalization gap, and it is exactly why TruthLens
> pairs every verdict with verification steps instead of presenting scores
> as truth.

Do **not** tune the heuristic's word lists against these numbers and re-report
— that would be overfitting to the test set. The rules are frozen as
general style signals; the numbers above are the honest result.
