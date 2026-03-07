# Evidence Artifacts

Each challenge decision must write:

- `fund_challenge/evidence/<decisionId>.json`
- `fund_challenge/evidence/latest.json`

## Required phase flow

1. PLAN_ONLY
2. EXECUTE_READY (only after all required evidence is complete)

If any required evidence field is missing or stale, decision must abort with:
`DECISION_ABORTED_UNVERIFIED_DATA`
