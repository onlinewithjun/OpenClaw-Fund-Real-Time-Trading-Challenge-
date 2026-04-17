$env:PYTHONIOENCODING = "utf-8"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$token = "[REDACTED - Telegram bot token - REQUIRES ROTATION]"
$chat_id = "7107266459"

$text = @"
📋 【基金挑战#15 · 2026-04-16 收盘复盘】

✅ 结论
挑战第42天，组合账面 PV 1115.79，浮盈 +151.36，距目标 2000 还差 884.21。系统无在途单，无机械阻塞，链路完整。

---
📊 持仓表现

| 代码 | 名称 | 持仓金额 | 持仓盈亏 |
|------|------|---------|---------|
| 020899 | 天弘中证全指通信设备指数发起 A | 245.58 | +74.82 ✅ |
| 000056 | 建信消费升级混合 | 124.25 | +46.31 ✅ |
| 017192 | 天弘中证工业有色金属主题 ETF 发起联接 A | 92.58 | +37.32 ✅ |
| 002611 | 博时黄金 ETF 联接 C | 178.25 | -7.09 ⚠️ |

组合账面 PV：1115.79 | 现金：475.13 | UPnL：+151.36 | Gap：884.21
同质化检查：002611 vs 020899 重合 0 只，0.0%（组合无内部重叠）

贡献结构：最强 020899(+74.82)，最弱 002611(-7.09)

---
📉 回撤分析

当前组合风险敞口：
- 最大拖累：002611（博时黄金）持仓 178.25，微亏 -7.09；黄金短期受美元/美债压制，短期或持续偏弱
- 最大驱动：020899（通信设备）持仓 245.58，贡献 +74.82；今日 A 股创业板 +3.17%，科技通信主线明确，量能2.35万亿健康

回撤容忍线：组合 PV 1115.79，若单日回撤 5% 约 -55.8；现金 475.13 提供约 42% 安全垫

仓位集中度偏高（TOP1 仓位 22%），单品种波动放大组合振幅

---
🔁 今日操作回顾

✅ 21:45 收盘复盘链路正常：state asOf 2026-04-16T21:45:42（当日有效）
✅ pendingTransactions = 0，无在途单，无阻塞
✅ 分步执行（state_refresh → review_summary）链路稳定
✅ 综合评分：Macro 30% / Sentiment 25% / Sector 25% / Quant 20% 框架沿用

---
🔍 次日观察清单

- 020899（通信设备）▲：创业板今日 +3.17% 强势，次日观察能否持续；放量冲高则控追涨
- 017192（工业有色金属）▲：资源类跟涨，跟踪大宗商品联动
- 002611（博时黄金）▼：金价短期承压，若持仓拖累扩大可考虑降权
- 000056（消费升级）：跟踪消费数据，边际变化决定去留
- 组合现金 475.13：明日若出现合适买点，有充足子弹
- 14:20 state_refresh 关注 asOf 校验，防止数据落后

---
⚠️ 风险提示

- 创业板指今日 +3.17% 再刷近11年新高，技术性回调风险升温；集中科技仓位的 020899 面临高波动
- 仓位集中度偏高（单品种 22%），建议关注组合层面回撤控制
- 黄金受美元/美债压制，短期 002611 偏弱概率大
- 本复盘为系统自动生成，不构成投资建议；请在支付宝/实际购买页面再次确认

---
🔧 系统状态
STATE_REFRESH_OK asOf=2026-04-16T21:45:42+08:00
"@

$body = @{
    chat_id = $chat_id
    text = $text
    parse_mode = "HTML"
} | ConvertTo-Json -Compress

$result = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" `
    -Method Post `
    -ContentType "application/json; charset=utf-8" `
    -Body ([System.Text.Encoding]::UTF8.GetBytes($body))

if ($result.ok -eq $true) {
    Write-Host "SENT OK: message_id = $($result.result.message_id)"
} else {
    Write-Host "SEND FAILED: $($result | ConvertTo-Json)"
}
"@