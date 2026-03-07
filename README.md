# OpenClaw Fund Real-Time Trading Challenge

A challenge-only, production-minded workflow for a **1000 CNY aggressive off-exchange fund trading experiment**.

## Goal

- Start capital: **1000 CNY**
- Target: **2x within 6 months**
- Platforms: **Alipay / TiantianFund**
- Style: **Short-term aggressive**, but with strict verification and risk gates

## What this branch contains

- `fund_challenge/` challenge runtime files only
- `skills/fund-challenge-*` challenge-specific skills only
- No unrelated coding/project files

## Core design

1. **State-first**: deterministic state and ledger updates
2. **Evidence-gated**: no EXECUTE_READY without validated evidence
3. **Execution-safe**: off-exchange constraints (T+ rules, cutoff, feasibility)
4. **Low-token ops**: compact prompts, compact evidence, short publish format

## Daily workflow (trading day)

- **09:00** Healthcheck (silent if healthy)
- **14:00** PLAN_ONLY
- **14:48** EXECUTE_READY gate (single actionable plan)
- **20:05** Update
- **20:25** Review
- **21:00** Maintenance (cache prune)

## Human responsibilities

- Only manual action needed: execute BUY in app before cutoff when instructed
- Confirm execution with short text, e.g.:
  - `I bought 020899 100 CNY at 14:52`
  - `Not executed: subscription suspended`

## Key scripts

- `run_decision_pipeline.py`: end-to-end compact pipeline
- `preflight_guard.py`: deterministic gating
- `decision_publish_gate.py`: strict publish gate
- `confirm_and_apply.py`: one-shot parse+apply confirmation
- `execution_receipt_updater.py`: authoritative state/ledger update

## Safety policy

If any key number/source cannot be verified, output:

`DECISION_ABORTED_UNVERIFIED_DATA`

and fall back to **HOLD**.
