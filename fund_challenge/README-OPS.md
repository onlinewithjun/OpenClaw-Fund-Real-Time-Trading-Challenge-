# Fund Challenge Ops Rules (Challenge-Only)

- Trigger tag: `[FUND_CHALLENGE_MODE]`
- Required skills:
  - fund-challenge-daily-trader-core
  - fund-challenge-data-guard
  - fund-challenge-execution-engine
- Deterministic math: `python fund_challenge/scripts/state_math.py --state fund_challenge/state.json`
- State write policy:
  - Update `state.json` only after explicit user execution confirmation
  - Append every update to `ledger.jsonl`
- Abort policy: if any key value cannot be verified from tools/reliable source, abort decision.
