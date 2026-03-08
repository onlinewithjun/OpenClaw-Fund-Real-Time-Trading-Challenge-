---
name: fund-challenge-data-guard
description: Data integrity and anti-hallucination guardrail for the aggressive fund challenge. Use ONLY for challenge jobs mentioning "基金实盘挑战" or "基金实盘 -" schedules. Enforce code-name matching, freshness checks, and source-cited evidence.
---

# Fund Challenge Data Guard

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Purpose

Prevent wrong fund IDs, stale data, arithmetic drift, and fabricated numbers.

## Mandatory checks

### 1) Fund identity check (strict)

For each fund used in decision:

- Query with web search pattern: `"<code> <fund_name> 天天基金网"`
- Query with reverse pattern: `"<fund_name> 基金代码 天天基金"`
- Accept only if code and Chinese name match in at least one authoritative listing.
- If mismatch or ambiguity: mark fund `INVALID_FOR_TRADE`.

### 2) Freshness check

- Capture timestamp for each market datum.
- Mark as stale if timestamp is older than latest market close context.
- Do not use stale inputs for aggressive rotation decisions.

### 3) Numeric verification

- All PnL, position ratio, and target-gap numbers must come from script output.
- If manual number appears in output, reject and recompute.

### 4) Source citation

Each critical fact must include a source line in decision notes:

- `Source: <site/url> @ <timestamp>`

### 5) Abort policy

Immediately abort decision with `DECISION_ABORTED_UNVERIFIED_DATA` if any of below occurs:

- Code-name mismatch
- Missing timestamp
- Unverifiable NAV/price proxy
- Script calculation error

## Recommended signal buckets (challenge mode only)

- Policy/news impulse (same-day)
- Sector heat and volume proxy
- Commodity/FX macro impulse relevant to holding theme
- Liquidity and redemption-window feasibility

## Non-goals

- Do not provide long-term diversified allocation advice.
- Do not make personal wealth planning recommendations.
