---
name: fund-challenge-instrument-rules
description: Instrument-level trading rule resolver for the 1000 CNY fund challenge. Use ONLY in challenge mode to enforce per-fund subscription/redemption limits, cutoff windows, T+n confirmation, and cash availability constraints before issuing actions.
---

# Fund Challenge Instrument Rules

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Purpose

Prevent non-executable orders by enforcing per-instrument and per-platform constraints.

## Inputs

- `fund_challenge/instrument_rules.json`
- Proposed action set (BUY/HOLD/REDEEM/SWITCH)
- Current timestamp (Asia/Shanghai)

## Mandatory checks per action

1. Fund-level buyability (open/paused/limit amount).
2. Fund-level redeemability and lock period constraints.
3. Platform-level cutoff (Alipay / TiantianFund) applicability.
4. Confirmation timeline (T+N confirm) and cash timeline (T+N settle).
5. Whether resulting cash can be reused for same-day or next-day operation.

## Output

- `EXECUTABLE` or `NON_EXECUTABLE`
- Earliest submit time
- Earliest effective date
- Earliest cash available date
- Fallback action (default HOLD)

## Hard rule

If rule data is missing for any target instrument, block trade and return `DECISION_ABORTED_UNVERIFIED_DATA`.
