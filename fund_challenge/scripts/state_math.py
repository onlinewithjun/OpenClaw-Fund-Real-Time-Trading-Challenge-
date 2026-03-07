from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

TWOPL = Decimal("0.01")


def q(v: Decimal) -> str:
    return str(v.quantize(TWOPL, rounding=ROUND_HALF_UP))


def d(x: str) -> Decimal:
    return Decimal(str(x))


def compute(state: dict) -> dict:
    holdings = state.get("holdings", [])
    cash = d(state.get("cash", "0"))

    mv = sum(d(h.get("marketValue", "0")) for h in holdings)
    pnl = sum(d(h.get("unrealizedPnl", "0")) for h in holdings)
    nav = cash + mv
    target = d(state.get("challenge", {}).get("targetValue", "2000"))
    gap = target - nav

    return {
        "cash": q(cash),
        "holdingsMarketValue": q(mv),
        "portfolioValue": q(nav),
        "totalUnrealizedPnl": q(pnl),
        "targetValue": q(target),
        "distanceToTarget": q(gap),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Deterministic state math for fund challenge")
    ap.add_argument("--state", required=True, help="Path to state.json")
    args = ap.parse_args()

    p = Path(args.state)
    state = json.loads(p.read_text(encoding="utf-8"))
    result = compute(state)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
