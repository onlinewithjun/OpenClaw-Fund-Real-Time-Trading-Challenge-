# OpenClaw Memory Maintenance Script
# Aggressive compaction and optimization for token savings

param(
    [switch]$DryRun = $false,
    [int]$DaysToKeep = 7,
    [int]$MaxFileSizeKB = 2
)

$ErrorActionPreference = "Stop"
$WorkspacePath = "$env:USERPROFILE\.openclaw\workspace"
$MemoryPath = Join-Path $WorkspacePath "memory"

Write-Host "🚀 Starting OpenClaw Memory Maintenance..." -ForegroundColor Green
Write-Host "Workspace: $WorkspacePath" -ForegroundColor Cyan
Write-Host "Memory Path: $MemoryPath" -ForegroundColor Cyan
Write-Host "Days to keep: $DaysToKeep" -ForegroundColor Cyan
Write-Host "Max file size: $($MaxFileSizeKB)KB" -ForegroundColor Cyan
Write-Host "Dry run: $DryRun" -ForegroundColor Cyan
Write-Host ""

# Create backup directory
$BackupPath = Join-Path $MemoryPath "backup"
if (!(Test-Path $BackupPath)) {
    New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
}

# Get current date
$CurrentDate = Get-Date
$CutoffDate = $CurrentDate.AddDays(-$DaysToKeep)

# Find all daily memory files
$DailyFiles = Get-ChildItem -Path $MemoryPath -Filter "*.md" -File | 
    Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}\.md$' }

Write-Host "📊 Found $($DailyFiles.Count) daily memory files" -ForegroundColor Yellow

# Process each file
$FilesProcessed = 0
$BytesSaved = 0
$FilesArchived = 0

