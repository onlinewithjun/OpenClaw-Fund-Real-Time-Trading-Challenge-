$env:PYTHONIOENCODING = "utf-8"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$token = "[REDACTED - Telegram bot token - REQUIRES ROTATION]"
$chat_id = "7107266459"

$text = Get-Content "C:\Users\Administrator\.openclaw\workspace\temp\review_text.txt" -Raw -Encoding UTF8

$body = @{
    chat_id = $chat_id
    text = $text
} | ConvertTo-Json -Compress

$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
$result = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" `
    -Method Post `
    -ContentType "application/json; charset=utf-8" `
    -Body $bytes

if ($result.ok -eq $true) {
    Write-Host "SENT OK: message_id = $($result.result.message_id)"
} else {
    Write-Host "SEND FAILED: $($result | ConvertTo-Json)"
}
