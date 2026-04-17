# Optimize MEMORY.md - Long-term memory maintenance script
# This script compacts and optimizes the long-term memory file

param(
    [string]$MemoryDir = "memory",
    [string]$MemoryFile = "MEMORY.md",
    [int]$MaxSections = 10,
    [int]$MaxSectionLength = 2000
)

Write-Host "Optimizing MEMORY.md..." -ForegroundColor Green

# Read current MEMORY.md
if (Test-Path $MemoryFile) {
    $memoryContent = Get-Content $MemoryFile -Raw
} else {
    Write-Host "MEMORY.md not found, creating empty file" -ForegroundColor Yellow
    $memoryContent = "# MEMORY.md - 长期记忆`n`n这是助手的长期记忆，记录重要的事件、决策和值得记住的信息。"
}

# Parse sections
$sections = @()
$currentSection = ""
$currentTitle = ""

# Split by headers
$lines = $memoryContent -split "`n"
foreach ($line in $lines) {
    if ($line -match "^##\s+(.+)$") {
        # Save previous section if exists
        if ($currentTitle -ne "") {
            $sections += @{
                Title = $currentTitle
                Content = $currentSection.Trim()
            }
        }
        $currentTitle = $matches[1]
        $currentSection = ""
    } elseif ($currentTitle -ne "") {
        $currentSection += "$line`n"
    }
}

# Add last section
if ($currentTitle -ne "") {
    $sections += @{
        Title = $currentTitle
        Content = $currentSection.Trim()
    }
}

# Limit number of sections (keep most recent)
if ($sections.Count -gt $MaxSections) {
    $sections = $sections[($sections.Count - $MaxSections)..($sections.Count - 1)]
    Write-Host "Limited to last $MaxSections sections" -ForegroundColor Yellow
}

# Compact each section content
$optimizedSections = @()
foreach ($section in $sections) {
    $content = $section.Content
    
    # Remove duplicate lines
    $uniqueLines = @()
    $prevLine = ""
    foreach ($line in ($content -split "`n")) {
        if ($line.Trim() -ne "" -and $line.Trim() -ne $prevLine.Trim()) {
            $uniqueLines += $line
            $prevLine = $line
        }
    }
    
    # Join back
    $compactedContent = ($uniqueLines -join "`n").Trim()
    
    # Truncate if too long
    if ($compactedContent.Length -gt $MaxSectionLength) {
        $compactedContent = $compactedContent.Substring(0, $MaxSectionLength) + "... [truncated]"
        Write-Host "Truncated section '$($section.Title)' to $MaxSectionLength characters" -ForegroundColor Yellow
    }
    
    $optimizedSections += @{
        Title = $section.Title
        Content = $compactedContent
    }
}

# Rebuild MEMORY.md
$optimizedContent = "# MEMORY.md - 长期记忆`n`n这是助手的长期记忆，记录重要的事件、决策和值得记住的信息。`n`n"
foreach ($section in $optimizedSections) {
    $optimizedContent += "## $($section.Title)`n`n$($section.Content)`n`n"
}

# Write optimized MEMORY.md
Set-Content -Path $MemoryFile -Value $optimizedContent -Encoding UTF8
Write-Host "MEMORY.md optimized successfully!" -ForegroundColor Green

# Show summary
Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "- Sections: $($optimizedSections.Count)" -ForegroundColor White
Write-Host "- Total size: $($optimizedContent.Length) bytes" -ForegroundColor White