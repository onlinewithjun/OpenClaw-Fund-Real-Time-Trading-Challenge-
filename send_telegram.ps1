$token = $env:TELEGRAM_BOT_TOKEN
if (-not $token) {
    Write-Host "TELEGRAM_BOT_TOKEN not set"
    exit 1
}

$body = @{
    chat_id = 7107266459
    text = "📊 基金挑战#05 State Refresh

✅ STATUS: STATE_REFRESH_OK
🕐 2026-04-13 14:20:34 +08:00"
}

try {
    $response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "SUCCESS: Message sent"
    Write-Host $response
} catch {
    Write-Host "ERROR: $_"
    Write-Host $_.Exception.Message
}
