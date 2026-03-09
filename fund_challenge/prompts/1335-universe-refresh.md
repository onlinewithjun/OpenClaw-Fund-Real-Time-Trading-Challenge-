[FUND_CHALLENGE_MODE][UNIVERSE_REFRESH]
Goal: refresh expanded candidate pool from TiantianFund full market perspective before 14:00 planning.

Requirements:
0) Read `fund_challenge/universe/strategy_mode.json` first and apply riskSwitch + poolMechanism.
1) Build/refresh `fund_challenge/universe/daily_candidates.json` with 10-20 candidates across styles:
   - Tech growth
   - Cyclical/resources
   - Gold/defensive
   - Broad index core
2) For each candidate, must verify via web_search using:
   - "fund_code + fund_name + 天天基金网"
   - Confirm code-name exact match; if uncertain, drop candidate.
3) Keep fields for each item:
   - code, name, category, rationale, sourceUrl, verifiedAt, confidence
4) Also write a compact markdown summary:
   - `fund_challenge/universe/daily_candidates.md`
   - Include TOP5 and why.
5) Enforce pool turnover policy:
   - Output entries for: added, removed, retained.
   - Max daily replacements: 3 unless user explicitly overrides.
6) If data quality is insufficient, output `DECISION_ABORTED_UNVERIFIED_DATA` and keep previous file unchanged.

Output:
- one short status line only.