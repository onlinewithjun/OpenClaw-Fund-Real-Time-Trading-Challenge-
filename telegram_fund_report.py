# -*- coding: utf-8 -*-
"""
生成 Telegram 基金报告
"""

import csv
from datetime import datetime

# 读取结果
results = []
with open('C:/Users/Administrator/.openclaw/workspace/fund_results_20260306.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        results.append(row)

# 计算汇总
total_holding = sum(float(r['holding']) for r in results)
total_daily_profit = sum(float(r['daily_profit']) for r in results)
total_cum_profit = sum(float(r['new_cum_profit']) for r in results)
total_return_pct = (total_cum_profit / total_holding) * 100

# 按类型分组
by_type = {}
for r in results:
    t = r['type']
    if t not in by_type:
        by_type[t] = []
    by_type[t].append(r)

# 生成报告
report = []
report.append("💰 1000 元挑战 - 基金实盘收益更新")
report.append(f"📅 日期：2026 年 3 月 6 日 (周五)")
report.append(f"⏰ 更新时间：20:00 (净值已更新)")
report.append("")
report.append("=" * 40)
report.append("")
report.append("📊 【总览】")
report.append(f"总持仓：¥{total_holding:,.2f}")
report.append(f"当日盈亏：¥{total_daily_profit:+,.2f}")
report.append(f"累计盈亏：¥{total_cum_profit:+,.2f}")
report.append(f"累计收益率：{total_return_pct:+.2f}%")
report.append("")

# 按资产类型展示
report.append("=" * 40)
report.append("")
report.append("📈 【按资产类型】")

for fund_type, funds in sorted(by_type.items()):
    type_holding = sum(float(f['holding']) for f in funds)
    type_daily = sum(float(f['daily_profit']) for f in funds)
    type_cum = sum(float(f['new_cum_profit']) for f in funds)
    type_weight = (type_holding / total_holding) * 100
    
    report.append(f"\n{fund_type} ({type_weight:.1f}%)")
    report.append(f"  持仓：¥{type_holding:,.0f} | 当日：¥{type_daily:+,.0f} | 累计：¥{type_cum:+,.0f}")
    
    for f in sorted(funds, key=lambda x: float(x['daily_profit']), reverse=True):
        code = f['code']
        name = f['name'][:12]
        change = float(f['change_pct'])
        daily = float(f['daily_profit'])
        
        if change > 0:
            arrow = "📈"
        elif change < 0:
            arrow = "📉"
        else:
            arrow = "➖"
        
        report.append(f"  {arrow} {name} ({code}): {change:+.2f}% | ¥{daily:+,.0f}")

report.append("")
report.append("=" * 40)
report.append("")
report.append("💡 【今日点评】")

# 找出表现最好和最差的
best = max(results, key=lambda x: float(x['change_pct']))
worst = min(results, key=lambda x: float(x['change_pct']))

report.append(f"🏆 最佳：{best['name']} ({best['code']}) {float(best['change_pct']):+.2f}%")
report.append(f"📉 最差：{worst['name']} ({worst['code']}) {float(worst['change_pct']):+.2f}%")

if total_daily_profit > 0:
    report.append(f"✅ 今日盈利 {total_daily_profit:+,.2f} 元，继续加油！")
else:
    report.append(f"⚠️ 今日亏损 {total_daily_profit:+,.2f} 元，长期持有不动摇！")

report.append("")
report.append("_注：QDII 基金 T+1/T+2 确认，部分净值可能延迟更新_")

# 输出报告
report_text = "\n".join(report)
import sys
sys.stdout.buffer.write(report_text.encode('utf-8'))

# 保存到文件
with open('C:/Users/Administrator/.openclaw/workspace/telegram_report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)
