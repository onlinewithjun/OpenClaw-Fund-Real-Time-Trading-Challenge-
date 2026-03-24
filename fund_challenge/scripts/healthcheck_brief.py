#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import py_compile
import subprocess
import sys
from datetime import datetime, time
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
OPENCLAW_HOME = Path(os.environ.get("USERPROFILE", "")) / ".openclaw"
CRON_JOBS = OPENCLAW_HOME / "cron" / "jobs.json"
STATE_PATH = WORKSPACE / "fund_challenge" / "state.json"
CANDIDATES_PATH = WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json"
CONSISTENCY_PATH = WORKSPACE / "fund_challenge" / "runtime" / "consistency_04b.json"


def fail(msg: str) -> None:
    print(f"HEALTHCHECK_ALERT: {msg}")
    sys.exit(1)


def ok(msg: str = "HEALTHCHECK_OK") -> None:
    print(msg)
    sys.exit(0)


def check_cron_jobs() -> None:
    if not CRON_JOBS.exists():
        fail("cron jobs.json missing; run openclaw gateway restart")
    try:
        data = json.loads(CRON_JOBS.read_text(encoding="utf-8"))
    except Exception:
        fail("cron jobs.json invalid JSON; re-save cron config")

    jobs = data.get("jobs", []) if isinstance(data, dict) else []
    challenge_jobs = [
        j for j in jobs
        if str(j.get("name", "")).startswith("基金挑战-")
        or str(j.get("name", "")).startswith("基金挑战#")
    ]
    enabled_jobs = [j for j in challenge_jobs if j.get("enabled", True)]
    if len(enabled_jobs) < 6:
        fail(f"enabled challenge jobs={len(enabled_jobs)} (<6); check cron list")


def check_files() -> None:
    required = [
        WORKSPACE / "fund_challenge" / "state.json",
        WORKSPACE / "fund_challenge" / "ledger.jsonl",
        WORKSPACE / "fund_challenge" / "instrument_rules.json",
    ]
    for p in required:
        if not p.exists():
            fail(f"missing {p.relative_to(WORKSPACE)}; restore from backup")


def check_python_syntax() -> None:
    scripts = [
        WORKSPACE / "fund_challenge" / "scripts" / "state_math.py",
        WORKSPACE / "fund_challenge" / "scripts" / "preflight_guard.py",
        WORKSPACE / "fund_challenge" / "scripts" / "runtime_cache.py",
        WORKSPACE / "fund_challenge" / "scripts" / "maintenance_cleanup.py",
    ]
    for s in scripts:
        try:
            py_compile.compile(str(s), doraise=True)
        except Exception:
            fail(f"py_compile failed: {s.name}; fix syntax")


def check_cache_help() -> None:
    cmd = [
        sys.executable,
        str(WORKSPACE / "fund_challenge" / "scripts" / "runtime_cache.py"),
        "prune",
        "--help",
    ]
    result = subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        fail("runtime_cache prune --help failed; check script args")


def auto_close_stale_pending() -> None:
    cmd = [
        sys.executable,
        str(WORKSPACE / "fund_challenge" / "scripts" / "auto_close_stale_pending.py"),
        "--state",
        str(STATE_PATH),
        "--ledger",
        str(WORKSPACE / "fund_challenge" / "ledger.jsonl"),
        "--hours",
        "48",
    ]
    subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True, timeout=30)


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def date_part(ts: str) -> str:
    return str(ts).split("T", 1)[0].split(" ", 1)[0]


