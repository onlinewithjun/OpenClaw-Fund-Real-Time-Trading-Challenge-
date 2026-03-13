# Upgrade Log (2026-03-12)

## 1) Execution Gate and Candidate Normalization
- Hardened 14:00/14:45 planning + execution gates with script-level checks.
- Added 14:40 consistency marker flow before final execution publish.
- Enforced pullback-only trial-buy policy (no blind chase on breakout candles).
- Normalized actionable targets to off-exchange purchasable funds.
- Added auto-remap from on-exchange ETF code `159509` to off-exchange `019118` when needed.

## 2) Universe and Rule Refresh Improvements
- Universe refresh output now reports added/removed candidate details.
- Rule metadata refresh updated `instrument_rules.json` timestamps and source mapping integrity.
- Improved review/plan stdout to include stronger hard-gate context.

## 3) State Accuracy Fix (Root Cause Patch)
- Fixed portfolio drift caused by stale shares/cost basis against user-side app records.
- Added explicit `pendingTransactions` model to avoid in-transit omission.
- `execution_receipt_updater.py` now records pending BUY/REDEEM status and applies conservative cash handling for unconfirmed BUY receipts.
- Added `reconcile_positions.py` for manual snapshot reconciliation (market value/PnL -> shares/cost basis backfill).
- `review_summary_script.py` now prints pending BUY/REDEEM separately and excludes pending items from settled PnL attribution.

## 4) Data Basis Clarification
- NAV snapshot remains sourced from Tiantian/Eastmoney fund interface (`dwjz` first, `gsz` fallback).
- Root issue was not NAV source mismatch, but state-accounting mismatch.
- Reconciliation flow was executed on 2026-03-12 to align holdings with user-confirmed snapshot.

## 5) Documentation Refresh
- Refreshed both `README.md` and `README.zh-CN.md`.
- Added 2026-03-12 bilingual upgrade log links.
- Synced Chinese README prompt and cron sections with current runtime workflow.
