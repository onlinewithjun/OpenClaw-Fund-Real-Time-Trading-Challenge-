---
name: fund-challenge-orchestrator
description: Master orchestrator for the 1000 CNY aggressive fund challenge workflow. Use ONLY when context explicitly indicates challenge mode ("基金实盘挑战", "1000元挑战", or cron jobs named "基金实盘 - ..."). Not for normal long-term investing conversations.
---

# Fund Challenge Orchestrator

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Scope lock

- Activate only for challenge-mode tasks.
- If request is normal investing advice, stop using this skill stack.

## Required sub-skills order

1. fund-challenge-market-calendar-gate
2. fund-challenge-identity-freshness-guard
3. fund-challenge-signal-fusion-engine
4. fund-challenge-position-risk-engine
5. fund-challenge-offexchange-exec-sim
6. fund-challenge-ledger-postmortem

## Global hard constraints

- Read `fund_challenge/state.json` first.
- Use `python fund_challenge/scripts/state_math.py --state fund_challenge/state.json` for all numbers.
- If any key data is unverifiable: output `DECISION_ABORTED_UNVERIFIED_DATA`.
- BUY actions require explicit user confirmation before state update.
- Never reset challenge progress implicitly.

## Decision output contract

1. Challenge Day + Timestamp
2. State Snapshot
3. Data Freshness Check
4. Verified Fund Universe
5. Decision (primary + fallback)
6. Execution Window and T+ constraints
7. Risk Controls
8. Post-trade State Delta (only after user confirmation)
