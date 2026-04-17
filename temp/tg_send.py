#!/usr/bin/env python3
import os, json, urllib.request

for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(k, None)

token = "8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY"
chat_id = "7107266459"

msg = """📊 基金挑战#15 · 2026-04-13 盘后复盘

▎结论
✅ 组合跑赢基准，今日 mark_to_market 净值更新有效；持仓结构尚可，但距离目标 2000CNY 仍有较大 Gap，需持续滚动正向超额收益。

▎组合总览
• 账面 PV：1112.82 CNY
• 今日 UPnL：+148.39 CNY
• 目标 Gap：887.18 CNY（需+79.7%）
• 现金：475.13 CNY（占比42.7%）
• 在途：无（✅）

▎持仓表现
├ 002611 博时黄金ETF联接C 持仓175.60 盈亏-9.74（⚠️最弱）
├ 020899 天弘通信设备指数 持仓246.39 盈亏+75.62（⭐最强）
├ 017192 天弘工业有色金属ETF联接 持仓91.91 盈亏+36.66（表现稳健）
└ 000056 建信消费升级混合 持仓123.79 盈亏+45.85（表现良好）

▎回撤分析
• 最大拖累：002611（-9.74），黄金短期承压；
• 最大驱动：020899（+75.62），通信设备强势贡献；
• 集中度风险：TOP1仓位占比22.1%，冲高回落需警惕；
• 板块轮动对组合波动影响明显。

▎操作复盘
✅ 链路运行稳定，在途单全部清零；
⚠️ 仓位集中度仍偏高，单品波动放大组合回撤；
📌 硬目标：距2026-09-04还剩约5个月，需持续超额收益。

▎次日观察清单
• 017192 是否弱于均值，走弱考虑降权；
• 020899 强势是否延续，冲高回落控追涨；
• 002611 对冲效果评估；
• 现金占比42.7%，满足机动仓需求；
• 14:20 state_refresh 有效性核查。

▎风险提示
⚠️ 本记录仅供内部复盘，不构成投资建议；
⚠️ A股/基金市场波动大，过往收益不代表未来；
⚠️ 操作前请确认支付宝/天天基金最新净值。"""

data = json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode("utf-8")
req = urllib.request.Request(
    "https://api.telegram.org/bot" + token + "/sendMessage",
    data=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        print("OK:", r.read().decode())
except Exception as e:
    print("ERROR:", e)
