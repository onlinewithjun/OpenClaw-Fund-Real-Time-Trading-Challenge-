[FUND_CHALLENGE_MODE][UPDATE_STEP1]
Post-close lightweight update (must finish fast).

Strict scope (no long analysis):
1) Recompute/read current state and output status_brief line.
2) Append/update ledger minimal event for today snapshot.
3) Do NOT run broad market scans or long watchlist analysis.
4) If NAV/return basis is needed, use final NAV interface only (Eastmoney F10 lsjz); do NOT use gsz/gszzl as final basis.
5) Do NOT alter holdings unless user explicitly confirmed execution.

Output:
- exactly 2 lines only:
  - Line1: status_brief
  - Line2: update_result (ok/failed + short reason)

If key data unverifiable: output `DECISION_ABORTED_UNVERIFIED_DATA`.