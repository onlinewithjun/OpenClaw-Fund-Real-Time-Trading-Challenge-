---
name: fund-challenge-execution-engine
description: Execution and risk engine for short-term aggressive off-exchange fund operations in the 1000 CNY challenge. Use ONLY when challenge context is explicit ("基金实盘挑战" / scheduled "基金实盘 - ..." jobs). Not for general investing conversations.
---

# Fund Challenge Execution Engine

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Objective

Convert verified signals into executable, constraint-aware daily actions with strict stop rules.

## Execution model

1. Ingest verified state and evidence.
2. Score opportunities (0-100) by momentum, catalyst, liquidity feasibility, and drawdown risk.
3. Select max 1 primary trade action for the day.
4. Size position by aggressive ladder:
   - High confidence: 35%–55% incremental exposure
   - Medium: 20%–35%
   - Low: 0% (hold)
5. Attach stop-loss / take-profit conditions.
6. Produce user instruction text optimized for Telegram execution.

## Off-exchange constraints (must simulate)

- T+1/T+2 confirmation and settlement lag must be explicitly modeled.
- Same-day frequent in/out assumptions are prohibited.
- Redemption cash availability date must be shown before recommending reuse.
- Switch operations must check platform execution cutoff.

## Default challenge risk rules

- Single-day max additional exposure: 55%
- Single-theme concentration cap: 60%
- Forced de-risk trigger: portfolio drawdown <= -8% from challenge start
- Soft take-profit: trim when single leg gain >= +7% in short window
- Hard cut: reduce when single leg loss <= -5% unless catalyst strengthened with verified data

## Telegram instruction template

`[Action] [Fund code + full name] [Amount CNY] [Reason in 1 line] [Must execute before HH:MM Asia/Shanghai] [If not executed, fallback]`

## Post-execution protocol

- Update `ledger.jsonl` only after user confirms completion.
- Recompute state with script; persist new snapshot.
- Append audit note with source timestamps and decision id.
