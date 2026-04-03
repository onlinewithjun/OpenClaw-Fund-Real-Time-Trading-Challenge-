#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
手动修复 state.json - 根据用户提供的支付宝截图数据更新状态
执行时间：2026-03-30 14:45
"""

import json
from pathlib import Path
from datetime import datetime

STATE_FILE = Path(__file__).parent.parent / "state.json"

# 用户提供的实际数据 (2026-04-01 14:53)
ACTUAL_DATA = {
    "asOf": "2026-04-01T14:53:00+08:00",
    "cash": "363.00",
    "totalAsset": "929.67",
    "holdings": [
        {
            "code": "002611",
            "name": "博时黄金 ETF 联接 C",
            "marketValue": "346.93",
            "unrealizedPnl": "-39.07",
            "returnRate": "-10.11%",
        },
        {
            "code": "020899",
            "name": "天弘中证全指通信设备指数发起 A",
            "marketValue": "165.80",
            "unrealizedPnl": "-8.04",
            "returnRate": "-4.63%",
        },
        {
            "code": "017192",
            "name": "天弘中证工业有色金属主题 ETF 发起联接 A",
            "marketValue": "53.94",
            "unrealizedPnl": "0.00",
            "returnRate": "--",
        },
    ],
}

def load_nav(code: str) -> str:
    """从 candidates.json 获取最新净值"""
    candidates_file = Path(__file__).parent.parent / "candidates.json"
    if not candidates_file.exists():
        return "1.0000"
    
    with open(candidates_file, "r", encoding="utf-8") as f:
        candidates = json.load(f)
    
    for fund in candidates.get("funds", []):
        if fund.get("code") == code:
            return str(fund.get("nav", "1.0000"))
    
    return "1.0000"

def calculate_shares(market_value: float, nav: str) -> float:
    """根据市值和净值估算份额"""
    try:
        nav_float = float(nav)
        if nav_float > 0:
            return round(market_value / nav_float, 2)
    except:
        pass
    return 0.0

def fix_state():
    # 加载现有 state
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
    
    # 更新 asOf 和现金
    state["asOf"] = ACTUAL_DATA["asOf"]
    state["cash"] = ACTUAL_DATA["cash"]
    
    # 更新持仓
    new_holdings = []
    for holding in ACTUAL_DATA["holdings"]:
        code = holding["code"]
        nav = load_nav(code)
        market_value = float(holding["marketValue"])
        shares = calculate_shares(market_value, nav)
        
        # 保留原有的 costBasisUnit（如果存在）
        existing = next((h for h in state["holdings"] if h["code"] == code), None)
        cost_basis = existing["costBasisUnit"] if existing else nav
        
        new_holdings.append({
            "code": code,
            "name": holding["name"],
            "latestNav": nav,
            "costBasisUnit": cost_basis,
            "shares": str(shares),
            "totalShares": str(shares),
            "availableShares": str(shares),
            "marketValue": str(market_value),
            "unrealizedPnl": holding["unrealizedPnl"],
            "settlementRule": "T+1_confirm_T+1_settle",
        })
    
    state["holdings"] = new_holdings
    
    # 清理过期的 pending 交易
    # 保留 PENDING_CONFIRM 和 PENDING_SETTLE 状态的
    # 清理已过期（超过预期确认日 3 天以上）的
    cleaned_pending = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    for pending in state.get("pendingTransactions", []):
        status = pending.get("status", "")
        expected_confirm = pending.get("expectedConfirmDate", "")
        
        # 保留未完成的
        if status in ["PENDING_CONFIRM", "PENDING_SETTLE"]:
            cleaned_pending.append(pending)
        # 保留已完成的（用于历史）
        elif status in ["SETTLED", "CANCELLED"]:
            cleaned_pending.append(pending)
    
    # 特别处理：017192 的 3 月 27 日买入单，如果实际已确认，应该标记为 SETTLED
    for pending in cleaned_pending:
        if pending.get("code") == "017192" and pending.get("actionType") == "BUY":
            if pending.get("status") == "PENDING_CONFIRM":
                # 检查预期确认日是否已过
                if pending.get("expectedConfirmDate", "") < "2026-03-30":
                    # 实际已持仓，标记为已确认
                    pending["status"] = "SETTLED"
                    pending["resolvedAt"] = f"{today}T14:45:00+08:00"
                    pending["note"] = pending.get("note", "") + " | 手动修复于 2026-03-30 14:45"
    
    state["pendingTransactions"] = cleaned_pending
    
    # 更新 notes
    state["notes"] = f"手动修复于 2026-03-30 14:45 | 数据源：用户支付宝截图 (12:50)"
    
    # 写回文件
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    print("[OK] state.json fixed")
    print(f"   asOf: {state['asOf']}")
    print(f"   cash: {state['cash']} CNY")
    print(f"   holdings: {len(state['holdings'])} funds")
    for h in state["holdings"]:
        print(f"     - {h['code']} {h['name']}: {h['marketValue']} CNY ({h['shares']} shares)")

if __name__ == "__main__":
    fix_state()
