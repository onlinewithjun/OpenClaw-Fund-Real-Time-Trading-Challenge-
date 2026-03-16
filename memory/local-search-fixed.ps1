param(
    [Parameter(Mandatory=$true)]
    [string]$SearchTerm,
    
    [string]$MemoryPath = "C:\Users\Administrator\.openclaw\workspace\memory",
    
    [int]$ContextLines = 2
)

Write-Host "🔍 Searching memory for: '$SearchTerm'" -ForegroundColor Cyan

# Check if memory directory exists
if (-not (Test-Path $MemoryPath)) {
    Write-Host "⚠️  Memory directory not found: $MemoryPath" -ForegroundColor Yellow
    return
}

# Get all markdown files in memory directory
$MemoryFiles = Get-ChildItem -Path $MemoryPath -Filter "*.md" -File

if ($MemoryFiles.Count -eq 0) {
    Write-Host "⚠️  No memory files found in $MemoryPath" -ForegroundColor Yellow
    return
}

$MatchCount = 0
$FileCount = 0

foreach ($File in $MemoryFiles) {
    $FileCount++
    $Content = Get-Content $File.FullName -Raw
    $Lines = $Content -split "`n"
    
    # Search for matches
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -like "*$SearchTerm*") {
            if ($MatchCount -eq 0) {
                Write-Host "`n📄 Found matches:" -ForegroundColor Green
            }
            
            $MatchCount++
            
            # Show context
            $StartLine = [Math]::Max(0, $i - $ContextLines)
            $EndLine = [Math]::Min($Lines.Count - 1, $i + $ContextLines)
            
            Write-Host "`n--- Match $MatchCount in $($File.Name) ---" -ForegroundColor Yellow
            for ($j = $StartLine; $j -le $EndLine; $j++) {
                if ($j -eq $i) {
                    Write-Host ">> $($Lines[$j])" -ForegroundColor Red
                } else {
                    Write-Host "   $($Lines[$j])"
                }
            }
        }
    }
}

if ($MatchCount -eq 0) {
    Write-Host "❌ No matches found for '$SearchTerm'" -ForegroundColor Red
} else {
    Write-Host "`n✅ Found $MatchCount match(es) in $FileCount file(s)" -ForegroundColor Green
}

Write-Host "`n💡 Tip: Use specific terms like 'qmd', 'compaction', 'telegram' for better results" -ForegroundColor Gray