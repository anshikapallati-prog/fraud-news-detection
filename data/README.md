# TruthLens AI — Demo News Dataset

A 500-row, three-class news-text dataset used to demonstrate, test, and explain the
TruthLens AI classifier.

| File | Description |
|------|-------------|
| `truthlens_news_dataset.csv` | 500 rows, UTF-8, comma-separated (spreadsheet/`pandas` friendly) |
| `truthlens_news_dataset.json` | The same 500 rows as a JSON array (API/web friendly) |
| `generate_dataset.py` | Deterministic generator that rebuilds both files (stdlib only, Python 3.7+) |

---

## ⚠️ Read this first — the data is synthetic

**None of this is real news, and no statement in it is true.**

* Every organisation, agency, place, official and statistic is **fictional**.
* The `label` column records the **characteristic pattern** of the text
  (attributed, measured reporting vs. sensational virality vs. an unverifiable
  circulating claim). It is **not** a fact-check verdict and **not** ground truth
  about anything real.
* Do **not** train a production fact-checking model on it, do **not** benchmark
  accuracy against it as if it were real-world data, and do **not** cite it as
  evidence about any real person or organisation.

It exists so that you can:

1. Demonstrate the app with representative inputs and expected categories.
2. Show a confusion matrix / class-balance chart in a presentation.
3. Prototype an offline baseline classifier without needing an API key.
4. Discuss dataset design, labels, and ethics in a report.

Every row carries `is_synthetic = true` and
`dataset_note = "SYNTHETIC DEMO DATA — fictional entities, not real news"`,
so the provenance travels with the data.

---

## Schema

| Column | Type | Meaning |
|--------|------|---------|
| `id` | string | Row identifier, `TL-0001` … `TL-0500` |
| `text` | string | The headline / social post / article body to classify |
| `label` | string | `Likely Real`, `Likely Fake`, or `Unverified / Insufficient Evidence` |
| `category` | string | Topical area: Politics, Health, Science, Technology, Finance, Climate, Sports, Entertainment, Crime, Disaster |
| `source_type` | string | `headline`, `social_post`, or `full_article` |
| `signals` | string | Semicolon-separated warning signals (empty for clean rows) |
| `origin` | string | `curated` (hand-written) or `generated` (template expansion) |
| `is_synthetic` | string | Always `true` |
| `dataset_note` | string | Fixed provenance warning |
| `notes` | string | Short annotation explaining why the row has its label |

The `label`, `text`, and `category` columns share their names and values with the
backend's Pydantic schema (`backend/schemas.py`), so rows can be posted straight to
`POST /api/analyze` without transformation.

---

## Class balance

| Label | Rows |
|-------|------|
| Likely Real | 167 |
| Likely Fake | 167 |
| Unverified / Insufficient Evidence | 166 |
| **Total** | **500** |

Source types: ~170 `full_article`, ~165 `headline`, ~165 `social_post`.
All 500 texts are unique.

---

## Regenerating the files

The generator is deterministic (`SEED = 20260101`), so you will get byte-identical
output unless you change the seed, the pools, or the row count.

```powershell
cd ".\data"
python generate_dataset.py              # rebuild 500 rows (CSV + JSON)
python generate_dataset.py --rows 1000  # build a larger set
```

Only the Python standard library is required — no `pip install` needed.

Looking for **real-world data** instead? See `data/external/` — 12,763 real
PolitiFact statements (LIAR benchmark) plus an evaluation script.

---

## Quick look (PowerShell)

```powershell
# Row count
(Import-Csv .\truthlens_news_dataset.csv).Count

# Class balance
Import-Csv .\truthlens_news_dataset.csv | Group-Object label |
  Select-Object Name, Count
```

```python
# Python / pandas
import pandas as pd

df = pd.read_csv("data/truthlens_news_dataset.csv")
print(df["label"].value_counts())
print(df.sample(3, random_state=0)[["id", "label", "text"]].to_string())
```

```python
# Minimal baseline classifier (scikit-learn) — for a report/demo only
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=0, stratify=df["label"]
)
model = LogisticRegression(max_iter=1000)
model.fit(TfidfVectorizer().fit_transform(X_train), y_train)
print(model.score(TfidfVectorizer().fit_transform(X_test), y_test))
```

> A high score here only means the model learned **this synthetic template style**.
> It says nothing about performance on real news. Write that caveat in your report.

---

## Using real data for real work

For genuine misinformation research, use a published, licensed corpus instead.
These are well-known starting points (check each licence before use):

| Dataset | What it is | Link |
|---------|------------|------|
| **LIAR** | 12.8k PolitiFact short statements, 6-way truth labels | https://huggingface.co/datasets/liar |
| **FakeNewsNet** | Politifact + GossipCop with social context | https://github.com/KaiDMML/FakeNewsNet |
| **ISOT Fake News** | ~44k real/fake news articles | https://onlineacademiccommunity.uvic.ca/isot/ |
| **WELFake** | ~72k articles, merged from several sets | https://huggingface.co/datasets/davanstrien/WELFake |
| **FakeHealth / CoAID** | Health misinformation (COVID-19 era) | https://github.com/sunlabuiuc/CoAID |
| **NELA-GT** | Large multi-source news corpus with source labels | https://github.com/MELALab/nela-gt |
| **RumourEval / CheckThat!** | Rumour verification + claim detection | https://checkthat.gitlab.io/ |
| **FEVER** | Fact verification against Wikipedia | https://fever.ai/ |

**Important:** `Likely Real` / `Likely Fake` in *this* project are **text-pattern
signals from a language model**, not verified facts. Even with a real dataset, a
model's output is an indication that a human should verify — never a verdict.

---

## Ethics and responsible use

* Do not use the classifier to accuse named individuals or organisations.
* Do not present a model score as proof that a claim is true or false.
* Do not republish the fake-news rows as if they were genuine reporting.
* Always route important claims through reputable, independent sources and official
  fact-checkers (for example, your national press council or an IFCN signatory).

Built for a college / university project demonstration.
