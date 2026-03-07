[FUND_CHALLENGE_MODE]
Final pre-close decision prompt.
Use the same 9-skill challenge pipeline. Re-check freshness, constraints, instrument rules, and math.
Decision phases required: PLAN_ONLY then EXECUTE_READY.
EXECUTE_READY is allowed only if validate_evidence.py passes.
If execution infeasible before cut-off, output explicit fallback plan (default HOLD).
