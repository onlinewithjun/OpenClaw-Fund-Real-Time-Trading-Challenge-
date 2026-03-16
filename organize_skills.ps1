# organize_skills.ps1 - Organize skills into original and open-source categories

$ErrorActionPreference = "Stop"
$workspaceRoot = "C:\Users\Administrator\.openclaw\workspace"
$skillsRoot = Join-Path $workspaceRoot "skills"

# Define original skills (with copyright)
$originalSkills = @(
    "fund-challenge-daily-trader-core",
    "fund-challenge-data-guard",
    "fund-challenge-evidence-audit",
    "fund-challenge-execution-engine",
    "fund-challenge-identity-freshness-guard",
    "fund-challenge-instrument-rules",
    "fund-challenge-ledger-postmortem",
    "fund-challenge-market-calendar-gate",
    "fund-challenge-offexchange-exec-sim",
    "fund-challenge-orchestrator",
    "fund-challenge-position-risk-engine",
    "fund-challenge-signal-fusion-engine",
    "frontend-design"
)

# Create directory structure
$originalDir = Join-Path $skillsRoot "original"
$opensourceDir = Join-Path $skillsRoot "opensource"

Write-Host "Creating directory structure..." -ForegroundColor Cyan
if (-not (Test-Path $originalDir)) {
    New-Item -ItemType Directory -Path $originalDir | Out-Null
    Write-Host "  Created: $originalDir" -ForegroundColor Green
}
if (-not (Test-Path $opensourceDir)) {
    New-Item -ItemType Directory -Path $opensourceDir | Out-Null
    Write-Host "  Created: $opensourceDir" -ForegroundColor Green
}

# Move original skills
Write-Host "`nMoving original skills..." -ForegroundColor Cyan
foreach ($skill in $originalSkills) {
    $srcPath = Join-Path $skillsRoot $skill
    $destPath = Join-Path $originalDir $skill
    
    if (Test-Path $srcPath) {
        Write-Host "  Moving: $skill -> original/" -ForegroundColor Yellow
        Move-Item -Path $srcPath -Destination $destPath -Force
    } else {
        Write-Host "  Warning: $skill not found at $srcPath" -ForegroundColor Red
    }
}

# Move all other skills to opensource
Write-Host "`nMoving open-source skills..." -ForegroundColor Cyan
Get-ChildItem -Path $skillsRoot -Directory | ForEach-Object {
    if ($_.Name -notin @("original", "opensource")) {
        $destPath = Join-Path $opensourceDir $_.Name
        Write-Host "  Moving: $($_.Name) -> opensource/" -ForegroundColor Yellow
        Move-Item -Path $_.FullName -Destination $destPath -Force
    }
}

Write-Host "`n✓ Skills organization complete!" -ForegroundColor Green
Write-Host "  Original skills: $($originalSkills.Count)" -ForegroundColor Cyan
Write-Host "  Open-source skills: $((Get-ChildItem -Path $opensourceDir -Directory).Count)" -ForegroundColor Cyan
