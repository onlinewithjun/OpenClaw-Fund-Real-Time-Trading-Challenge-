#!/usr/bin/env python3
"""Mark 020899 pending transaction as FAILED per user confirmation."""
import json
from datetime import datetime

state_path = 'fund_challenge/state.json'

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

updated = False
for tx in state['pendingTransactions']:
    if tx['code'] == '020899' and tx['status'] == 'PENDING_CONFIRM':
        tx['status'] = 'FAILED'
        tx['note'] = tx['note'] + ' | 用户确认买入失败于 2026-03-23 14:50'
        tx['resolvedAt'] = '2026-03-23T14:50:00+08:00'
        print(f"Updated transaction {tx['id']} to FAILED")
        updated = True

if not updated:
    print("No matching PENDING_CONFIRM transaction found for 020899")
else:
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("State updated successfully")
