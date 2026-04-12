# Optimized Memory Search Script for OpenClaw
# This script provides efficient memory retrieval with token optimization

param(
    [string]$Query = "",
    [int]$MaxResults = 5,
    [string]$OutputFormat = "compact"  # compact, detailed, or minimal
)

# Function to search using qmd (if available)
function Search-WithQMD {
    param($searchQuery, $maxResults)
    
    try {
        # Use WSL to run qmd search
        $qmdResult = wsl node /home/lizhuojun/node_modules/@tobilu/qmd/dist/qmd.js search --collection workspace --query "$searchQuery" --limit $maxResults
        
        if ($qmdResult) {
            return $qmdResult
        }
    }
    catch {
        Write-Host "QMD search failed: $_"
    }
    
    return $null
}

# Function to fallback to basic file search
function Search-WithBasic {
    param($searchQuery, $maxResults)
    
    $results = @()
    $memoryFiles = Get-ChildItem -Path "memory/*.md" -File | Sort-Object LastWriteTime -Descending
    
    foreach ($file in $memoryFiles) {
        if ($results.Count -ge $maxResults) { break }
        
        $content = Get-Content $file.FullName -Raw
        if ($content -match [regex]::Escape($searchQuery)) {
            $context = Get-ContextSnippet -Content $content -Query $searchQuery -Length 200
            $results += @{
                File = $file.Name
                Score = 0.8  # Basic match
                Context = $context
                Date = $file.LastWriteTime.ToString("yyyy-MM-dd")
            }
        }
    }
    
    return $results
}

# Function to extract context snippet
function Get-ContextSnippet {
    param($Content, $Query, $Length = 200)
    
    $index = $Content.IndexOf($Query)
    if ($index -eq -1) { return $Content.Substring(0, [Math]::Min($Length, $Content.Length)) }
    
    $start = [Math]::Max(0, $index - ($Length / 2))
    $end = [Math]::Min($Content.Length, $start + $Length)
    
    return $Content.Substring($start, $end - $start)
}

# Function to format results based on output format
function Format-Results {
    param($results, $format)
    
    switch ($format) {
        "minimal" {
            $output = ""
            foreach ($result in $results) {
                if ($result.File) {
                    $output += "- $($result.Date): $($result.Context)`n"
                } else {
                    $output += "- $result`n"
                }
            }
            return $output.Trim()
        }
        "compact" {
            $output = ""
            foreach ($result in $results) {
                if ($result.File) {
                    $output += "📄 $($result.Date) ($($result.File)): $($result.Context)`n"
                } else {
                    $output += "- $result`n"
                }
            }
            return $output.Trim()
        }
        "detailed" {
            $output = ""
            foreach ($result in $results) {
                if ($result.File) {
                    $output += "=== $($result.Date) ===`nFile: $($result.File)`nScore: $($result.Score)`nContext: $($result.Context)`n`n"
                } else {
                    $output += "- $result`n"
                }
            }
            return $output.Trim()
        }
    }
}

# Main execution
if ([string]::IsNullOrEmpty($Query)) {
    Write-Host "Usage: .\optimized-memory-search.ps1 -Query 'search term' -MaxResults 5 -OutputFormat compact"
    exit 1
}

Write-Host "🔍 Searching memory for: '$Query'..."

# Try QMD first (most efficient)
$results = Search-WithQMD -searchQuery $Query -maxResults $MaxResults

if (-not $results) {
    Write-Host "⚠️  QMD not available, falling back to basic search..."
    $results = Search-WithBasic -searchQuery $Query -maxResults $MaxResults
}

if ($results.Count -eq 0) {
    Write-Host "❌ No results found for: '$Query'"
    exit 0
}

# Format and display results
$formattedResults = Format-Results -results $results -format $OutputFormat
Write-Host "`n✅ Found $($results.Count) result(s):`n"
Write-Host $formattedResults

# Token optimization tip
$totalChars = $formattedResults.Length
$estimatedTokens = [Math]::Ceiling($totalChars / 4)
Write-Host "`n💡 Token estimate: ~$estimatedTokens tokens (saved by using compact format)"