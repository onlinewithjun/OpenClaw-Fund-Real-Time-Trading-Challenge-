$files = Get-ChildItem 'C:\Users\Administrator\.openclaw\workspace\fund_challenge\' -Recurse -File -Include '*.py','*.ps1' -ErrorAction SilentlyContinue
foreach ($f in $files) {
    $lines = Get-Content $f.FullName -ErrorAction SilentlyContinue
    $lineNum = 0
    foreach ($line in $lines) {
        $lineNum++
        if ($line -match 'telegram|sendMessage|7107266459') {
            Write-Output "$($f.FullName) line $lineNum : $line"
        }
    }
}
