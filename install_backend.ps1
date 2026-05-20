# Install backend deps + generate gRPC stubs.
# From the repo root:  .\install_backend.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "Installing backend Python dependencies"
py -3 -m pip install -r (Join-Path $root "backend\requirements.txt")

Write-Host "Generating gRPC Python stubs from .proto files"
py -3 (Join-Path $root "backend\rpc\gen_protos.py")

Write-Host "Backend ready."
