---
name: fund-challenge-market-calendar-gate
description: Trading-day and cut-off gate for the fund challenge. Use only in challenge mode to validate trading calendar, execution windows, and market timing constraints before any decision.
---

# Fund Challenge Market Calendar Gate

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Purpose

Prevent invalid actions on non-trading days or after execution cut-off.

## Mandatory checks

- Validate Shanghai timezone date/time.
- Validate if current date is trading day for off-exchange fund operations.
- Validate time bucket (pre-close actionable vs post-close review).
- Enforce explicit execution deadline in final instruction.

## Output

- `TRADING_DAY_OK` or `TRADING_DAY_BLOCKED`
- Cut-off timestamp
- Allowed action type set for current time window

## Block conditions

If non-trading day or deadline passed, return no-trade guidance and stop decision flow.
