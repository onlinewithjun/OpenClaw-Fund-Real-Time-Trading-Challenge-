$ErrorActionPreference = 'Stop'
$env:HTTP_PROXY = ''
$env:HTTPS_PROXY = ''
$env:ALL_PROXY = ''
$env:http_proxy = ''
$env:https_proxy = ''
$env:all_proxy = ''
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$body = @{
    chat_id = "7107266459"
    text = "晨报测试 - 此bot可用"
} | ConvertTo-Json -Compress

$utf8 = [System.Text.Encoding]::UTF8
$bytes = $utf8.GetBytes($body)

Invoke-RestMethod -Uri "https://api.telegram.org/bot8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY/sendMessage" -Method POST -ContentType "application/json; charset=utf-8" -Body $bytes -TimeoutSec 15
