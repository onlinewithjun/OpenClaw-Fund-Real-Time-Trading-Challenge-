# Memory Compaction Script for OpenClaw
# Aggressive compaction strategy to save tokens

param(
    [int]$DaysToKeep = 7,
    [string]$MemoryDir = "memory"
)

# Get current date
$CurrentDate = Get-Date -Format "yyyy-MM-dd"

# Function to compact a single memory file
function Compact-MemoryFile {
    param([string]$FilePath)
    
    $Content = Get-Content $FilePath -Raw
    if (!$Content) { return }
    
    # Remove empty lines and excessive whitespace
    $Compacted = $Content -replace '\n\s*\n', "`n`n" -replace '^\s+', '' -replace '\s+$', ''
    
    # Remove redundant timestamps and repetitive headers
    $Compacted = $Compacted -replace '## \d{4}-\d{2}-\d{2}.*?\n', ''
    $Compacted = $Compacted -replace '\*记忆存储时间：.*?\*', ''
    
    # Keep only essential information
    $EssentialLines = @()
    $Lines = $Compacted -split '\n'
    $InCodeBlock = $false
    
    foreach ($Line in $Lines) {
        if ($Line.Trim() -eq '```') {
            $InCodeBlock = !$InCodeBlock
            $EssentialLines += $Line
        }
        elseif ($InCodeBlock) {
            $EssentialLines += $Line
        }
        elseif ($Line.Trim().Length -gt 0 -and !$Line.Trim().StartsWith('---')) {
            $EssentialLines += $Line
        }
    }
    
    $FinalContent = ($EssentialLines -join "`n").Trim()
    
    # Only write if content is significantly different
    if ($FinalContent.Length -lt $Content.Length * 0.8) {
        Set-Content -Path $FilePath -Value $FinalContent
        $Saved = $Content.Length - $FinalContent.Length; Write-Host "Compacted $FilePath`: $Saved bytes saved"
    }
}

# Compact all daily memory files except today
$MemoryFiles = Get-ChildItem -Path $MemoryDir -Filter "*.md" | Where-Object { 
    $_.Name -ne "$CurrentDate.md" 
}

foreach ($File in $MemoryFiles) {
    Compact-MemoryFile $File.FullName
}

# Archive old files (older than $DaysToKeep days)
$CutoffDate = (Get-Date).AddDays(-$DaysToKeep)
$OldFiles = Get-ChildItem -Path $MemoryDir -Filter "*.md" | Where-Object { 
    $_.LastWriteTime -lt $CutoffDate -and $_.Name -ne "$CurrentDate.md"
}

if ($OldFiles) {
    $ArchiveDir = Join-Path $MemoryDir "archive"
    if (!(Test-Path $ArchiveDir)) {
        New-Item -ItemType Directory -Path $ArchiveDir | Out-Null
    }
    
    foreach ($File in $OldFiles) {
        Move-Item -Path $File.FullName -Destination $ArchiveDir
        Write-Host "Archived $($File.Name) to archive folder"
    }
}

Write-Host "Memory compaction completed!"