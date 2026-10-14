<#
.SYNOPSIS
  (Optional) Auto-start TruthLens AI every time you sign in to Windows.
.DESCRIPTION
  Creates a shortcut in your Windows Startup folder that runs
  start-truthlens.ps1 on login, so the website is always a click away.
  Run once:  powershell -ExecutionPolicy Bypass -File install-autostart.ps1
  To undo: delete the "TruthLens AI" shortcut from the Startup folder
  (press Win+R, type shell:startup, Enter).
#>

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Target = Join-Path $Root "start-truthlens.ps1"
$Startup = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $Startup "TruthLens AI.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($ShortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$Target`""
$shortcut.WorkingDirectory = $Root
$shortcut.Description = "Start TruthLens AI servers on sign-in"
$shortcut.Save()

Write-Host "Done! TruthLens AI will now start automatically when you sign in." -ForegroundColor Green
Write-Host "Shortcut: $ShortcutPath" -ForegroundColor Gray
Write-Host "To remove: delete that shortcut (Win+R -> shell:startup)." -ForegroundColor Gray
