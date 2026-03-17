from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


TERMINAL = {"SETTLED", "CANCELLED"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_local() -> datetime:
    return datetime.now().astimezone()


def now_iso() -> str:
    return now_local().replace(microsecond=0).isoformat()


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))


def append_ledger(ledger_path: Path, event: dict) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Auto-close stale pending transactions to unblock ops healthchecks")
    ap.add_argument("--state", default="fund_challenge/state.json")
    ap.add_argument("--ledger", default="fund_challenge/ledger.jsonl")
    ap.add_argument("--hours", type=float, default=48.0, help="Close active pending items older than this many hours")
    args = ap.parse_args()

    state_path = Path(args.state)
    ledger_path = Path(args.ledger)
    state = load_json(state_path)
    pending = state.get("pendingTransactions", [])
    if not isinstance(pending, list):
        pending = []

    cutoff = now_local() - timedelta(hours=args.hours)
    changed: list[dict] = []

    for item in pending:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status", "")).upper()
        if status in TERMINAL:
            continue
        created_at = str(item.get("createdAt", "")).strip()
        if not created_at:
            continue
        try:
            created_dt = parse_iso(created_at)
        except Exception:
            continue
        if created_dt.tzinfo is None:
            created_dt = created_dt.replace(tzinfo=now_local().tzinfo)
        if created_dt <= cutoff:
            old_status = item.get("status")
            item["status"] = "CANCELLED"
            note = str(item.get("note", "")).strip()
            suffix = f"auto-closed stale pending at {now_iso()} after >{args.hours:g}h"
            item["note"] = f"{note} | {suffix}" if note else suffix
            item["resolvedAt"] = now_iso()
            changed.append({
                "id": item.get("id"),
                "code": item.get("code"),
                "actionType": item.get("actionType"),
                "createdAt": created_at,
                "oldStatus": old_status,
                "newStatus": item["status"],
            })

    if not changed:
        print("AUTO_CLOSE_STALE_PENDING_NOOP")
        return

    state["pendingTransactions"] = pending
    state["notes"] = f"Auto-closed stale pending transactions at {now_iso()}"
    save_json(state_path, state)

    append_ledger(ledger_path, {
        "ts": now_iso(),
        "event": "auto_close_stale_pending",
        "count": len(changed),
        "thresholdHours": args.hours,
        "items": changed,
    })

    codes = ",".join(sorted({str(x.get("code") or "UNKNOWN") for x in changed}))
    print(f"AUTO_CLOSE_STALE_PENDING_OK count={len(changed)} codes={codes}")


if __name__ == "__main__":
    main()
