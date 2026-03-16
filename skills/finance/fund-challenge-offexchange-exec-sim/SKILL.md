---
name: fund-challenge-offexchange-exec-sim
description: Off-exchange execution constraint simulator for challenge mode. Use only in challenge tasks to model T+ confirmation/settlement, subscription/redemption limits, and cutoff feasibility.
---

# Fund Challenge Off-Exchange Execution Simulator

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Mandatory execution checks

- Validate T+ confirmation and settlement path for each action.
- Validate redemption cash availability date before reuse.
- Validate subscription/redemption restrictions and cut-off.
- Reject same-day round-trip assumptions.

## Output requirements

- Feasible/Not-feasible flag
- Earliest effective date
- Cash availability date
- Fallback plan when infeasible

## Policy

If execution feasibility is uncertain, do not issue trade command.
