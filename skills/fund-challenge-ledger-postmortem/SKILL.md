---
name: fund-challenge-ledger-postmortem
description: State persistence, ledger audit, and post-trade review for challenge mode. Use only for challenge tasks to ensure deterministic updates, traceability, and learning feedback loops.
---

# Fund Challenge Ledger and Postmortem

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Persistence rules

- Update `fund_challenge/state.json` only after explicit user execution confirmation.
- Apply confirmation with `fund_challenge/scripts/execution_receipt_updater.py`.
- Append immutable event to `fund_challenge/ledger.jsonl` for every confirmed action.
- Recompute state via `state_math.py` before writing snapshot.

## Audit fields

Each ledger event includes:

- timestamp
- decisionId
- action type
- instrument code/name
- amount
- evidence summary with source timestamps
- resulting portfolio snapshot

## Postmortem protocol

- Daily: summarize decision quality and misses.
- Weekly: evaluate hit rate, drawdown pattern, and rule violations.
- Never optimize by rewriting historical events.
