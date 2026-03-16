# Simple Daily Memory Compaction Script
# This script compresses daily memory files by removing redundant system status sections

param(
    [string]$MemoryPath = "memory",
    [int]$MaxFileSizeKB = 2,
    [switch]$DryRun = $false
)

Write-Host "🚀 Starting Simple Memory Compaction..." -ForegroundColor Green
Write-Host "Memory Path: $MemoryPath" -ForegroundColor Cyan
Write-Host "Max File Size: ${MaxFileSizeKB}KB" -ForegroundColor Cyan
Write-Host "Dry Run: $DryRun" -ForegroundColor Cyan

# Get all daily memory files
$MemoryFiles = Get-ChildItem -Path $MemoryPath -Filter "*.md" | Where-Object { $_.Name -match "^\d{4}-\d{2}-\d{2}\.md$" }

if ($MemoryFiles.Count -eq 0) {
    Write-Host "⚠️  No daily memory files found." -ForegroundColor Yellow
    return
}

Write-Host "📊 Found $($MemoryFiles.Count) daily memory files" -ForegroundColor Cyan

$TotalBytesSaved = 0
$FilesProcessed = 0

foreach ($File in $MemoryFiles) {
    $FilePath = $File.FullName
    $OriginalSize = $File.Length
    $OriginalContent = Get-Content -Path $FilePath -Raw
    
    # Skip if file is already small enough
    if ($OriginalSize -le ($MaxFileSizeKB * 1024)) {
        Write-Host "✅ File already optimized: $($File.Name) ($([math]::Round($OriginalSize/1024, 1))KB)" -ForegroundColor Green
        continue
    }
    
    # Remove system status sections (simplified approach)
    $OptimizedContent = $OriginalContent
    
    # Remove system status blocks that start with "## 系统状态" and end before next ##
    $OptimizedContent = $OptimizedContent -replace '(?s)##\s*系统状态.*?(?=##|$)', ''
    
    # Remove empty lines and normalize whitespace
    $OptimizedContent = $OptimizedContent -replace '\n\s*\n', "`n`n"
    $OptimizedContent = $OptimizedContent.Trim()
    
    $NewSize = [System.Text.Encoding]::UTF8.GetByteCount($OptimizedContent)
    $BytesSaved = $OriginalSize - $NewSize
    
    if ($BytesSaved -gt 0) {
        Write-Host "🔧 Compressed: $($File.Name) ($([math]::Round($OriginalSize/1024, 1))KB → $([math]::Round($NewSize/1024, 1))KB, saved $([math]::Round($BytesSaved/1024, 1))KB)" -ForegroundColor Yellow
        
        if (-not $DryRun) {
            Set-Content -Path $FilePath -Value $OptimizedContent -Encoding UTF8
            $TotalBytesSaved += $BytesSaved
            $FilesProcessed++
        }
    } else {
        Write-Host "ℹ️  No compression possible: $($File.Name)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "📊 Compaction Summary:" -ForegroundColor Cyan
Write-Host "  Files processed: $FilesProcessed" -ForegroundColor White
Write-Host "  Total bytes saved: $([math]::Round($TotalBytesSaved/1024, 1))KB" -ForegroundColor White
Write-Host "  Dry run mode: $DryRun" -ForegroundColor White

Write-Host "✅ Memory compaction completed!" -ForegroundColor Green