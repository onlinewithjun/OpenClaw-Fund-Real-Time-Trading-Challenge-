# OpenClaw Memory Compaction Script (Fixed)
# Aggressively compacts daily memory files to save tokens

param(
    [int]$MaxFileSizeKB = 2,
    [bool]$DryRun = $false
)

$MemoryPath = "C:\Users\Administrator\.openclaw\workspace\memory"
$MaxFileSizeBytes = $MaxFileSizeKB * 1024

# Get all daily memory files
$MemoryFiles = Get-ChildItem -Path $MemoryPath -Filter "2026-*.md" | Sort-Object Name

Write-Host "🚀 Starting Daily Memory Compaction..."
Write-Host "Memory Path: $MemoryPath"
Write-Host "Max file size: $($MaxFileSizeKB)KB"
Write-Host "Dry run: $DryRun"
Write-Host ""

foreach ($File in $MemoryFiles) {
    $FileSizeKB = [Math]::Round($File.Length / 1024, 1)
    
    if ($File.Length -gt $MaxFileSizeBytes) {
        Write-Host "⚠️  File too large: $($File.Name) ($($FileSizeKB)KB)"
        
        if (-not $DryRun) {
            try {
                # Read the file content
                $Content = Get-Content -Path $File.FullName -Raw
                
                # Extract only essential sections
                # Keep: 时间线, 关键事件, 结论, 系统状态更新
                $EssentialSections = @()
                
                # Split by sections (## headers)
                $Sections = $Content -split "(?m)^## "
                
                foreach ($Section in $Sections) {
                    if ($Section -match "^(时间线|关键事件|结论|系统状态更新|重要发现|优化结果)") {
                        $EssentialSections += "## $Section"
                    }
                }
                
                if ($EssentialSections.Count -gt 0) {
                    $CompactedContent = $EssentialSections -join "`n`n"
                    
                    # Add header if needed
                    if (-not $CompactedContent.StartsWith("#")) {
                        $DatePart = $File.Name.Replace(".md", "")
                        $CompactedContent = "# $DatePart`n`n" + $CompactedContent
                    }
                    
                    # Write compacted content back to file
                    Set-Content -Path $File.FullName -Value $CompactedContent -Encoding UTF8
                    $NewSizeKB = [Math]::Round((Get-Item $File.FullName).Length / 1024, 1)
                    Write-Host "✅ Compacted: $($File.Name) ($($FileSizeKB)KB → $($NewSizeKB)KB)"
                } else {
                    Write-Host "❌ No essential sections found in: $($File.Name)"
                }
            }
            catch {
                Write-Host "❌ Error processing $($File.Name): $($_.Exception.Message)"
            }
        }
    } else {
        Write-Host "✅ File within limits: $($File.Name) ($($FileSizeKB)KB)"
    }
}

Write-Host ""
Write-Host "📊 Compaction completed!"