$token = $env:TELEGRAM_BOT_TOKEN
if (-not $token) {
    Write-Host "TELEGRAM_BOT_TOKEN not set"
    exit 1
}

$text = [System.IO.File]::ReadAllText("C:\Users\Administrator\.openclaw\workspace\send_telegram2.ps1", [System.Text.Encoding]::UTF8) | Out-Null

$jsonBody = @{
    chat_id = 7107266459
    text = "📊 基金挑战#05 State Refresh\n\n✅ STATUS: STATE_REFRESH_OK\n🕐 2026-04-13 14:20:34 +08:00"
} | ConvertTo-Json -Compress

$bytes = [System.Text.Encoding]::UTF8.GetBytes($jsonBody)

try {
    $response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -ContentType "application/json; charset=utf-8" -Body $bytes -ErrorAction Stop
    Write-Host "SUCCESS"
    Write-Host ($response | ConvertTo-Json)
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
    $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
    $body = $reader.ReadToEnd()
    $reader.Close()
    Write-Host "Response body: $body"
}
