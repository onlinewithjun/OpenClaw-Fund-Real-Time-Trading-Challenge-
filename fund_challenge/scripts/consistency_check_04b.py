#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
STATE_PATH = WORKSPACE / "fund_challenge" / "state.json"
CANDIDATES_PATH = WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json"
MARKER_PATH = WORKSPACE / "fund_challenge" / "runtime" / "consistency_04b.json"


def fail(msg: str) -> None:
    save_json(MARKER_PATH, {
        "ok": False,
        "checkedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "reason": msg,
    })
    print(f"【基金挑战#04b｜14:40一致性补刷】 CONSISTENCY_ALERT: {msg}")
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Post-universe-refresh consistency checks for 14:40 guard")
    ap.add_argument("--after", default="14:35", help="Require state.asOf and candidates.updatedAt >= HH:MM")
    args = ap.parse_args()

    if not STATE_PATH.exists():
        fail("state.json_missing")
    if not CANDIDATES_PATH.exists():
        fail("daily_candidates.json_missing")

    try:
        floor_t = datetime.strptime(args.after, "%H:%M").time()
    except Exception:
        fail(f"bad_after_time={args.after}")

    today = datetime.now().date().isoformat()

    state = load_json(STATE_PATH)
    asof = str(state.get("asOf", ""))
    if not asof:
        fail("state_asOf_missing")
    try:
        asof_dt = parse_iso(asof)
    except Exception:
        fail(f"state_asOf_invalid={asof}")
    if asof_dt.date().isoformat() != today or asof_dt.time() < floor_t:
        fail(f"stale_state_asOf={asof}; require_after={args.after}")

    holdings = state.get("holdings", []) if isinstance(state, dict) else []
    if not holdings:
        fail("holdings_empty")
    for h in holdings:
        code = str(h.get("code", "")).strip()
        mv = h.get("marketValue")
        if not code or mv in (None, ""):
            fail("core_holding_fields_missing(code/marketValue)")

    candidates = load_json(CANDIDATES_PATH)
    updated = str(candidates.get("updatedAt", "")) if isinstance(candidates, dict) else ""
    if not updated:
        fail("candidates_updatedAt_missing")
    try:
        upd_dt = parse_iso(updated)
    except Exception:
        fail(f"candidates_updatedAt_invalid={updated}")
    if upd_dt.date().isoformat() != today or upd_dt.time() < floor_t:
        fail(f"stale_candidates_updatedAt={updated}; require_after={args.after}")

    arr = candidates.get("candidates", []) if isinstance(candidates, dict) else []
    if not isinstance(arr, list) or len(arr) == 0:
        fail("candidates_empty")

    save_json(MARKER_PATH, {
        "ok": True,
        "checkedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "requireAfter": args.after,
        "stateAsOf": asof,
        "candidatesUpdatedAt": updated,
        "candidatesCount": len(arr),
    })

    print(
        "【基金挑战#04b｜14:40一致性补刷】 CONSISTENCY_OK "
        f"asOf={asof} candidates_updatedAt={updated} candidates={len(arr)}"
    )


if __name__ == "__main__":
    main()
