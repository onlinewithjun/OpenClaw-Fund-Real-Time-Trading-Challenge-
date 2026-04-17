$env:PYTHONIOENCODING = "utf-8"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$state = Get-Content "C:\Users\Administrator\.openclaw\workspace\fund_challenge\state.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$holdings = $state.holdings
$cash = $state.cash
$asOf = $state.asOf
$pending = $state.pendingTransactions

Write-Host "asOf: $asOf"
Write-Host "cash: $cash"

Write-Host "=== HOLDINGS ==="
foreach ($h in $holdings) {
    $code = $h.code
    $name = $h.name
    $mv = $h.marketValue
    $upnl = $h.unrealizedPnl
    Write-Host "$code | $name | MV=$mv | UPnL=$upnl"
}

Write-Host "=== PENDING ==="
Write-Host ($pending | ConvertTo-Json -Depth 5)
