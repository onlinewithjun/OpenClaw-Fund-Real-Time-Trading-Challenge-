# Daily Checklist (Challenge Mode Only)

1. Confirm today is a trading day.
2. Pull `fund_challenge/state.json`.
3. Verify each fund code-name pair (double query).
4. Verify data freshness timestamps.
5. Run script: `python fund_challenge/scripts/state_math.py --state fund_challenge/state.json`.
6. If any verification fails -> `DECISION_ABORTED_UNVERIFIED_DATA`.
7. Produce one primary action and one fallback.
8. Include execution deadline (before 15:00 Asia/Shanghai).
9. Wait for user execution confirmation.
10. Record confirmed action in `ledger.jsonl` and update `state.json`.