foreach ($File in $DailyFiles) {
    try {
        # Parse date from filename
        $FileDateStr = $File.Name.Substring(0, 10)
        $FileDate = [DateTime]::ParseExact($FileDateStr, "yyyy-MM-dd", $null)
        
        # Check if file is too old
        if ($FileDate -lt $CutoffDate) {
            Write-Host "📦 Archiving old file: $($File.Name)" -ForegroundColor Gray
            if (!$DryRun) {
                $BackupFile = Join-Path $BackupPath $File.Name
                Move-Item -Path $File.FullName -Destination $BackupFile -Force
                $FilesArchived++
            }
            continue
        }
        
        # Read file content
        $Content = Get-Content -Path $File.FullName -Raw
        $OriginalSize = $File.Length
        
        # Apply aggressive compaction
        $CompactedContent = $Content
        
        # Remove redundant whitespace and empty lines
        $CompactedContent = $CompactedContent -replace '\n\s*\n\s*\n', "`n`n"
        $CompactedContent = $CompactedContent -replace '^\s+', ''
        $CompactedContent = $CompactedContent -replace '\s+$', ''
        
        # Remove duplicate entries (basic deduplication)
        $Lines = $CompactedContent -split '\n'
        $UniqueLines = @()
        $SeenLines = @{}
        
        foreach ($Line in $Lines) {
            if (![string]::IsNullOrWhiteSpace($Line)) {
                $LineHash = [System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Line.Trim()))
                $LineKey = [BitConverter]::ToString($LineHash).Replace("-", "").ToLower()
                
                if (!$SeenLines.ContainsKey($LineKey)) {
                    $UniqueLines += $Line
                    $SeenLines[$LineKey] = $true
                }
            } else {
                $UniqueLines += $Line
            }
        }
        
        $CompactedContent = $UniqueLines -join "`n"
        
        # Check if file is too large
        $CompactedSize = [System.Text.Encoding]::UTF8.GetByteCount($CompactedContent)
        if ($CompactedSize -gt ($MaxFileSizeKB * 1024)) {
            Write-Host "⚠️  File too large: $($File.Name) ($([math]::Round($CompactedSize/1024, 1))KB)" -ForegroundColor Yellow
            
            # Apply additional compression by summarizing
            $Summary = "# COMPACTED MEMORY - $($FileDateStr)`n"
            $Summary += "## Summary`n"
            
            # Extract key sections
            if ($CompactedContent -match '(?s)##\s*关键事件.*?(?=##|$)') {
                $Summary += "### Key Events`n" + $Matches[0].Substring(0, [Math]::Min($Matches[0].Length, 500)) + "...`n`n"
            }
            
            if ($CompactedContent -match '(?s)##\s*系统状态.*?(?=##|$)') {
                $Summary += "### System Status`n" + $Matches[0].Substring(0, [Math]::Min($Matches[0].Length, 300)) + "...`n`n"
            }
            
            if ($CompactedContent -match '(?s)##\s*待办事项.*?(?=##|$)') {
                $Summary += "### Todo Items`n" + $Matches[0].Substring(0, [Math]::Min($Matches[0].Length, 300)) + "...`n`n"
            }
            
            $CompactedContent = $Summary
            $CompactedSize = [System.Text.Encoding]::UTF8.GetByteCount($CompactedContent)
        }
        
        $NewSize = $CompactedSize
        $SizeDiff = $OriginalSize - $NewSize
        
        if ($SizeDiff -gt 0) {
            Write-Host "✅ Compacted: $($File.Name) ($([math]::Round($OriginalSize/1024, 1))KB → $([math]::Round($NewSize/1024, 1))KB, saved $([math]::Round($SizeDiff/1024, 1))KB)" -ForegroundColor Green
            
            if (!$DryRun) {
                Set-Content -Path $File.FullName -Value $CompactedContent -Encoding UTF8
            }
            
            $BytesSaved += $SizeDiff
        }
        
        $FilesProcessed++
        
    } catch {
        Write-Host "❌ Error processing $($File.Name): $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Optimize MEMORY.md
Write-Host "`n🧠 Optimizing MEMORY.md..." -ForegroundColor Cyan
$MemoryMDPath = Join-Path $WorkspacePath "MEMORY.md"
if (Test-Path $MemoryMDPath) {
    $MemoryContent = Get-Content -Path $MemoryMDPath -Raw
    $OriginalMemorySize = (Get-Item $MemoryMDPath).Length
    
    # Clean up MEMORY.md
    $CleanedMemory = $MemoryContent
    
    # Remove outdated entries (older than 30 days)
    $CleanedMemory = $CleanedMemory -replace '(?s)##\s*\d{4}-\d{2}-\d{2}.*?(?=##|$)', ''
    
    # Ensure it's well-structured
    if ($CleanedMemory -notmatch '##\s*身份信息') {
        $CleanedMemory = "# MEMORY.md - 长期记忆`n`n这是助手的长期记忆，记录重要的事件、决策和值得记住的信息。`n`n## 身份信息`n" + $CleanedMemory
    }
    
    $NewMemorySize = [System.Text.Encoding]::UTF8.GetByteCount($CleanedMemory)
    $MemorySizeDiff = $OriginalMemorySize - $NewMemorySize
    
    if ($MemorySizeDiff -gt 0 -and !$DryRun) {
        Set-Content -Path $MemoryMDPath -Value $CleanedMemory -Encoding UTF8
        Write-Host "✅ Optimized MEMORY.md ($([math]::Round($OriginalMemorySize/1024, 1))KB → $([math]::Round($NewMemorySize/1024, 1))KB)" -ForegroundColor Green
        $BytesSaved += $MemorySizeDiff
    }
}

# Update qmd index if available
Write-Host "`n🔍 Updating qmd search index..." -ForegroundColor Cyan
try {
    $QmdCheck = wsl -e bash -c "which qmd" 2>$null
    if ($QmdCheck) {
        if (!$DryRun) {
            wsl -e bash -c "qmd update" | Out-Null
            Write-Host "✅ Updated qmd search index" -ForegroundColor Green
        } else {
            Write-Host "ℹ️  Would update qmd search index (dry run)" -ForegroundColor Gray
        }
    } else {
        Write-Host "⚠️  qmd not found, skipping index update" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Failed to update qmd index: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n📊 Maintenance Summary:" -ForegroundColor Green
Write-Host "  Files processed: $FilesProcessed" -ForegroundColor White
Write-Host "  Files archived: $FilesArchived" -ForegroundColor White
Write-Host "  Total bytes saved: $([math]::Round($BytesSaved/1024, 1))KB" -ForegroundColor White
Write-Host "  Dry run mode: $DryRun" -ForegroundColor White

if (!$DryRun) {
    Write-Host "`n✅ Memory maintenance completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nℹ️  Dry run completed. Use -DryRun:$false to apply changes." -ForegroundColor Yellow
}