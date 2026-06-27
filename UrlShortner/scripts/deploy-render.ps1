param(
    [Parameter(Mandatory = $false)]
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

Write-Host "Preparing repository for Render deployment..." -ForegroundColor Cyan

Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or not available in PATH."
}

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "Committing pending changes..." -ForegroundColor Yellow
    git add .
    git commit -m "chore: add production deployment config for Render"
} else {
    Write-Host "No local changes to commit." -ForegroundColor Green
}

Write-Host "Pushing to origin/$Branch ..." -ForegroundColor Cyan
git push origin $Branch

Write-Host "Done. Now complete these manual cloud steps:" -ForegroundColor Green
Write-Host "1) Create free PostgreSQL on Neon"
Write-Host "2) Create free Redis on Upstash"
Write-Host "3) Create Render Web Service from this repo (Docker)"
Write-Host "4) Add environment variables in Render dashboard"
Write-Host "5) Deploy and verify /actuator/health"

