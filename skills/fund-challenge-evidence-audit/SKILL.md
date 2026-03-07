---
name: fund-challenge-evidence-audit
description: Evidence capture and machine-auditable decision gating for challenge mode. Use ONLY in challenge tasks to write evidence snapshots, validate citation completeness, and enforce PLAN_ONLY to EXECUTE_READY transition.
---

# Fund Challenge Evidence Audit

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Purpose

Guarantee that every numeric or factual claim is backed by timestamped evidence.

## Files

- `fund_challenge/evidence/<decisionId>.json`
- `fund_challenge/evidence/latest.json`
- `fund_challenge/scripts/build_evidence.py`
- `fund_challenge/scripts/validate_evidence.py`

## Decision phases

1. `PLAN_ONLY`: produce candidate action and missing evidence checklist.
2. `EXECUTE_READY`: allowed only if all mandatory evidence fields are complete.

## Mandatory evidence fields

- decisionId
- generatedAt (Asia/Shanghai)
- stateDigest (portfolio value, pnl, target gap from script output)
- fundIdentityChecks[]
- marketSignals[] with source and timestamp
- executionConstraints[]
- arithmeticChecksum

## Gate rule

If any field is missing, or source timestamps are stale/unknown, force output:
`DECISION_ABORTED_UNVERIFIED_DATA`

Before any EXECUTE_READY output, run:

`python fund_challenge/scripts/validate_evidence.py --evidence fund_challenge/evidence/latest.json --require-execute-ready`

If validator fails, block execution and downgrade to HOLD.

## Fallback policy

When audit fails, publish HOLD + data-gap remediation steps; never emit aggressive buy/switch.
