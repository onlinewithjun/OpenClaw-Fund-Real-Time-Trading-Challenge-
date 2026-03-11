param(
  [Parameter(Mandatory=$true)]
  [string]$Command
)

$ErrorActionPreference = 'Stop'
$env:HTTP_PROXY = ''
$env:HTTPS_PROXY = ''
$env:ALL_PROXY = ''
$env:http_proxy = ''
$env:https_proxy = ''
$env:all_proxy = ''
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Invoke-Expression $Command
