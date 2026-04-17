$files = Get-ChildItem 'C:\Users\Administrator\.openclaw\workspace\fund_challenge\scripts\*.py' -ErrorAction SilentlyContinue
foreach ($f in $files) {
    $lines = Get-Content $f.FullName -ErrorAction SilentlyContinue
    $lineNum = 0
    foreach ($line in $lines) {
        $lineNum++
        if ($line -match 'telegram|sendMessage|bot[0-9]') {
            Write-Output "$($f.Name) line $lineNum : $line"
        }
    }
}
