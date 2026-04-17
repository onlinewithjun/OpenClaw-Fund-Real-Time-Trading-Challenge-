$body = @{
    chat_id = "7107266459"
    text = "晨报测试 - 此bot可用 ??? (无代理)"
} | ConvertTo-Json -Compress

$utf8 = [System.Text.Encoding]::UTF8
$bytes = $utf8.GetBytes($body)

$old_proxy = $env:HTTP_PROXY
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""
$env:NO_PROXY = "*"
$env:no_proxy = "*"

try {
    Invoke-RestMethod -Uri "https://api.telegram.org/bot8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY/sendMessage" -Method POST -ContentType "application/json; charset=utf-8" -Body $bytes -TimeoutSec 15 -Proxy "" -ProxyUseDefaultCredentials
    Write-Output "SUCCESS"
} catch {
    Write-Output "FAILED: $_"
} finally {
    $env:HTTP_PROXY = $old_proxy
}
