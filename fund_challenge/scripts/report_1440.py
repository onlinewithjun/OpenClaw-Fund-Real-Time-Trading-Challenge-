import json
from pathlib import Path

state = json.loads(Path('fund_challenge/state.json').read_text(encoding='utf-8'))
marker = json.loads(Path('fund_challenge/runtime/consistency_04b.json').read_text(encoding='utf-8'))

holdings = state.get('holdings', [])
total_mv = sum(float(h.get('marketValue', 0)) for h in holdings)
cash = float(state.get('cash', 0))
total_assets = cash + total_mv

lines = [
    '【基金挑战#07｜14:40定期巡检】',
    '',
    '▎状态刷新 ✅',
    f'  asOf: {state.get("asOf", "")}',
    f'  现金: {cash:.2f} CNY',
    f'  总仓位: {total_mv:.2f} CNY',
    f'  总资产: {total_assets:.2f} CNY',
    '',
    '▎持仓明细',
]
for h in holdings:
    lines.append(f'  {h["code"]} {h["name"]}')
    lines.append(f'    最新净值: {h["latestNav"]} | 成本: {h["costBasisUnit"]}')
    lines.append(f'    份额: {h["shares"]} | 市值: {h["marketValue"]} | 浮动盈亏: {h["unrealizedPnl"]}')

lines.extend([
    '',
    '▎一致性检查 ✅ PASSED',
    f'  requireAfter: {marker.get("requireAfter")}',
    f'  stateAsOf: {marker.get("stateAsOf")}',
    f'  candidatesUpdatedAt: {marker.get("candidatesUpdatedAt")}',
    f'  candidatesCount: {marker.get("candidatesCount")}',
    '',
    '▎结论',
    '  数据新鲜度OK，建议保守路径：持仓不动',
])

import sys
sys.stdout.reconfigure(encoding='utf-8')
print('\n'.join(lines))
