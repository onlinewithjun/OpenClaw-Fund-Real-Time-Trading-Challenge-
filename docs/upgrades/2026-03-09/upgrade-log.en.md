# Upgrade Log (2026-03-09)

## 1) Data Basis Correction
- Holding updates were switched to final NAV (`lsjz`) accounting.
- Intraday estimate values are no longer allowed as end-of-day booking basis.

## 2) Universe Refresh Pipeline
- Universe refresh moved to a two-stage flow:
  - broad scan (~50 funds)
  - deep refine shortlist
- 14:00 planning now consumes the refreshed full-market candidate scope.

## 3) Strategy & Risk Controls
- Enforced purchasable-universe constraints (TiantianFund / Alipay eligible scope).
- Strengthened `riskSwitch` with turnover/drawdown guardrails.
- Added oversold-rotation channel and linked it to execution feasibility checks.

## 4) Evidence Validation
- Completed evidence-array population and validation hardening for the PLAN phase.

## 5) Infrastructure
- Added a local DashScope embeddings proxy to restore `memory_search` compatibility.

## 6) Security Note
- No plaintext secrets were committed in this change set.
