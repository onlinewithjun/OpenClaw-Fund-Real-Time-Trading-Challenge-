[FUND_CHALLENGE_MODE][HEALTHCHECK]
Run a lightweight daily health check before market work:
1) Verify cron scheduler enabled and challenge jobs exist/enabled.
2) Verify model route openai-codex/gpt-5.3-codex is available.
3) Verify key files exist: fund_challenge/state.json, fund_challenge/ledger.jsonl, fund_challenge/instrument_rules.json.
4) Verify python scripts callable: state_math.py, preflight_guard.py.
5) Verify cache prune command is callable.

Output rule:
- If all checks pass: output NO_REPLY.
- If any check fails: output one short alert with failed item + quick fix suggestion.
