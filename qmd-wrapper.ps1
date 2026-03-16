#!/usr/bin/env pwsh
# PowerShell wrapper for qmd

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Check Node version
$nodeVersion = node --version 2>&1
if ($nodeVersion -match 'v(\d+)') {
    $majorVersion = [int]$matches[1]
    if ($majorVersion -lt 22) {
        Write-Error "Error: node (>=22) not found. Install from https://nodejs.org"
        exit 1
    }
} else {
    Write-Error "Error: node not found. Install from https://nodejs.org"
    exit 1
}

# Path to qmd
$qmdPath = "C:\nvm4w\nodejs\node_modules\@tobilu\qmd\dist\qmd.js"

if (-not (Test-Path $qmdPath)) {
    Write-Error "Error: qmd not found at $qmdPath"
    exit 1
}

# Run qmd
node $qmdPath $Arguments