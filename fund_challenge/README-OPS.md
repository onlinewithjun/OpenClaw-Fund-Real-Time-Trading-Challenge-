# Fund Challenge Ops Rules (Challenge-Only)

- Trigger tag: `[FUND_CHALLENGE_MODE]`
- Required skills:
  - fund-challenge-orchestrator
  - fund-challenge-market-calendar-gate
  - fund-challenge-identity-freshness-guard
  - fund-challenge-signal-fusion-engine
  - fund-challenge-position-risk-engine
  - fund-challenge-offexchange-exec-sim
  - fund-challenge-instrument-rules
  - fund-challenge-evidence-audit
  - fund-challenge-ledger-postmortem
- Deterministic math: `python fund_challenge/scripts/state_math.py --state fund_challenge/state.json`
- State write policy:
  - Update `state.json` only after explicit user execution confirmation
  - Append every update to `ledger.jsonl`
- Abort policy: if any key value cannot be verified from tools/reliable source, abort decision.
