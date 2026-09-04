# PowerShell shim for the cscan evidence tool (Windows PowerShell 5.1+).
# Usage: .\tools\cscan.ps1 <freeze|inventory|search|scaffold|validate> [options]
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'cscan.py'
$py = 'python'
if (Get-Command python3 -ErrorAction SilentlyContinue) { $py = 'python3' }
& $py $script @args
exit $LASTEXITCODE
