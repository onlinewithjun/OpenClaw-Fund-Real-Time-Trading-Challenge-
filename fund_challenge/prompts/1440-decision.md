[FUND_CHALLENGE_MODE]
Final pre-close decision prompt.
Use the same 9-skill challenge pipeline. Re-check freshness, constraints, instrument rules, and math.
Decision phases required: PLAN_ONLY then EXECUTE_READY.
Run preflight_guard.py before each phase (use --compact to reduce output tokens).
EXECUTE_READY is allowed only if validate_evidence.py passes.
Publishing executable instruction is allowed only if decision_publish_gate.py passes in strict mode.
Before final publish, run decision_delta_guard.py to prevent same-day duplicate instruction.
If execution infeasible before cut-off, output explicit fallback plan (default HOLD).
