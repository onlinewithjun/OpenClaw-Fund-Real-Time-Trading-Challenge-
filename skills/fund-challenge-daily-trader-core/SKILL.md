---
name: fund-challenge-daily-trader-core
description: End-to-end daily workflow for the 1000 CNY aggressive off-exchange fund challenge. Use ONLY when the task explicitly references "基金实盘挑战", "1000元挑战", or cron jobs named "基金实盘 - ...". Never use this skill for normal long-term investment advice.
---

# Fund Challenge Daily Trader Core

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Enforce scope

- Activate only in challenge mode.
- If user asks regular wealth management/investing, do not use this skill.

## Mission

Operate as an aggressive short-term trader for a 6-month 1000 CNY doubling challenge on Alipay/Tiantian Fund, with strict anti-hallucination and state-first execution.

## Mandatory daily pipeline

1. Load state from `fund_challenge/state.json`.
2. Check market calendar (trading day yes/no).
3. If non-trading day: publish "No trade" + next checkpoint; do not fabricate signals.
4. Verify latest data timestamp for each holding and candidate sector (must be same-day or latest available market close with explicit timestamp).
5. Run fund code-name verification workflow (read `../fund-challenge-data-guard/SKILL.md`).
6. Run arithmetic via script (`python fund_challenge/scripts/state_math.py`) and never do manual math in prose.
7. Generate one action set only:
   - BUY (manual confirmation required)
   - HOLD
   - REDEEM / SWITCH
8. Apply off-exchange constraints check (T+1/T+2/T+n lock and confirm windows).
9. If any key number is unverifiable, stop and output `DECISION_ABORTED_UNVERIFIED_DATA`.
10. Send Telegram instruction before 15:00 Asia/Shanghai.
11. Wait for user execution confirmation, then update state ledger.

## Output contract (challenge mode)

Always output these sections in order:

1. `Challenge Day` and `Timestamp (Asia/Shanghai)`
2. `State Snapshot` (cash, holdings MV, unrealized PnL, distance to target)
3. `Data Freshness Check`
4. `Verified Universe` (fund code-name pairs)
5. `Decision` (single primary action + optional contingency)
6. `Execution Window` (deadline + T+ constraints)
7. `Risk Controls` (stop-loss/take-profit triggers)
8. `Post-Trade State Delta` (only if user confirms execution)

## Hard rules

- Never reset challenge progress implicitly.
- Never overwrite yesterday state without a ledger event.
- Never use stale narrative as live market evidence.
- Never output a trade with missing timestamp/source.
- Never bypass the verification skill.

## Files used by this skill

- `fund_challenge/state.json`
- `fund_challenge/ledger.jsonl`
- `fund_challenge/scripts/state_math.py`
- `fund_challenge/checklists/daily-checklist.md`
