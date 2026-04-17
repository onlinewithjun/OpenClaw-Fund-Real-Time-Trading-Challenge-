$body = @{
    chat_id = "7107266459"
    text = "晨报测试 - 此bot可用 ??"
} | ConvertTo-Json -Compress

$utf8 = [System.Text.Encoding]::UTF8
$bytes = $utf8.GetBytes($body)
$content = $utf8.GetString($bytes)

Invoke-RestMethod -Uri "https://api.telegram.org/bot8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY/sendMessage" -Method POST -ContentType "application/json; charset=utf-8" -Body $bytes -TimeoutSec 10
