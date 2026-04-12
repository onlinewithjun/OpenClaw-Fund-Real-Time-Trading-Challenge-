# Basic Memory Compaction Script for OpenClaw
# Simple approach: Remove system status sections and redundant content

param(
    [string]$MemoryPath = "memory",
    [int]$MaxFileSizeKB = 2,
    [bool]$DryRun = $false
)

Write-Host "🚀 Starting Basic Memory Compaction..." -ForegroundColor Green
Write-Host "Memory Path: $MemoryPath" -ForegroundColor Cyan
Write-Host "Max File Size: ${MaxFileSizeKB}KB" -ForegroundColor Cyan
Write-Host "Dry Run: $DryRun" -ForegroundColor Cyan

# Get all daily memory files
$MemoryFiles = Get-ChildItem -Path $MemoryPath -Filter "*.md" | Where-Object { $_.Name -match "^\d{4}-\d{2}-\d{2}\.md$" }

Write-Host "📊 Found $($MemoryFiles.Count) daily memory files" -ForegroundColor Yellow

$TotalBytesSaved = 0
$FilesProcessed = 0

foreach ($File in $MemoryFiles) {
    $OriginalSize = $File.Length
    $Content = Get-Content -Path $File.FullName -Raw
    
    # Simple compression: Remove system status sections (basic approach)
    # Look for common patterns that can be safely removed
    $OptimizedContent = $Content
    
    # Remove verbose system status blocks (if they exist)
    if ($OptimizedContent -match "## 系统状态") {
        # Find the start and end of system status section
        $Lines = $OptimizedContent -split "`n"
        $NewLines = @()
        $InSystemStatus = $false
        
        foreach ($Line in $Lines) {
            if ($Line -match "^## 系统状态") {
                $InSystemStatus = $true
                continue
            }
            if ($InSystemStatus -and ($Line -match "^## " -or $Line -eq "")) {
                $InSystemStatus = $false
            }
            if (-not $InSystemStatus) {
                $NewLines += $Line
            }
        }
        
        $OptimizedContent = $NewLines -join "`n"
    }
    
    # Remove duplicate empty lines
    $OptimizedContent = $OptimizedContent -replace "`n`n`n+", "`n`n"
    
    $NewSize = $OptimizedContent.Length
    $BytesSaved = $OriginalSize - $NewSize
    
    if ($BytesSaved -gt 0 -and $NewSize -gt 0) {
        if (-not $DryRun) {
            Set-Content -Path $File.FullName -Value $OptimizedContent -Encoding UTF8
            Write-Host "✅ Compressed: $($File.Name) ($([math]::Round($OriginalSize/1024,1))KB → $([math]::Round($NewSize/1024,1))KB)" -ForegroundColor Green
        } else {
            Write-Host "🔍 Would compress: $($File.Name) ($([math]::Round($OriginalSize/1024,1))KB → $([math]::Round($NewSize/1024,1))KB)" -ForegroundColor Blue
        }
        $TotalBytesSaved += $BytesSaved
        $FilesProcessed++
    } elseif ($NewSize -le ($MaxFileSizeKB * 1024)) {
        Write-Host "ℹ️  File already optimized: $($File.Name) ($([math]::Round($NewSize/1024,1))KB)" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  File too large but no compression possible: $($File.Name) ($([math]::Round($NewSize/1024,1))KB)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📊 Compaction Summary:" -ForegroundColor Cyan
Write-Host "  Files processed: $FilesProcessed" -ForegroundColor White
Write-Host "  Total bytes saved: $([math]::Round($TotalBytesSaved/1024,1))KB" -ForegroundColor White
Write-Host "  Dry run mode: $DryRun" -ForegroundColor White
Write-Host "✅ Memory compaction completed!" -ForegroundColor Green