# Upgrade Log (2026-03-10)

## 1) Scheduler & Workflow Refactor
- Evening jobs were reordered (weekdays):
  - Update: 21:00
  - PostSummary: 21:30
  - Review: 21:45
  - Maintenance: 22:00
- Post-close flow was split into two steps:
  - STEP1 (lightweight, script-first update)
  - STEP2 (post summary)
- New job added: `FundChallenge-20:12-PostSummary`.
- Added stagger offsets to reduce contention:
  - 21:30 +120s, 21:45 +240s, 22:00 +360s.

## 2) Data Basis & Holding Updates
- Intraday estimate fields (`gsz/gszzl`) are no longer allowed as final basis.
- End-of-day calculations are standardized on Eastmoney F10 `lsjz` final NAV.
- Applied correction chain for 2026-03-09 holdings: rollback estimate -> recompute by final NAV -> rewrite state.

## 3) Strategy & Candidate Pool
- Universe refresh upgraded to two-stage mode:
  - Broad scan: at least 50 funds
  - Deep refine: 10-15 funds
- Enforced full purchasable universe scope (TiantianFund/Alipay).
- Integrated `riskSwitch + oversoldRotationChannel` in decision prompts.

## 4) Memory Retrieval Infrastructure
- Restored `memory_search` compatibility by:
  - local DashScope embeddings proxy (127.0.0.1:18890)
  - startup task `OpenClaw-EmbedProxy`
- Resolved embeddings 401/404 compatibility failures.

## 5) Documentation Sync
- Refreshed both `README.md` and `README.zh-CN.md`:
  - aligned latest schedule and two-step flow
  - added daily upgrade-log entry links

## 6) Security Check
- Ran secret-pattern scan (API key/token patterns) on staged diffs.
- No plaintext keys committed.
