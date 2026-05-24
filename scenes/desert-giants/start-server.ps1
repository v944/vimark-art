$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
Write-Host "Starting local server on port 8080..." -ForegroundColor Green
Write-Host "Open http://localhost:8080 in your browser" -ForegroundColor Cyan
python3 -m http.server 8080
