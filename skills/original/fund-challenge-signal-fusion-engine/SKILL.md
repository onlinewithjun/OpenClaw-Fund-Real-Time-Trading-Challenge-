---
name: fund-challenge-signal-fusion-engine
description: Aggressive short-term signal fusion engine for challenge mode. Use only for challenge tasks to combine policy/news, sector heat, and macro-linked signals into ranked opportunities.
---

# Fund Challenge Signal Fusion Engine

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Signal buckets

- Policy and regulatory news impulse
- Sector/theme heat and momentum proxy
- Macro linkage (gold, metals, FX, rates) for current holdings
- Liquidity feasibility for off-exchange execution

## Scoring model

Score each candidate 0-100 by weighted dimensions:

- Catalyst strength
- Momentum persistence
- Execution feasibility
- Drawdown vulnerability

## Requirements

- Use only verified and timestamped data.
- Prefer same-day evidence where available.
- If confidence is weak, output HOLD rather than forcing a trade.