def check_data_freshness() -> str:
    now = datetime.now()
    today = now.date().isoformat()
    current_t = now.time()

    if not STATE_PATH.exists():
        fail("state.json missing")
    state = load_json(STATE_PATH)
    asof = str(state.get("asOf", "")).strip()
    if not asof:
        fail("state.asOf missing")

    try:
        parse_iso(asof)
    except Exception:
        fail(f"state.asOf invalid: {asof}")

    pending = state.get("pendingTransactions", []) if isinstance(state, dict) else []
    active_pending = [
        t for t in pending
        if str((t or {}).get("status", "")).upper() not in {"SETTLED", "CANCELLED", "FAILED"}
        and not str((t or {}).get("resolvedAt", "")).strip()
    ]

    # Weekend / non-trading-day mode: keep checks structural and explanatory, do not hard-fail on stale trade date.
    if now.weekday() >= 5:
        return f"NON_TRADING_DAY lastStateAsOf={asof}"

    # Before market opens, allow previous trade-day snapshot, but reject invalid state.
    if current_t >= time(9, 0) and date_part(asof) != today:
        fail(f"stale state.asOf: {asof}")

    # Auto-heal obvious stale pending items first so healthcheck can clear low-risk ops debt by itself.
    if active_pending and current_t >= time(9, 0):
        auto_close_stale_pending()
        state = load_json(STATE_PATH)
        pending = state.get("pendingTransactions", []) if isinstance(state, dict) else []
        active_pending = [
            t for t in pending
            if str((t or {}).get("status", "")).upper() not in {"SETTLED", "CANCELLED", "FAILED"}
            and not str((t or {}).get("resolvedAt", "")).strip()
        ]

    # Active overnight BUY orders are hard blockers.
    # Overnight REDEEM orders are informational unless current liquid cash is already exhausted.
    if active_pending and current_t >= time(9, 0):
        overnight_buy = []
        overnight_redeem = []
        cash = float(state.get("cash", "0") or 0)
        for t in active_pending:
            created_at = str((t or {}).get("createdAt", "")).strip()
            if not created_at:
                continue
            try:
                created_dt = parse_iso(created_at)
            except Exception:
                continue
            if created_dt.date().isoformat() >= today:
                continue
            code = str((t or {}).get("code", "")).strip() or "UNKNOWN"
            action_type = str((t or {}).get("actionType", "")).upper()
            if action_type == "BUY":
                overnight_buy.append(code)
            elif action_type in {"REDEEM", "SELL"}:
                overnight_redeem.append(code)
        if overnight_buy:
            fail(f"stale_pending_buy_transactions codes={','.join(sorted(set(overnight_buy)))}")
        if overnight_redeem and cash <= 0:
            fail(f"overnight_redeem_with_no_cash codes={','.join(sorted(set(overnight_redeem)))}")

    # After 13:35, candidate freshness becomes operationally mandatory.
    if current_t >= time(13, 35):
        if not CANDIDATES_PATH.exists():
            fail("daily_candidates.json missing after 13:35")
        candidates = load_json(CANDIDATES_PATH)
        updated = str(candidates.get("updatedAt", "")).strip()
        if not updated:
            fail("daily_candidates.updatedAt missing")
        if date_part(updated) != today:
            fail(f"stale daily_candidates.updatedAt: {updated}")
        arr = candidates.get("candidates", []) if isinstance(candidates, dict) else []
        if not isinstance(arr, list) or len(arr) == 0:
            fail("daily_candidates empty after 13:35")

    # After 14:40, consistency marker should exist and be fresh.
    if current_t >= time(14, 40):
        if not CONSISTENCY_PATH.exists():
            fail("consistency_04b.json missing after 14:40")
        marker = load_json(CONSISTENCY_PATH)
        checked_at = str(marker.get("checkedAt", "")).strip()
        if marker.get("ok") is not True:
            fail(f"consistency marker not ok: {marker.get('reason', '')}")
        if not checked_at or date_part(checked_at) != today:
            fail(f"stale consistency marker: {checked_at}")

    return "TRADING_DAY_OK"


def main() -> None:
    check_cron_jobs()
    check_files()
    check_python_syntax()
    check_cache_help()
    freshness = check_data_freshness()
    ok(f"HEALTHCHECK_OK {freshness}")


if __name__ == "__main__":
    main()
