[FUND_CHALLENGE_MODE][HEALTHCHECK]
Run a lightweight daily health check before market work. Execute these checks sequentially:

1) **Cron check**: Verify cron scheduler enabled and all 6 challenge jobs exist/enabled.
2) **File check**: Verify key files exist: fund_challenge/state.json, fund_challenge/ledger.jsonl, fund_challenge/instrument_rules.json.
3) **Script syntax check**: Run `python -m py_compile` on: state_math.py, preflight_guard.py, runtime_cache.py.
4) **Cache prune test**: Run `python fund_challenge/scripts/runtime_cache.py prune --help` (help only, not actual prune).

**DO NOT** run preflight_guard.py full execution (it triggers slow API calls).

Output rule:
- If all checks pass: output NO_REPLY.
- If any check fails: output one short alert with failed item + quick fix suggestion.
