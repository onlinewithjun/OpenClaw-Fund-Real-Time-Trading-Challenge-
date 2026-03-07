---
name: fund-challenge-position-risk-engine
description: Position sizing and risk control engine for the aggressive 1000 CNY challenge. Use only in challenge mode to compute exposure, concentration, stop-loss, and take-profit actions.
---

# Fund Challenge Position Risk Engine

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Position sizing bands

- High confidence: +35% to +55% incremental exposure
- Medium confidence: +20% to +35%
- Low confidence: 0% (HOLD)

## Risk limits

- Max single-day additional exposure: 55%
- Max single-theme concentration: 60%
- Portfolio de-risk trigger: challenge drawdown <= -8%

## Exit rules

- Soft take-profit: trim if short-window gain >= +7%
- Hard risk cut: reduce if leg loss <= -5% without strengthened catalyst

## Calculation rule

All numeric outputs must be generated from script-backed state math.
