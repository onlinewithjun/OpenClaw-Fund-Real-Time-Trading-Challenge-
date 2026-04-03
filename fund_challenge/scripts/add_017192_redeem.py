#!/usr/bin/env python3
"""Mark 017192 as redeemed and update state."""
import json

state_path = 'fund_challenge/state.json'

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

# Add redeem transaction for 017192
redeem_tx = {
    "id": "act-20260323-145200",
    "createdAt": "2026-03-23T14:52:00+08:00",
    "actionType": "REDEEM",
    "code": "017192",
    "name": "天弘中证工业有色金属主题 ETF 发起联接 A",
    "shares": "21.54",
    "amountCny": "38.18",
    "status": "PENDING_CONFIRM",
    "note": "用户手动卖出于 2026-03-23 14:52 | 15:00 前提交",
    "expectedConfirmDate": "2026-03-24",
    "expectedSettleDate": "2026-03-25"
}

state['pendingTransactions'].append(redeem_tx)
print(f"Added redeem transaction for 017192")

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("State updated successfully")
