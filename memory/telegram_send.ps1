$token = "[REDACTED - Telegram bot token - REQUIRES ROTATION]"
$body = @{
    chat_id = 7107266459
    text = "【基金挑战#07｜14:40定期巡检】

▎状态刷新 ✅
  asOf: 2026-04-13T14:42:11+08:00
  现金: 475.13 CNY
  总仓位: 638.54 CNY
  总资产: 1113.67 CNY

▎持仓明细
  002611 博时黄金 ETF 联接 C
    最新净值: 3.2938 | 成本: 3.4598
    份额: 53.57 | 市值: 176.45 | 浮动盈亏: -8.89
  020899 天弘中证全指通信设备指数发起 A
    最新净值: 3.1070 | 成本: 2.1534
    份额: 79.30 | 市值: 246.39 | 浮动盈亏: +75.62
  017192 天弘中证工业有色金属主题 ETF 发起联接 A
    最新净值: 1.8932 | 成本: 1.1382
    份额: 48.55 | 市值: 91.91 | 浮动盈亏: +36.66
  000056 建信消费升级混合
    最新净值: 1.9060 | 成本: 1.2000
    份额: 64.95 | 市值: 123.79 | 浮动盈亏: +45.85

▎一致性检查 ✅ PASSED
  stateAsOf: 2026-04-13T14:42:11+08:00
  candidatesUpdatedAt: 2026-04-13T14:35:33+08:00
  candidatesCount: 11

▎结论
  数据新鲜度OK，建议保守路径：持仓不动"
    parse_mode = "HTML"
}

$json = ConvertTo-Json -InputObject $body -Compress
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$uri = "https://api.telegram.org/bot$token/sendMessage"
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
Invoke-RestMethod -Uri $uri -Method Post -ContentType "application/json" -Body $bytes