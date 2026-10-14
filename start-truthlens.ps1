<#
.SYNOPSIS
  Starts the TruthLens AI project (backend + frontend) and opens it in your browser.
.DESCRIPTION
  Double-click this file (or run it in PowerShell) any time you want to use
  the website. It opens two terminal windows — one for the FastAPI backend,
  one for the React frontend — waits until both answer, then opens
  http://localhost:5173 in your default browser.

  To stop everything: close the two "TruthLens" terminal windows,
  or run:  Get-Process python,vite,node | Stop-Process
#>

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Wait-Http($Url, $Name, $TimeoutSec = 90) {
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while ((Get-Date) -lt $deadline) {
        try {
            $r = Invoke-WebRequest -Uri $Url -TimeoutSec 5 -UseBasicParsing
            if ($r.StatusCode -eq 200) {
                Write-Host "  [OK] $Name is up ($Url)" -ForegroundColor Green
                return $true
            }
        } catch { Start-Sleep -Seconds 2 }
    }
    Write-Host "  [!!] $Name did not start in time ($Url)" -ForegroundColor Red
    return $false
}

function Test-PortOpen($Url) {
    try {
        $r = Invoke-WebRequest -Uri $Url -TimeoutSec 4 -UseBasicParsing
        return $r.StatusCode -eq 200
    } catch { return $false }
}

Write-Host ""
Write-Host "  TruthLens AI - starting servers..." -ForegroundColor Cyan

# 1. Backend (FastAPI + uvicorn)
$backendUp = Test-PortOpen "http://localhost:8000/api/health"
if ($backendUp) {
    Write-Host "  [OK] backend already running - reusing it" -ForegroundColor Green
} else {
$backend = Join-Path $Root "backend"
if (-not (Test-Path (Join-Path $backend "venv\Scripts\python.exe"))) {
    Write-Host "  [!!] Backend virtual environment not found." -ForegroundColor Red
    Write-Host "       Run the setup steps in README.md first (py -3.12 -m venv venv ...)."
    Read-Host "Press Enter to exit"
    exit 1
}
Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$backend'; .\venv\Scripts\Activate.ps1; $Host.UI.RawUI.WindowTitle = 'TruthLens Backend :8000'; python main.py"
) | Out-Null
Write-Host "  [..] backend terminal launched" -ForegroundColor Gray
}

# 2. Frontend (React + Vite)
$frontendUp = Test-PortOpen "http://localhost:5173/"
if ($frontendUp) {
    Write-Host "  [OK] frontend already running - reusing it" -ForegroundColor Green
} else {
$frontend = Join-Path $Root "frontend"
if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    Write-Host "  [!!] Frontend dependencies not installed." -ForegroundColor Red
    Write-Host "       Run 'npm install' inside the frontend folder first (see README.md)."
    Read-Host "Press Enter to exit"
    exit 1
}
Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$frontend'; $Host.UI.RawUI.WindowTitle = 'TruthLens Frontend :5173'; npm run dev"
) | Out-Null
Write-Host "  [..] frontend terminal launched" -ForegroundColor Gray
}

# 3. Wait, then open the browser
Write-Host ""
$apiOk = Wait-Http "http://localhost:8000/api/health" "Backend API"
$webOk = Wait-Http "http://localhost:5173/" "Frontend site"

if ($webOk) {
    Write-Host ""
    Write-Host "  Opening http://localhost:5173 ..." -ForegroundColor Cyan
    Start-Process "http://localhost:5173/"
} else {
    Write-Host ""
    Write-Host "  Servers may still be starting - check the two terminal windows." -ForegroundColor Yellow
}

if (-not $apiOk) {
    Write-Host "  Tip: analysis needs a Groq key in backend\.env (see README.md)." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Leave the two terminal windows open while you use the site." -ForegroundColor Gray
Write-Host "  To stop: close both windows." -ForegroundColor Gray
Write-Host ""
