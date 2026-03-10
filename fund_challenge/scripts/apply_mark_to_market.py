from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from state_math import compute


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def d(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def q2(v: Decimal) -> str:
    return str(v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def main() -> None:
    ap = argparse.ArgumentParser(description="Apply NAV snapshot by shares/costBasis method")
    ap.add_argument("--state", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--snapshot", required=True)
    args = ap.parse_args()

    state_path = Path(args.state)
    ledger_path = Path(args.ledger)
    snap_path = Path(args.snapshot)

    state = load_json(state_path)
    snap = load_json(snap_path)

    items = snap.get("items", [])
    if not isinstance(items, list) or not items:
        raise SystemExit("invalid snapshot items")

    by_code = {str(i.get("code")): i for i in items}
    out = deepcopy(state)

    for h in out.get("holdings", []):
        code = str(h.get("code"))
        if code not in by_code:
            raise SystemExit(f"snapshot missing code: {code}")

        item = by_code[code]
        if str(item.get("name", "")).strip() != str(h.get("name", "")).strip():
            raise SystemExit(f"code-name mismatch for {code}")

        shares = d(h.get("shares", h.get("totalShares", "0")))
        if shares <= 0:
            raise SystemExit(f"shares missing/invalid for {code}")

        cost_unit = d(h.get("costBasisUnit", "0"))
        nav = d(item.get("nav", "0"))
        if nav <= 0:
            raise SystemExit(f"snapshot nav invalid for {code}")

        market_value = shares * nav
        cost_total = shares * cost_unit
        upnl = market_value - cost_total

        h["latestNav"] = str(nav)
        h["marketValue"] = q2(market_value)
        h["unrealizedPnl"] = q2(upnl)
        h.setdefault("totalShares", str(shares))
        h.setdefault("availableShares", h.get("totalShares"))

    out["asOf"] = snap.get("asOf") or now_iso()

    before = compute(state)
    after = compute(out)

    save_json(state_path, out)

    event = {
        "ts": now_iso(),
        "event": "mark_to_market_refresh",
        "snapshotAsOf": out["asOf"],
        "method": "shares_costbasis",
        "before": before,
        "after": after,
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(json.dumps({"ok": True, "event": "mark_to_market_refresh", "asOf": out["asOf"], "after": after}, ensure_ascii=False))


if __name__ == "__main__":
    main()
