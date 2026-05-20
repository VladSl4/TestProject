# Launches the three backend services in separate PowerShell windows.
# Order matters: database_service (gRPC :5001) -> proxy_service (gRPC :5002) -> gateway (REST :8000).
# From the repo root:  .\start_backend.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$backend = Join-Path $root "backend"

function Start-Service-Window([string]$title, [string]$module) {
    $cmd = "Set-Location '$backend'; `$Host.UI.RawUI.WindowTitle = '$title'; py -3 -m $module"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $cmd
}

Start-Service-Window "database_service :5001 (gRPC)" "database_service.main"
Start-Sleep -Seconds 2
Start-Service-Window "proxy_service :5002 (gRPC)" "proxy_service.main"
Start-Sleep -Seconds 1
Start-Service-Window "gateway :8000 (REST)" "gateway.main"

Write-Host "Three windows launched:"
Write-Host "  - database_service  :: gRPC  127.0.0.1:5001"
Write-Host "  - proxy_service     :: gRPC  127.0.0.1:5002"
Write-Host "  - gateway           :: REST  http://127.0.0.1:8000/docs"
