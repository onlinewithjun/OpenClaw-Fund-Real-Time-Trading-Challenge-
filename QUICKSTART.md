# QUICKSTART (3 Minutes)

## 1) Pre-check (once)

```bash
python fund_challenge/scripts/state_math.py --state fund_challenge/state.json
openclaw cron list --all
```

## 2) Daily operation (trading day)

- 14:00: PLAN_ONLY arrives
- 14:48: EXECUTE_READY arrives (single plan only)
- If action is BUY, execute manually in Alipay/Tiantian before cutoff
- Reply confirmation text, e.g.:
  - `我已买入 020899 100元，14:52`
  - `未执行：限购`

## 3) One-shot confirmation apply

```bash
python fund_challenge/scripts/confirm_and_apply.py --text "我已买入 020899 100元" --link-decision-id
```

## 4) Core emergency rules

- If data is unverifiable: `DECISION_ABORTED_UNVERIFIED_DATA` + HOLD
- If plan cannot execute (suspension/limit/cutoff): return HOLD, then next feasible single plan
- No user confirmation = no state update

## 5) Useful diagnostics

```bash
python fund_challenge/scripts/status_brief.py
python fund_challenge/scripts/daily_bundle_runner.py --phase PLAN_ONLY
openclaw cron runs --limit 20
```
