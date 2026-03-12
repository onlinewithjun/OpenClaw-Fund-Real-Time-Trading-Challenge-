from __future__ import annotations

import argparse
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


def dec(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def q2(v: Decimal) -> str:
    return str(v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def q4(v: Decimal) -> str:
    return str(v.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def main() -> None:
    ap = argparse.ArgumentParser(description="Reconcile holdings from manual snapshot values")
    ap.add_argument("--state", default="fund_challenge/state.json")
    ap.add_argument("--snapshot", required=True, help="Path to manual snapshot json")
    ap.add_argument("--ledger", default="fund_challenge/ledger.jsonl")
    args = ap.parse_args()

    state_path = Path(args.state)
    snap_path = Path(args.snapshot)
    ledger_path = Path(args.ledger)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    snap = json.loads(snap_path.read_text(encoding="utf-8"))

    items = snap.get("holdings", [])
    if not isinstance(items, list) or not items:
        raise SystemExit("snapshot.holdings is required")

    by_code = {str(x.get("code")): x for x in items if x.get("code")}

    for h in state.get("holdings", []):
        code = str(h.get("code", ""))
        if code not in by_code:
            continue
        src = by_code[code]
        mv = dec(src.get("marketValue", h.get("marketValue", "0")))
        upnl = dec(src.get("unrealizedPnl", h.get("unrealizedPnl", "0")))
        nav = dec(h.get("latestNav", "0"))
        if nav <= 0:
            raise SystemExit(f"latestNav missing for code={code}")

        shares = mv / nav
        cost_total = mv - upnl
        cost_unit = (cost_total / shares) if shares > 0 else dec("0")

        h["marketValue"] = q2(mv)
        h["unrealizedPnl"] = q2(upnl)
        h["shares"] = q4(shares)
        h["totalShares"] = q4(shares)
        h["availableShares"] = q4(shares)
        h["costBasisUnit"] = q4(cost_unit)

    if "cash" in snap:
        state["cash"] = str(snap.get("cash"))

    if "pendingTransactions" in snap:
        state["pendingTransactions"] = snap.get("pendingTransactions") or []

    state["asOf"] = snap.get("asOf") or now_iso()
    state["notes"] = f"Manual reconciliation applied at {now_iso()}"

    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    event = {
        "ts": now_iso(),
        "event": "manual_reconcile",
        "snapshot": str(snap_path),
        "asOf": state["asOf"],
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"RECONCILE_OK asOf={state['asOf']} snapshot={snap_path}")


if __name__ == "__main__":
    main()
