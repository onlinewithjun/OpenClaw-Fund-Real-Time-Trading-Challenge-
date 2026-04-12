# Local Search Alternative for OpenClaw Memory
# This script provides a simple grep-like search for memory files

param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    
    [string]$MemoryPath = "memory",
    [int]$ContextLines = 2,
    [switch]$CaseSensitive = $false
)

Write-Host "🔍 Searching memory for: '$Query'" -ForegroundColor Green

# Get all memory files
$MemoryFiles = Get-ChildItem -Path $MemoryPath -Filter "*.md" -ErrorAction SilentlyContinue

if ($MemoryFiles.Count -eq 0) {
    Write-Host "⚠️  No memory files found in $MemoryPath" -ForegroundColor Yellow
    return
}

$TotalMatches = 0
$Results = @()

foreach ($File in $MemoryFiles) {
    try {
        $Content = Get-Content $File.FullName -ErrorAction Stop
        $LineNumber = 0
        
        foreach ($Line in $Content) {
            $LineNumber++
            
            # Check if line matches query
            $MatchFound = $false
            if ($CaseSensitive) {
                $MatchFound = $Line -match [regex]::Escape($Query)
            } else {
                $MatchFound = $Line -match "(?i)$([regex]::Escape($Query))"
            }
            
            if ($MatchFound) {
                $TotalMatches++
                
                # Get context lines
                $StartLine = [Math]::Max(0, $LineNumber - $ContextLines - 1)
                $EndLine = [Math]::Min($Content.Length, $LineNumber + $ContextLines)
                
                $Context = @()
                for ($i = $StartLine; $i -lt $EndLine; $i++) {
                    $ContextLine = $Content[$i]
                    if ($i + 1 -eq $LineNumber) {
                        $Context += ">>> $ContextLine"
                    } else {
                        $Context += "    $ContextLine"
                    }
                }
                
                $Result = [PSCustomObject]@{
                    File = $File.Name
                    LineNumber = $LineNumber
                    Context = $Context -join "`n"
                    Relevance = 1.0  # Simple relevance scoring
                }
                $Results += $Result
            }
        }
    }
    catch {
        Write-Host "⚠️  Error reading $($File.Name): $_" -ForegroundColor Yellow
    }
}

# Display results
if ($TotalMatches -eq 0) {
    Write-Host "❌ No matches found for '$Query'" -ForegroundColor Red
} else {
    Write-Host "✅ Found $TotalMatches match(es) in $($Results.Count) file(s)" -ForegroundColor Green
    
    # Sort by relevance (simple sorting by file date for now)
    $SortedResults = $Results | Sort-Object { [DateTime]::ParseExact($_.File.Substring(0, 10), "yyyy-MM-dd", $null) } -Descending
    
    foreach ($Result in $SortedResults) {
        Write-Host "`n📄 File: $($Result.File) (Line $($Result.LineNumber))" -ForegroundColor Cyan
        Write-Host $Result.Context
    }
}

Write-Host "`n💡 Tip: Use quotes for multi-word searches, e.g., '.\local-search.ps1 \"system status\"'" -ForegroundColor Gray