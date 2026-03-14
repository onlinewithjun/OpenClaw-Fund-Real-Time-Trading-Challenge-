# Upgrade Log (2026-03-14)

## 1) Model and Gateway
- Enabled and switched the default primary model to `openai-codex/gpt-5.4`.
- Fixed the OpenClaw gateway service entrypoint drift so the scheduled service now points to the current nvm-managed installation.
- Cleaned the session store by removing missing-transcript index entries and orphan transcript files; `openclaw doctor` no longer reports those issues.

## 2) Memory and Context Optimization
- Compacted `MEMORY.md` to keep only durable long-term information.
- Added `memory/2026-03-14.md` to record the day’s maintenance and strategy evolution.
- Archived older daily notes into `memory/archive/` and short-lived reports into `memory/archive/special/`.
- Added a context high-water mark rule in `AGENTS.md` so memory is written proactively before context pressure becomes risky.
- Added a daily `Memory maintenance` cron job for conservative review, archiving, and compaction.
- Recorded the user preference that low-risk internal optimizations can be applied proactively without repeated approval.

## 3) Fund Challenge System Fixes
- Added actual evening retry scheduling for `update_refresh_retry.py` via new #06b~#06f retry jobs.
- Upgraded `healthcheck_brief.py`:
  - no longer checks only file existence and syntax;
  - now validates freshness windows for `state.json`, `daily_candidates.json`, and `consistency_04b.json`;
  - added a non-trading-day friendly mode returning `HEALTHCHECK_OK NON_TRADING_DAY ...`.
- Added `fund_challenge/scripts/maintenance_cleanup.py` to:
  - prune runtime cache,
  - remove temporary failure files under `out/`,
  - archive older evidence files,
  - clean `__pycache__`,
  - remove stale runtime snapshots,
  - remove historical nested leftover directories.
- Switched the #08 maintenance cron to `maintenance_cleanup.py`.
- Moved the `TARGET_REMAP` logic out of hardcoded Python and into `instrument_rules.json.targetRemap`.

## 4) Fund Challenge Strategy Upgrade
- Upgraded the strategy from a short-term framework with conservative behavior into a more genuinely aggressive short-term style while still avoiding blind chasing.
- Enhanced `gate_scoring.py` with:
  - strong-switch detection,
  - `strongSwitchCount` / `pullbackCount`,
  - confidence tiers (A/B/C),
  - `suggestedBuyPct`,
  - improved momentum scoring and risk-switch logic.
- Enhanced `execute_gate_script_only.py` with:
  - dual entry lanes: pullback entry + strong-switch entry,
  - non-fixed buy sizing driven by evidence-based suggested allocation,
  - exit target selection upgraded from simple worst-PnL ranking to expectation-failure-first liquidation.
- Preserved stale/freshness guards and the real external execution confirmation boundary so aggressive strategy changes do not bypass core safety rails.

## 5) Toward Higher Autonomy
- Added `基金挑战#09-01:20策略复盘优化`, an isolated daily cron job that:
  - reviews the challenge every night,
  - learns and tunes the challenge strategy/ops conservatively,
  - writes memory notes and commits relevant internal changes.
- Recorded the user’s delegation: the Fund Challenge strategy layer is fully delegated to the AI, with the user accepting very high risk; real external buy/redeem execution still keeps a final execution/confirmation boundary.
