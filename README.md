# 🛡️ TruthLens AI — Smart Fake News Detection System

> **"Question the News. Discover the Signals."**

An AI-powered web application that analyzes news headlines, articles, and social media posts for potential misinformation patterns. Built with React, FastAPI, and the Groq API.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![React](https://img.shields.io/badge/React-18-61dafb)
![License](https://img.shields.io/badge/License-Educational-orange)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Run It Anytime](#-run-it-anytime)
- [Accounts & Login](#-accounts--login)
- [Usage](#-usage)
- [Demo Dataset](#-demo-dataset)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

- **AI-Powered Analysis** — Uses Groq-hosted LLaMA 3.3 70B to analyze text patterns
- **Three-Tier Classification** — Likely Real, Likely Fake, or Unverified/Insufficient Evidence
- **Suspicious Signal Detection** — Identifies sensationalism, missing attribution, and logical fallacies
- **Claim Extraction** — Highlights key factual claims that need verification
- **Fact-Checking Guidance** — Provides concrete verification steps
- **Analysis History** — View past analyses stored locally in your browser
- **Accounts & Login** — Register and sign in (local demo auth with JWT sessions); Analyze and History pages require sign-in
- **One-Click Launch** — `start-truthlens.ps1` starts both servers and opens the site; optional auto-start on Windows sign-in
- **Responsive Design** — Works on desktop, tablet, and mobile
- **Premium Dark UI** — Polished SaaS-style interface with glass morphism and animations

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS v4, Framer Motion, Lucide Icons |
| **Backend** | Python 3.10+, FastAPI, Pydantic v2, Groq SDK |
| **AI** | Groq API → LLaMA 3.3 70B Versatile |
| **Storage** | Browser localStorage (client-side only) |

---

## 📦 Prerequisites

Before you begin, make sure you have:

1. **Python 3.10 or higher** — [Download here](https://www.python.org/downloads/)
   - ⚠️ Check "Add Python to PATH" during installation
   - ⚠️ Python 3.7/3.8/3.9 will **not** work (FastAPI + Pydantic v2 require 3.10+).
     The backend fails fast with a clear message on older versions.
   - Windows shortcut (PowerShell, admin not required):
     ```powershell
     winget install Python.Python.3.12
     py -3.12 --version   # confirm the new version; use `py -3.12` instead of `python`
     ```
2. **Node.js 18 or higher** — [Download here](https://nodejs.org/)
3. **A Groq API Key** — [Get one free at console.groq.com](https://console.groq.com)

Verify your installations:

```powershell
python --version   # Should show 3.10+
node --version     # Should show 18+
npm --version      # Should show 8+
```

---

## 🚀 Installation

### Step 1: Clone or navigate to the project directory

```powershell
cd "c:\Users\HP\OneDrive\Desktop\FN\Fraud news detection"
```

### Step 2: Set up the Backend

```powershell
# Create and activate a virtual environment
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Set up the Frontend

Open a **new PowerShell terminal**:

```powershell
cd "c:\Users\HP\OneDrive\Desktop\FN\Fraud news detection\frontend"
npm install
```

---

## ⚙️ Configuration

### Step 1: Create the backend `.env` file

```powershell
cd "c:\Users\HP\OneDrive\Desktop\FN\Fraud news detection\backend"
Copy-Item .env.example .env
```

### Step 2: Edit the `.env` file

Open `backend/.env` in a text editor and replace the placeholder:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
SECRET_KEY=a-long-random-string-you-generate-once
```

Generate the secret with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

> ⚠️ **Key format check:** real Groq API keys start with `gsk_` and are about
> 56 characters long. If analysis requests fail with **401 Unauthorized**, the
> value in `backend/.env` is not a valid Groq key — get a free one at
> https://console.groq.com/keys and paste it in.

> ⚠️ **Never commit your `.env` file to version control.** It is already in `.gitignore`.

---

## ▶️ Running the Application

You need **two separate PowerShell terminals**:

### Terminal 1 — Backend (FastAPI)

```powershell
cd "c:\Users\HP\OneDrive\Desktop\FN\Fraud news detection\backend"
.\venv\Scripts\Activate.ps1
python main.py
```

The backend will start at: **http://localhost:8000**

### Terminal 2 — Frontend (React + Vite)

```powershell
cd "c:\Users\HP\OneDrive\Desktop\FN\Fraud news detection\frontend"
npm run dev
```

The frontend will start at: **http://localhost:5173**

### Access Points

| URL | Description |
|-----|-------------|
| http://localhost:5173 | Frontend application |
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | Swagger API documentation |
| http://localhost:8000/redoc | ReDoc API documentation |

---

## ▶️ Run It Anytime

Don't want to type commands every time? Use the launcher script:

**Option A — Double-click (recommended)**

1. Open the project folder in File Explorer:
   `Fraud news detection`
2. Right-click `start-truthlens.ps1` → **Run with PowerShell**
   (first run only: if Windows blocks it, run
   `powershell -ExecutionPolicy Bypass -File start-truthlens.ps1` instead)
3. The script starts both servers in their own windows, waits until they
   answer, and opens **http://localhost:5173** in your browser.

**Option B — Auto-start on Windows sign-in (optional)**

Run once:

```powershell
cd "c:\Users\HP\OneDrive\Desktop\FN\Fraud news detection"
powershell -ExecutionPolicy Bypass -File install-autostart.ps1
```

The servers will now launch automatically every time you sign in.
To undo, press `Win+R`, type `shell:startup`, and delete the
"TruthLens AI" shortcut.

**Stopping the servers**

- Close the two "TruthLens" terminal windows, or run:
  ```powershell
  Get-Process python,vite,node -ErrorAction SilentlyContinue | Stop-Process
  ```
- Note: `users.db` (your local accounts) is kept — your logins survive restarts.

---

## 🔐 Accounts & Login

The Analyze and History pages require an account. Registration takes seconds:

1. Open http://localhost:5173 and click **Sign In** (or go to Analyze — you'll be redirected).
2. Switch to the **Register** tab, enter any email and a password (min. 8 characters).
3. You're signed in immediately and taken to the Analyzer.

How it works:

- Passwords are stored as salted PBKDF2 hashes in `backend/users.db`
  (a local SQLite file on your PC — git-ignored, never uploaded).
- Sign-in returns a 7-day JWT session token kept in the browser.
- Signing out clears the token; expired/invalid sessions return to the login page.

> Demo-grade auth for a college project: no email verification, no rate
> limiting, no password reset. Good enough for a local demo — do not present
> it as production-grade security.

---

## 🔋 Offline Mode (works without an API key)

Analysis **always returns a result**, even when the Groq service is unreachable:

| Situation | What you get |
|-----------|--------------|
| Valid Groq key | Full AI assessment (`mode: "ai"`) |
| Missing / invalid key, no internet, timeout, rate limit, bad AI response | Local heuristic assessment (`mode: "offline"`) |

The offline check is deterministic and transparent: it names the exact
patterns it matched (capital-letter shouting, urgency pressure, vague
sourcing, absolutist language, missing attribution) and labels itself
everywhere — amber banner in the results card, `mode` field in the API and
copies, and explicit limitations. It is a useful demo fallback, **not** an AI
assessment. Add a real key for the full experience.

---

## 📖 Usage

1. Open **http://localhost:5173** in your browser
2. Click **"Analyze News"** or navigate to the Analyze page
3. Paste any news text, or click **"Try a Sample"** to load example content
4. Click **"Analyze"** and wait 10–30 seconds
5. Review the classification, suspicious signals, claims, and verification steps
6. Use the **"Copy Results"** button to save findings
7. View past analyses in the **History** tab

---

## 📊 Demo Dataset

The `data/` folder contains a **500-row synthetic demo dataset** for demonstrations,
testing, and presentations:

| File | Description |
|------|-------------|
| `data/truthlens_news_dataset.csv` | 500 rows (spreadsheet / `pandas` friendly) |
| `data/truthlens_news_dataset.json` | Same 500 rows as a JSON array |
| `data/generate_dataset.py` | Deterministic generator (stdlib only — no `pip install` needed) |
| `data/README.md` | Full schema, usage examples, and ethics notes |

- Balanced across the app's three classes (~167 Likely Real / 167 Likely Fake /
  166 Unverified), 10 topic categories, and 3 source types (headline, social post,
  full article).
- **All synthetic:** fictional organisations, places, officials and numbers.
  Labels encode the text's *characteristic pattern*, not real-world truth.
  See `data/README.md` before using it in a report.

### Real-world data: LIAR benchmark (`data/external/`)

Yes — external datasets work with this project. `data/external/` contains
**12,763 real PolitiFact statements** (LIAR, Wang 2017), normalized to the same
schema, plus an evaluation script:

```powershell
cd ".\data\external"
python fetch_liar.py            # re-download / re-normalize (stdlib only)

cd ..\..\backend
.\venv\Scripts\python.exe ..\data\external\evaluate_offline.py --n 600
```

Measured agreement of the offline heuristic: **57.7% on synthetic style,
33.3% on real one-line claims** (it correctly abstains to Unverified ~89% of
the time). Full methodology, ethics notes, and report-ready interpretation in
`data/external/README.md`.

```powershell
cd ".\data"
python generate_dataset.py              # rebuild the 500 rows
python generate_dataset.py --rows 1000  # build a larger set

# Row count + class balance
(Import-Csv .\truthlens_news_dataset.csv).Count
Import-Csv .\truthlens_news_dataset.csv | Group-Object label | Select-Object Name, Count
```

---

## 📡 API Documentation

### Health Check

```
GET /api/health
```

Response:
```json
{
  "status": "ok",
  "service": "TruthLens AI API",
  "model_configured": "llama-3.3-70b-versatile"
}
```

### Analyze News

```
POST /api/analyze
Content-Type: application/json

{
  "text": "Your news article or headline here (20-15000 characters)"
}
```

Response:
```json
{
  "classification": "Unverified / Insufficient Evidence",
  "explanation": "...",
  "summary": "...",
  "suspicious_signals": ["..."],
  "claims_to_verify": ["..."],
  "verification_steps": ["..."],
  "evidence_limitations": ["..."]
}
```

### Authentication

```
POST /api/auth/register   { "email": "...", "password": "..." }  → 201 { user, token }
POST /api/auth/login      { "email": "...", "password": "..." }  → 200 { user, token }
GET  /api/auth/me         Authorization: Bearer <token>          → 200 { id, email, created_at }
```

Register also signs you in immediately (returns a token). Duplicate emails get
409, bad credentials get 401 without revealing whether the email exists.

---

## 🧪 Testing

### Run Backend Tests

```powershell
cd "c:\Users\HP\OneDrive\Desktop\FN\Fraud news detection\backend"
.\venv\Scripts\Activate.ps1
python -m pytest tests/ -v
```

Tests include:
- ✅ Health check endpoint
- ✅ Empty/invalid input validation
- ✅ Valid input with mocked Groq response
- ✅ Malformed AI response handling
- ✅ Rate limit error handling
- ✅ Register / duplicate / invalid email / short password
- ✅ Login success / wrong password / session (`/me`) / bad token

> Tests use mocked Groq responses — no API key or paid calls required.

---

## 🔧 Troubleshooting

### "GROQ_API_KEY is not set"
→ Make sure you created `backend/.env` with your actual Groq API key.

### "401 Unauthorized" from the Groq API
→ The key in `backend/.env` is not a valid Groq key. Groq keys start with
`gsk_`. Paste a fresh key from https://console.groq.com/keys — no code changes needed.

### Backend fails with "requires Python 3.10 or higher"
→ You are running an old Python (e.g. 3.7). Install Python 3.10+ (see
Prerequisites), delete the old `backend\venv` folder, and recreate the virtual
environment with the new Python.

### "Could not connect" only when signed in
→ Fixed in the current code (the backend allows the `Authorization` header).
If you see it, restart the backend so it loads the latest code.

### Backend seems stuck on old code after edits
→ The dev auto-reloader can miss rapid file changes (worse on OneDrive-synced
folders). Stop the backend terminal (`Ctrl+C`) and start it again with
`python main.py` — or just run `start-truthlens.ps1` after closing old windows.

### "Could not connect to the TruthLens AI server"
→ Make sure the backend is running (`python main.py` in the backend directory).

### "CORS error" in browser console
→ Ensure the backend is running on port 8000 and the frontend on port 5173.

### "Module not found" when starting backend
→ Make sure you activated the virtual environment: `.\venv\Scripts\Activate.ps1`

### "npm install" fails
→ Delete `node_modules` and `package-lock.json`, then run `npm install` again.

### Rate limit errors from Groq
→ Wait 30-60 seconds and try again. The free tier has per-minute rate limits.

### Python version error
→ Ensure Python 3.10+ is installed: `python --version`
→ If several Pythons are installed, use the launcher: `py -3.12 -m venv venv`

---

## ✅ Verification Checklist

Use this checklist to verify everything works:

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Groq API key obtained
- [ ] `backend/.env` created with API key
- [ ] Backend virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend starts without errors on port 8000
- [ ] `http://localhost:8000/api/health` returns `{"status": "ok"}`
- [ ] Frontend starts without errors on port 5173
- [ ] Landing page loads with hero section
- [ ] Navigation works (Home, Analyze, History, About)
- [ ] Sample text loads when clicking "Try a Sample"
- [ ] Analysis completes and shows results
- [ ] Results show classification, signals, claims, and steps
- [ ] "Copy Results" button works
- [ ] "Analyze Another" button resets the form
- [ ] History page shows past analyses
- [ ] About page explains the workflow
- [ ] Logged-out visit to /analyze redirects to /login
- [ ] Register creates an account and lands on /analyze signed in
- [ ] Navbar shows your email with a Sign Out button
- [ ] Sign Out clears the session and returns to login on protected pages
- [ ] `start-truthlens.ps1` launches both servers and opens the browser
- [ ] `data/truthlens_news_dataset.csv` opens with 500 rows
- [ ] `python data\generate_dataset.py --rows 500` regenerates CSV + JSON

---

## ⚠️ Disclaimer

**TruthLens AI** uses a language model to analyze text patterns. It does **not**:
- Access the internet to verify claims
- Query fact-checking databases
- Provide definitive proof of truth or falsehood

AI-generated assessments can be incorrect. The classification reflects text-pattern analysis, not independent fact-checking. **Always verify important claims through reputable, independent news sources.**

Submitted text is sent to the Groq API for analysis. No content is stored on the server.

---

## 📄 License

Built for educational purposes. This is a college/university project demonstration.

---

Made with ❤️ for responsible AI
