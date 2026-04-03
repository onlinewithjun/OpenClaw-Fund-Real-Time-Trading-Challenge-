# Upgrade Log (2026-04-03)

## 1) Telegram Announcement Delivery Fix (P0)

**Problem**: All non-trading-hour isolated-session crons (evening 21:xx, morning 09:xx, overnight 01~03xx, weekly report, etc.) were failing with `Outbound not configured for channel: telegram` for 2 consecutive runs; intraday 14:xx crons were completely fine.

**Root cause**: The announcement dispatcher fails when running isolated sessions outside trading hours, unrelated to `sessionKey` configuration.

**Fix**: Migrated 16 failing cron jobs from `sessionTarget=isolated` to `sessionTarget=current`, binding them to the main session to ensure the announcement delivery context is valid.

Affected cron jobs:
- Fund Challenge #09~#16 (evening update/retry/review/maintenance batches)
- Fund Challenge #17 (overnight 01:20 strategy review)
- workspace-secret-scan-daily, memory-maintenance-daily
- Morning news digests (US close, AI 24h, HK evening, A-share evening)

---

## 2) Execution Layer Cooldown Guard (P2 - Bug 4)

**Problem**: MEMORY.md explicitly prohibits low-quality "sold yesterday, bought back today" whipsaw loops, but the execute gate had no such protection. This allowed the 4/1~4/2 reverse operations (002611 sold consecutively, then 000056 bought back immediately).

**Fix**:
- Added `recent_action_map()`: tracks REDEEM and BUY counts per fund code within a 5-day window by reading ledger.jsonl
- Added `cooldown_violation()`: same code + same action type + >=2 occurrences within 5 days → hard block with cooldown violation reason
- Integrated into all 3 decision branches in `execute_gate_script_only.py` (REDEEM_REDUCE / TRIAL_BUY / raise_cash)

Example output when triggered:
```
cooldown_redeem_violation_002611_within_5d_count=2  →  HOLD
cooldown_buy_violation_000056_within_5d_count=2     →  HOLD
```

---

## 3) Plan Report Signal Deviation Alerts (P2 - Bug 3)

**Problem**: 000056 (Jianxin Consumer Growth Mixed) was manually bought at ¥78, but its quant rank was #10 (second-to-last), score=61.4, confidence=0.72 — a severe deviation from the quant system with no alert generated.

**Fix**: `generate_full_plan_report()` now annotates each holding with its quant rank. When rank >= 8, a `[Signal Deviation Alerts]` section is appended:
```
ALERT: 000056 is ranked #10 (quant signal weak) but still held - review for reduction or exit
```

---

## 4) PV Target De-risk Warning (P2 - Bug 5)

**Problem**: On 3/31, portfolio NAV briefly hit 2004 (distanceToTarget=-4.41), but the system generated no alert and the user missed the opportunity to lock in profits.

**Fix**: `generate_full_plan_report()` now detects `portfolioValue >= target` and appends a warning below the `[Portfolio]` section:
```
** DE-RISK RECOMMENDED: Strongly consider REDEEMING profits rather than initiating new BUYs **
```

---

## 5) Outstanding Issues (Pending Audit)

### ⚠️ 4/1~4/2 Reverse Operation Root Cause

Observed in ledger MTM records:
```
03-31 21:00  PV=2004 (target reached)
04-01 21:00  PV=891  (aggressive sell-off, pendingRedeem=¥180)
04-02 21:00  PV=986  (immediate buy-back)
```

The pattern lacks logical coherence. The likely cause is interference between `auto_close_stale_pending` and manual operations. Recommended action: dedicate a special review during the next #17 overnight strategy review (01:20) to audit this operation chain.

---

## 6) Other Changes

- Added one-off fix scripts: `add_017172_redeem.py`, `fix_pending_020899.py`, `fix_state_manual.py`
- Memory archiving: daily notes older than 7 days moved to `memory/archive/`
- `MEMORY.md` kept compact with only durable long-term information
