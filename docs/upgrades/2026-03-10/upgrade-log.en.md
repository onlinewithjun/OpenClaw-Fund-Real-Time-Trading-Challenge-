# Upgrade Log (2026-03-10)

## Scheduler and Workflow
- Reordered evening jobs (weekdays):
  - Update → 21:00
  - PostSummary → 21:30
  - Review → 21:45
  - Maintenance → 22:00
- Split post-close pipeline into two steps:
  - STEP1 (lightweight update)
  - STEP2 (post summary)
- Added new cron job: `FundChallenge-20:12-PostSummary`.

## Data Basis and Risk Controls
- Fixed holding-update basis; intraday estimate fields (`gsz/gszzl`) are no longer allowed as final source.
- Standardized to final NAV basis via Eastmoney F10 `lsjz` for end-of-day recalculation.
- Applied and audited 2026-03-09 holding update with rollback/correction trace.

## Candidate Pool and Strategy
- Universe refresh moved to two-stage pipeline:
  - Broad scan: at least 50 funds
  - Deep refine: 10-15 funds
- Enforced full purchasable universe scope (TiantianFund/Alipay) with elimination/replacement rules.
- Integrated riskSwitch + oversoldRotationChannel into decision prompts.

## Memory Retrieval Infrastructure
- Restored `memory_search` chain by:
  - adding a local DashScope embeddings proxy
  - enabling startup task `OpenClaw-EmbedProxy`
- Avoided 404/401 issues caused by compatibility path mismatch.

## Security Note
- Performed secret-pattern scan before commit.
- No plaintext API keys were committed.
